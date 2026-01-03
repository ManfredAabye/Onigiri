# Onigiri 4

Rigging add-on for Blender 4.1.* to Blender 4.5.*, based on [Onigiri](https://github.com/nessaki/Onigiri)

Download the .zip file from the Releases area to install as a Blender Add-on.

The .zip is created from the GitHub repository code using only the Onigiri directory.

## Blender 5.0 Compatibility

This add-on has been updated for Blender 5.0:

- All PropertyGroup and Operator property declarations have been converted to the new assignment-with-type format.
- The codebase is now formally Blender 5.0 compatible.
- The Collada export function has been removed/replaced; glTF is now recommended.

Note: For older Blender versions (<5.0), please continue to use the previous add-on version.

---

## Onigiri Documentation

## Overview

Onigiri is a rigging and conversion add-on for Blender, designed especially for working with avatars and animations for OpenSim and Second Life. It supports mapping, adjustment, and export of rigs and meshes, especially for glTF workflows.

---

## Installation

1. Download the Onigiri add-on as a ZIP file.
2. Open Blender and go to `Edit > Preferences > Add-ons > Install`.
3. Select the ZIP file and install the add-on.
4. Enable the add-on in the add-on list.

---

## Main Features

### 1. Character Converter

- Converts avatars and rigs to OpenSim/Second Life compatible skeletons.
- Supports Mixamo, DAZ, Avastar, and other common rigs.
- Automatic and manual bone mapping.

### 2. Mapper

- Detailed mapping tool for bones between source and target rigs.
- Supports reskinning, bone renaming, and hierarchy adjustment.
- Visualization of bone mapping in the 3D view.

### 3. Sliders & Shape Tools

- Adjust body shapes and proportions using sliders.
- Save and load shape presets.

### 4. Export

- Export models and rigs as glTF 2.0 for OpenSim/Second Life.
- Support for animations and materials.

---

## Typical Workflows

### Prepare Mixamo Avatar for OpenSim/SL

1. Import the Mixamo model (FBX).
2. Open the Onigiri panel and start the Character Converter.
3. Map the bones to the OpenSim/SL rig.
4. Check and optimize weights.
5. Export as glTF.

### Convert DAZ/Avastar Avatar

1. Import the DAZ/Avastar model.
2. Use the Character Converter and Mapper.
3. Adjust bone names and hierarchy.
4. Export as glTF.

---

## Tips & Notes

- Save Blender files regularly as backups.
- Test models in a test region after upload.
- Use Onigiri tools for shape and weight optimization.
- If you have problems: see README, CHANGELOG, or this manual.

---

## Support & Community

- GitHub: <https://github.com/nessaki/Onigiri>
- Official documentation (English): <https://github.com/nessaki/Onigiri/wiki>
- For questions and help: see README or create a GitHub issue.

---

## Manual: Exporting a Mixamo-Avatar as glTF for OpenSim/Second Life

This how-to explains how to import a Mixamo-rigged avatar model into Blender, prepare it for OpenSim/Second Life, and export it as glTF.

## Requirements

- Blender 5.0 or newer
- Onigiri add-on installed and enabled
- Mixamo avatar as FBX file

## Step 1: Import Mixamo Avatar

1. Start Blender and open a new scene.
2. Go to `File > Import > FBX (.fbx)`.
3. Select your Mixamo avatar FBX file and import it.
4. Check if the model and rig are displayed correctly.

## Step 2: Prepare Rig for OpenSim/Second Life

1. Select the imported armature object.
2. Open the Onigiri panel (usually in the properties or right side of the 3D view).
3. In the Onigiri panel, choose the function to convert or map to an OpenSim/Second Life compatible rig:
    - Use the "Character Converter" or "Mapper" function if needed.
    - Select "Second Life / OpenSim" as the target platform.
    - Follow the add-on instructions to map the bones correctly.
4. Check bone names and hierarchy. Adjust them to OpenSim/SL standards if necessary (e.g., "mPelvis", "mTorso", "mHead", etc.).
5. Optionally, use Onigiri tools to optimize vertex groups, weights, and pose.

## Step 3: Clean and Test the Model

1. Remove unnecessary meshes, bones, or helper objects.
2. Check skinning weights and animations (if present).
3. Make sure the model is in T-pose or A-pose (depending on the target platform).

## Step 4: Export as glTF

1. Select the armature object and the mesh.
2. Go to `File > Export > glTF 2.0 (.glb/.gltf)`.
3. Choose the option `Selected Objects`.
4. Make sure "Animations" is enabled if you want to export animations.
5. Choose a location and export the file.

## Step 5: Import into OpenSim/Second Life

1. Use a viewer or import tool that supports glTF (e.g., DreamGrid, OpenSim distributions with glTF support).
2. Upload the glTF model and check rigging and animations.
3. Adjust materials and textures if necessary.

## Tips&Notes

- Mixamo rigs often need to be mapped manually to the OpenSim/SL bone structure.
- Onigiri offers tools for automatic and manual mapping.
- Test the model in a test region after upload.
- For complex avatars, it is recommended to save as a Blender file in between.

---
Questions or problems? See README, CHANGELOG, or the Onigiri documentation for further information.
