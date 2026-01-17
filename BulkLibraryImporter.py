#Author-Zeul
#Description-Bulk import .f3d files from a local folder into Fusion 360 Data Panel, preserving folder structure

import adsk.core
import adsk.fusion
import traceback
import os

# Global handlers to keep them in scope
_handlers = []

def get_source_folder(ui: adsk.core.UserInterface) -> str:
    """Open folder dialog to select local source folder containing .f3d files."""
    dlg = ui.createFolderDialog()
    dlg.title = "Select Library Folder to Import"

    if dlg.showDialog() == adsk.core.DialogResults.DialogOK:
        return dlg.folder
    return None


def get_destination_folder(ui: adsk.core.UserInterface, app: adsk.core.Application) -> adsk.core.DataFolder:
    """Confirm or let user select destination project in Data Panel."""
    project = app.data.activeProject

    if project is None:
        ui.messageBox(
            "No active project found.\n\nPlease open or create a project in the Data Panel first.",
            "No Active Project",
            adsk.core.MessageBoxButtonTypes.OKButtonType,
            adsk.core.MessageBoxIconTypes.WarningIconType
        )
        return None

    result = ui.messageBox(
        f"Import library to project:\n\n'{project.name}'\n\n"
        "Make sure the correct project is active before clicking Yes.",
        "Confirm Destination Project",
        adsk.core.MessageBoxButtonTypes.YesNoButtonType,
        adsk.core.MessageBoxIconTypes.QuestionIconType
    )

    if result == adsk.core.DialogResults.DialogYes:
        return project.rootFolder
    return None


def scan_folder(source_path: str) -> tuple:
    """
    Recursively scan source folder for .f3d files.

    Returns:
        tuple: (folders_list, files_list)
            - folders_list: List of relative folder paths to create
            - files_list: List of (relative_path, absolute_path) for .f3d files
    """
    folders = set()
    files = []

    top_folder_name = os.path.basename(source_path)

    for root, dirs, filenames in os.walk(source_path):
        # Calculate relative path from source
        rel_root = os.path.relpath(root, source_path)

        # Add all directory paths (including intermediate ones)
        if rel_root != '.':
            # Include top folder name in path
            folder_path = os.path.join(top_folder_name, rel_root)
            folders.add(folder_path)
            # Also add all parent folders
            parts = folder_path.split(os.sep)
            for i in range(1, len(parts) + 1):
                folders.add(os.sep.join(parts[:i]))
        else:
            folders.add(top_folder_name)

        # Add .f3d files
        for filename in filenames:
            if filename.lower().endswith('.f3d'):
                abs_path = os.path.join(root, filename)
                if rel_root != '.':
                    rel_path = os.path.join(top_folder_name, rel_root, filename)
                else:
                    rel_path = os.path.join(top_folder_name, filename)
                files.append((rel_path, abs_path))

    # Sort folders by depth (create parent folders first)
    sorted_folders = sorted(list(folders), key=lambda x: x.count(os.sep))

    return sorted_folders, files


def check_conflict(dest_folder: adsk.core.DataFolder, folder_name: str) -> bool:
    """Check if a folder with the given name already exists in destination."""
    try:
        existing = dest_folder.dataFolders.itemByName(folder_name)
        return existing is not None
    except:
        return False


def ensure_folder_path(root_folder: adsk.core.DataFolder, rel_path: str) -> adsk.core.DataFolder:
    """
    Create nested folder structure as needed.

    Args:
        root_folder: The root DataFolder to start from
        rel_path: Relative path like "VEX-Library/Motors/V5"

    Returns:
        The leaf DataFolder at the end of the path
    """
    parts = rel_path.split(os.sep)
    current = root_folder

    for part in parts:
        if not part:
            continue

        # Try to find existing folder
        try:
            existing = current.dataFolders.itemByName(part)
            if existing:
                current = existing
            else:
                # Create new folder
                current = current.dataFolders.add(part)
        except:
            # If itemByName fails, try to create
            try:
                current = current.dataFolders.add(part)
            except Exception as e:
                raise Exception(f"Failed to create folder '{part}': {str(e)}")

    return current


