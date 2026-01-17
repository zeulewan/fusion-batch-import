# Bulk Library Importer for Fusion 360

Bulk import `.f3d` files from a local folder into Fusion 360's Data Panel, preserving the complete folder structure. Universal tool that works with any CAD library, optimized for VEX robotics.

## Features

- **Recursive Import**: Imports all `.f3d` files from a folder and all subfolders
- **Structure Preservation**: Recreates the exact folder hierarchy in the Data Panel
- **Progress Tracking**: Real-time progress bar showing import status
- **Conflict Detection**: Warns if destination folder already exists
- **Error Handling**: Graceful handling of failed imports with detailed summary

## Installation

### Method 1: Copy to Scripts Folder (Recommended)

1. Download or clone this repository
2. Copy the entire `BulkLibraryImporter` folder to your Fusion 360 Scripts directory:

   **macOS:**
   ```
   ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/
   ```

   Quick copy command (macOS):
   ```bash
   cp -r /Users/zeul/GIT/BulkLibraryImporter ~/Library/Application\ Support/Autodesk/Autodesk\ Fusion\ 360/API/Scripts/
   ```

   **Windows:**
   ```
   %appdata%\Autodesk\Autodesk Fusion 360\API\Scripts\
   ```

3. Restart Fusion 360 (or refresh scripts)

### Method 2: Run Directly

1. Open Fusion 360
2. Go to **Utilities** > **Scripts and Add-Ins** (or press `Shift+S`)
3. Click the green **+** button next to "My Scripts"
4. Navigate to and select the `BulkLibraryImporter` folder
5. Click **Open**

## Usage

1. **Prepare your library**: Organize your `.f3d` files in folders on your computer. Example:
   ```
   VEX-Library/
   ├── Motors/
   │   ├── V5_Smart_Motor.f3d
   │   └── V5_Motor_Cartridge.f3d
   ├── Structure/
   │   ├── C-Channels/
   │   │   ├── 2x25_C-Channel.f3d
   │   │   └── 2x35_C-Channel.f3d
   │   └── Plates/
   │       └── 5x5_Plate.f3d
   └── Hardware/
       ├── Screws/
       └── Nuts/
   ```

2. **Open a project**: Make sure the correct project is active in the Data Panel

3. **Run the script**:
   - Go to **Utilities** > **Scripts and Add-Ins**
   - Select **BulkLibraryImporter**
   - Click **Run**

4. **Follow the prompts**:
   - Select your source folder (e.g., `VEX-Library`)
   - Confirm the destination project
   - Wait for import to complete

5. **Verify**: Check the Data Panel - your folder structure should appear with all files

## VEX CAD Library

This tool is optimized for the [VEX-CAD-Fusion-360-Library](https://github.com/vindou/VEX-CAD-Fusion-360-Library):

1. Download the library from GitHub
2. Extract the ZIP file
3. Run this script and select the extracted folder
4. All VEX parts will be imported with proper organization

## Known Limitations

1. **Async Uploads**: Files upload in the background after the script completes. Large libraries may take a few minutes to fully sync.

2. **No Selective Import**: V1 imports everything in the folder. Future versions may add filtering.

3. **Project Root Only**: Currently imports to the root of the active project. Subfolder destination selection coming in V2.

## Troubleshooting

### "No active project found"
- Open or create a project in the Data Panel before running the script

### "Upload failed" errors
- Check your internet connection
- Verify the `.f3d` files are valid Fusion 360 archives
- Try importing a smaller batch

### Script doesn't appear
- Ensure the folder contains both `.py` and `.manifest` files
- Try restarting Fusion 360

## Requirements

- Autodesk Fusion 360 (any recent version)
- macOS or Windows
- No external dependencies (uses embedded Python)

## License

MIT License - Free to use, modify, and distribute.

## Credits

Created for the VEX robotics community.
