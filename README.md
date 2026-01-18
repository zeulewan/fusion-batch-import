# Fusion Batch Import for Fusion 360

Bulk import `.f3d` files from a local folder into Fusion 360's Data Panel, preserving the complete folder structure.
Originally built for the [VEX robotics](https://github.com/vindou/VEX-CAD-Fusion-360-Library) library.

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [VEX CAD Library](#vex-cad-library)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)

## Installation

### Easy Install (Recommended)

1. Install the free [GitHubToFusion360](https://apps.autodesk.com/FUSION/en/Detail/Index?id=789800822168335025) app from Autodesk App Store
2. In Fusion 360, press `Shift+S` to open Scripts and Add-Ins
3. Find and run **GitHubToFusion360**
4. Paste this URL: `https://github.com/zeulewan/fusion-batch-import`
5. Click Install. Done

### Manual Install

**Option A: Copy to Scripts Folder**

1. Download or clone this repository
2. Copy the entire `FusionBatchImport` folder to your Fusion 360 Scripts directory:

   - **macOS:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/`
   - **Windows:** `%appdata%\Autodesk\Autodesk Fusion 360\API\Scripts\`

3. Restart Fusion 360

**Option B: Add Script Manually**

1. Open Fusion 360
2. Go to **Utilities** > **Scripts and Add-Ins** (or press `Shift+S`)
3. Click the **+** button next on the top left. Click `Script of add-in from device`.
4. Navigate to and select the `FusionBatchImport` folder
5. Click **Open**
6. No need for restart

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
   - Select **FusionBatchImport**
   - Click **Run**

4. **Follow the prompts**:
   - Select your source folder (e.g., `VEX-Library`)
   - Confirm the destination project
   - Wait for import to complete

5. **Verify**: Check the Data Panel - your folder structure should appear with all files

## VEX CAD Library

This tool was built for the [VEX-CAD-Fusion-360-Library](https://github.com/vindou/VEX-CAD-Fusion-360-Library):

1. Download the library from GitHub
2. Extract the ZIP file
3. Run this script and select the extracted folder
4. All VEX parts will be imported with proper organization
5. Script takes ~2 mins to run, and another 5 or 10 for all the uploads to process.

## Notes

1. Files upload in the background after the script completes. Large libraries may take a few minutes to fully sync.
3. Currently imports to the root of the active project.

## Troubleshooting

### "Upload failed" errors
- Requires internet connection for API usage
- Verify the `.f3d` files are valid Fusion 360 archives
- Try importing a smaller batch

### Script doesn't appear
- Ensure the folder contains both `.py` and `.manifest` files
- Try restarting Fusion 360
