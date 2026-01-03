# Manual: Exporting a Mixamo-Avatar as glTF for OpenSim/Second Life

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

## Tips & Notes

- Mixamo rigs often need to be mapped manually to the OpenSim/SL bone structure.
- Onigiri offers tools for automatic and manual mapping.
- Test the model in a test region after upload.
- For complex avatars, it is recommended to save as a Blender file in between.

---
Questions or problems? See README, CHANGELOG, or the Onigiri documentation for further information.