def upload_files(
    ui: adsk.core.UserInterface,
    dest_root: adsk.core.DataFolder,
    folders: list,
    files: list
) -> tuple:
    """
    Create folder structure and upload .f3d files with progress tracking.

    Returns:
        tuple: (success_count, errors_list)
    """
    total_files = len(files)
    success_count = 0
    errors = []

    # Create progress dialog
    progress = ui.createProgressDialog()
    progress.cancelButtonText = "Cancel"
    progress.isBackgroundTranslucent = False
    progress.isCancelButtonShown = True

    # Phase 1: Create folder structure
    progress.show(
        "Creating Folder Structure",
        f"Creating {len(folders)} folders...",
        0, len(folders), 0
    )

    folder_cache = {}  # Cache created folders for faster lookup

    for i, folder_path in enumerate(folders):
        if progress.wasCancelled:
            progress.hide()
            return success_count, ["Import cancelled by user"]

        try:
            folder = ensure_folder_path(dest_root, folder_path)
            folder_cache[folder_path] = folder
        except Exception as e:
            errors.append(f"Folder '{folder_path}': {str(e)}")

        progress.progressValue = i + 1
        progress.message = f"Creating folder: {os.path.basename(folder_path)}"

        # Allow UI to update
        adsk.doEvents()

    progress.hide()

    if not files:
        return success_count, errors

    # Phase 2: Upload files
    progress.show(
        "Importing Library",
        f"Importing 0/{total_files} files...",
        0, total_files, 0
    )

    for i, (rel_path, abs_path) in enumerate(files):
        if progress.wasCancelled:
            progress.hide()
            errors.append("Import cancelled by user")
            break

        try:
            # Get parent folder path
            parent_rel = os.path.dirname(rel_path)

            # Get target folder from cache or create
            if parent_rel in folder_cache:
                target_folder = folder_cache[parent_rel]
            else:
                target_folder = ensure_folder_path(dest_root, parent_rel)
                folder_cache[parent_rel] = target_folder

            # Upload file (queued for background upload)
            target_folder.uploadFile(abs_path)
            success_count += 1

        except Exception as e:
            errors.append(f"File '{os.path.basename(abs_path)}': {str(e)}")

        progress.progressValue = i + 1
        progress.message = f"Importing {i+1}/{total_files}: {os.path.basename(abs_path)}"

        # Allow UI to update
        adsk.doEvents()

    progress.hide()

    return success_count, errors


def run(context):
    """Main entry point for the script."""
    ui = None

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Step 1: Get source folder
        ui.messageBox(
            "This script will import a folder of .f3d files into your Fusion 360 Data Panel, "
            "preserving the folder structure.\n\n"
            "You will be asked to:\n"
            "1. Select the source folder containing .f3d files\n"
            "2. Confirm the destination project\n\n"
            "Click OK to continue.",
            "Bulk Library Importer",
            adsk.core.MessageBoxButtonTypes.OKButtonType,
            adsk.core.MessageBoxIconTypes.InformationIconType
        )

        source = get_source_folder(ui)
        if not source:
            return

        # Validate source folder
        if not os.path.isdir(source):
            ui.messageBox(
                f"Invalid folder path:\n{source}",
                "Error",
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.CriticalIconType
            )
            return

        # Step 2: Get destination project
        dest = get_destination_folder(ui, app)
        if not dest:
            return

        # Step 3: Scan source folder
        top_folder_name = os.path.basename(source)
        folders, files = scan_folder(source)

        if not files:
            ui.messageBox(
                f"No .f3d files found in:\n{source}\n\n"
                "Make sure the folder contains Fusion 360 archive files (.f3d).",
                "No Files Found",
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.WarningIconType
            )
            return

        # Step 4: Check for conflicts
        if check_conflict(dest, top_folder_name):
            result = ui.messageBox(
                f"A folder named '{top_folder_name}' already exists in the destination project.\n\n"
                "Do you want to continue anyway?\n"
                "(Existing files with the same name may be duplicated)",
                "Folder Already Exists",
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.WarningIconType
            )
            if result != adsk.core.DialogResults.DialogYes:
                return

        # Step 5: Confirm import
        result = ui.messageBox(
            f"Ready to import:\n\n"
            f"Source: {source}\n"
            f"Files: {len(files)} .f3d files\n"
            f"Folders: {len(folders)} folders to create\n\n"
            f"Continue with import?",
            "Confirm Import",
            adsk.core.MessageBoxButtonTypes.YesNoButtonType,
            adsk.core.MessageBoxIconTypes.QuestionIconType
        )
        if result != adsk.core.DialogResults.DialogYes:
            return

        # Step 6: Perform import
        success_count, errors = upload_files(ui, dest, folders, files)

        # Step 7: Show summary
        if errors:
            error_summary = "\n".join(errors[:10])
            if len(errors) > 10:
                error_summary += f"\n... and {len(errors) - 10} more errors"

            ui.messageBox(
                f"Import completed with errors.\n\n"
                f"Successfully queued: {success_count}/{len(files)} files\n\n"
                f"Errors ({len(errors)}):\n{error_summary}",
                "Import Complete (with errors)",
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.WarningIconType
            )
        else:
            ui.messageBox(
                f"Script finished!\n\n"
                f"Queued: {success_count} files\n"
                f"Created: {len(folders)} folders\n\n"
                f"Location: {top_folder_name}/\n\n"
                "Uploads are processing in the background.\n"
                "Large libraries may take a while to fully appear in the Data Panel.",
                "Import Complete",
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )

    except:
        if ui:
            ui.messageBox(
                f"An unexpected error occurred:\n\n{traceback.format_exc()}",
                "Error",
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.CriticalIconType
            )
