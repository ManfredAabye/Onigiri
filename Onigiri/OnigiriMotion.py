import bpy # type: ignore
import os
import traceback
from bpy_extras.io_utils import ImportHelper, ExportHelper # type: ignore
from . import motion, utils, animutils, rigutils, snap
import bpy.props # type: ignore
from . import mod_settings

# OnigiriMotionProperties
# OnigiriMotionRemoveObjectAnimation
# OnigiriMotionApplyTransforms
# OnigiriMotionRemoveTransforms
# OnigiriMotionCycleRig
# OnigiriMotionHipCorrectionStart
# OnigiriMotionHipCorrectionEnd
# OnigiriMotionHipCorrectionReset
# OnigiriMotionMapLoad
# OnigiriMotionMapSave
# OnigiriMotionMatchMap
# OnigiriMotionMapClean
# OnigiriMotionReset
# OnigiriMotionAction
# OnigiriMotionAnchor
# OnigiriMotionMesh
# OnigiriMotionViewBones
# OnigiriMotionHideTarget
# OnigiriMotionMapAdd
# OnigiriMotionMapRemove
# OnigiriMotionMapSelect
# OnigiriMotionLockSelected
# OnigiriMotionLockRemove
# OnigiriMotionApplyScale
# OnigiriMotionMixerProperties
# OnigiriMotionMixerLockTarget
# OnigiriMotionMixerAddSource
# OnigiriMotionMixerRemoveSource
# OnigiriMotionMixerReady
# OnigiriMotionMixerActiveRigName
# OnigiriMotionMixerSetAnchor
# OnigiriMotionMixerMode
# OnigiriMotionMixerSpace
# OnigiriMotionMixerInherit
# OnigiriMotionMixerAddBones
# OnigiriMotionMixerRemoveBones
# OnigiriMotionMixerSetLocation
# OnigiriMotionMixerSetRotation
# OnigiriMotionMixerSetScale
# OnigiriMotionSpliceProperties
# OnigiriMotionSpliceSync
# OnigiriMotionSpliceReset
# OnigiriMotionSpliceCapture

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = oni_settings["paths"]["data"]

# region OnigiriMotionProperties
class OnigiriMotionProperties(bpy.types.PropertyGroup):

    def update_motion_blank(self, context):
        self["motion_blank"] = False

    motion_blank: bpy.props.BoolProperty(default=False, update=update_motion_blank)

    motion_menu_enabled: bpy.props.BoolProperty(
        name="",
        description="Retarget Motion"
        "\n\n"
        "This is where you retarget animations if any kind.  There are other retargeting tools included with Onigiri "
        "that also do this but this one is a replacement for all of them except if you want to retarget multiple avatars at "
        "once but that feature is going away for a more simpler approach.",
        default=False,
    )
    motion_distance: bpy.props.FloatProperty(
        name="",
        description="The distance that the generated rig will be from origin on its Y axis.  This is a visual convenience but it "
        "could cause location issues where your multiple mesh objects will be out of sync.  Leaving this at 0 is safe "
        "if you have a streamlined workfow or set it to around 0.6 for a good visual distance when remapping.",
        default=0.0,
    )
    motion_stabilize: bpy.props.BoolProperty(
        name="",
        description="Bone Stabilizer"
        "\n\n"
        "This will almost certainly break your avatar in Second Life if you are not using a custom rig setup.  This pins "
        "the unused bones down to help prevent woonile when using an unusual hierarchy.  This is what you want if you used "
        "an arbitrary bone set in the Visual Snap Mapper.  It also works for well configured bone chains as long as your "
        "avatar is using all of the bones present that are glued.",
        default=False,
    )
    motion_glue: bpy.props.BoolProperty(
        name="",
        description="Hard Re-Target"
        "\n\n"
        "This glues the mapped target bones onto your animation source bones.  This is a brute force retargeting that can "
        "work with very odd rigs or if you are retargeting a non-bipedal entity or using joint location animations on a custom rig.",
        default=False,
    )
    motion_to_animation: bpy.props.BoolProperty(
        name="",
        description="Send details to animation tools"
        "\n\n"
        "This will send the range of your current animation to the (range) and (loop) settings in the "
        "animation export tool.  The alternative is to use the (Acquire) button in the animation exporter "
        "to grab the ranges.  Keep in mind that the (Loop) feature must be enabled in order for loop to work.",
        default=True,
    )
    motion_prepare_actor: bpy.props.BoolProperty(
        name="",
        description="The Actor is the rig that mimics your animation.  This mimic rig is responsible for exporting your animation "
        "so it must be in a somewhat clean condition.  If the tool is generating a copy of your rig for use then you "
        "probably want to enable this to get a sort of mannequin skeleton without transforms or animations.  This "
        "setting has no meaning when using (Glue)",
        default=False,
    )

    def update_motion_match_map(self, context):
        self["motion_match_map"] = True

    motion_match_map: bpy.props.BoolProperty(
        name="",
        description="A map was generated using the existing rig's bone names.  To use an alternate method use (Clean Maps).  "
        "To automatically generate a Second Life rig make sure (Custom Target) is disabled.",
        default=True,
        update=update_motion_match_map,
    )

    def update_motion_interactive_menu_enabled(self, context):
        selected = bpy.context.selected_objects
        if len(selected) == 0:
            print("Nothing selected")
            self["motion_interactive_menu_enabled"] = False
            return

        if self.motion_interactive_menu_enabled:
            inRig = motion.get_director(selected[0])
            if not inRig:
                print("No director")
                self["motion_interactive_menu_enabled"] = False
                return
            outRig = inRig.get("oni_motion_actor")
            if outRig is None:
                print("No actor")
                self["motion_interactive_menu_enabled"] = False
                return
            for o in selected:
                o.select_set(False)
            inRig.select_set(True)
            outRig.select_set(True)
            utils.activate(inRig)
            bpy.ops.object.mode_set(mode="POSE")
            for boneObj in bpy.context.selected_pose_bones:
                boneObj.bone.select = False
            props["director_bone"] = ""
            props["actor_bone"] = ""

        else:

            inRig = motion.get_director(selected[0])
            utils.get_state()
            if inRig:
                outRig = inRig.get("oni_motion_actor")
                if outRig is not None:
                    outRig.select_set(True)
                    utils.activate(outRig)

                else:
                    print(
                        "Retargeter found a director but no actor, defaulting to selected and active director, look into this"
                    )
                    inRig.select_set(True)
                    utils.activate(inRig)

    motion_interactive_menu_enabled: bpy.props.BoolProperty(
        name="",
        description="This enables an interactive mapper so that you can map your retarget bones right here in the retargeter for "
        "a visual of how the Actor will respond with your animaton.",
        default=False,
        update=update_motion_interactive_menu_enabled,
    )

    motion_view_map_menu_enabled: bpy.props.BoolProperty(
        name="",
        description="View the mapped bones",
        default=False,
    )

    def update_motion_anchor_location_x(self, context):
        bpy.ops.onigiri.motion_anchor(transform="location", axis="x", action="disable")

    def update_motion_anchor_location_y(self, context):
        bpy.ops.onigiri.motion_anchor(transform="location", axis="y", action="disable")

    def update_motion_anchor_location_z(self, context):
        bpy.ops.onigiri.motion_anchor(transform="location", axis="z", action="disable")

    def update_motion_anchor_rotation_x(self, context):
        bpy.ops.onigiri.motion_anchor(transform="rotation", axis="x", action="disable")

    def update_motion_anchor_rotation_y(self, context):
        bpy.ops.onigiri.motion_anchor(transform="rotation", axis="y", action="disable")

    def update_motion_anchor_rotation_z(self, context):
        bpy.ops.onigiri.motion_anchor(transform="rotation", axis="z", action="disable")

    motion_anchor_location_x: bpy.props.BoolProperty(
        default=True, update=update_motion_anchor_location_x
    )
    motion_anchor_location_y: bpy.props.BoolProperty(
        default=True, update=update_motion_anchor_location_y
    )
    motion_anchor_location_z: bpy.props.BoolProperty(
        default=True, update=update_motion_anchor_location_z
    )
    motion_anchor_rotation_x: bpy.props.BoolProperty(
        default=False, update=update_motion_anchor_rotation_x
    )
    motion_anchor_rotation_y: bpy.props.BoolProperty(
        default=False, update=update_motion_anchor_rotation_y
    )
    motion_anchor_rotation_z: bpy.props.BoolProperty(
        default=False, update=update_motion_anchor_rotation_z
    )

    def update_constrain_location(self, context):
        selected = bpy.context.selected_objects
        if len(selected) == 0:
            print("Nothing selected")
            self["motion_constrain_location"] = False
            return
        inRig = motion.get_director(selected[0])
        if not inRig:
            print("No director")
            self["motion_constrain_location"] = False
            return

        motion.update_map(inRig=inRig)

    motion_constrain_location: bpy.props.BoolProperty(
        name="",
        description="This takes a moment to engage so be patient.  Also, it only works when (Interactive Retargeting) is enabled."
        "\n\n"
        "Location constraints can be tricky.  It allows relative location motion which is usually not useful "
        "when retargeting.  The hip / pelvis usually the only target that can benefit from this when using "
        "Second Life but this works as expected so it's here but if you need this and you have a custom rig "
        "then you probably want to reset the stage and use (Glue) instead.",
        default=False,
        update=update_constrain_location,
    )

    clean_motion_menu_enabled: bpy.props.BoolProperty(
        name="",
        description="Clean Motion"
        "\n\n"
        " * Fix armature <-> animation transforms (you can fix the scale problem here)"
        " * Fix hip height, location"
        "\n\n",
        default=False,
    )
    clean_motion_hip_start: bpy.props.BoolProperty(
        name="",
        description="start",
        default=False,
    )
    clean_motion_hip_end: bpy.props.BoolProperty(
        name="",
        description="end",
        default=True,
    )

    def update_motion_use_shapes(self, context):
        if len(bpy.context.selected_objects) == 0:
            self["motion_use_shapes"] = False
            return
        armObj = bpy.context.selected_objects[0]
        inRig = motion.get_director(armObj)
        if not inRig:
            self["motion_use_shapes"] = False
            return
        outRig = inRig["oni_motion_actor"]
        outRig.data.show_bone_custom_shapes = self.motion_use_shapes

    motion_use_shapes: bpy.props.BoolProperty(
        name="",
        description="The is a visual only.  It's provided in order to clean up the view when using the lock features while you're not "
        "using the Glue feature.  If you're snapping your bones to the source animation rig then you will see some strange "
        "configuration that cannot be easily rectified but does not affect the animation outcome.  The purpose of this switch "
        "is to just be a more visually readable appearance for your work",
        default=False,
        update=update_motion_use_shapes,
    )


class OnigiriMotionRemoveObjectAnimation(bpy.types.Operator):
    """This removes the animation from the object only, not the armature/bone animations"""

    bl_idname = "onigiri.motion_remove_object_animation"
    bl_label = "Remove Object Animation"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        return True

    def execute(self, context):

        oni_motion = bpy.context.window_manager.oni_motion
        armObj = bpy.context.selected_objects[0]
        actionObj = armObj.animation_data.action
        fcurves = actionObj.fcurves
        fcurve_paths = {}
        for boneObj in armObj.data.bones:
            path_key = 'pose.bones["' + boneObj.name + '"]'
            fcurve_paths[path_key] = boneObj.name
        for fc in fcurves:
            dp, idx = fc.data_path, fc.array_index
            bone_path, delimiter, transform_type = dp.rpartition(".")
            if bone_path not in fcurve_paths:
                if bone_path == "":
                    print("Object animation detected, removing fcurve")
                    fcurves.remove(fc)

        return {"FINISHED"}


class OnigiriMotionApplyTransforms(bpy.types.Operator):
    """Choose a rig with an animation on it.  It's assumed that the animation has scale
    data applied to it and you want to fix that by applying scale to the rig and also have
    the animation function after this.  Other options are available"""

    bl_idname = "onigiri.motion_apply_transforms"
    bl_label = "Apply Transforms"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        return True

    def execute(self, context):

        oni_motion = bpy.context.window_manager.oni_motion

        tarmObj = bpy.context.selected_objects[0]

        result = animutils.apply_transforms(tarmObj, report=True)

        if not result:
            print("The call to animutils::apply_transforms seems to have failed")
            popup("Motion transfer failed", "Error", "ERROR")
            return {"FINISHED"}

        return {"FINISHED"}


class OnigiriMotionRemoveTransforms(bpy.types.Operator):
    """Remove Scale, Euler (rotation), Quaternion (rotation) or translation
    (location) transforms from the animated selected pose bones."""

    bl_idname = "onigiri.motion_remove_transforms"
    bl_label = "Remove Transforms"

    action: bpy.props.StringProperty(default="scale")

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]

        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        return True

    def execute(self, context):

        if self.action == "scale":
            trs = "scale"
        elif self.action == "euler":
            trs = "rotation_euler"
        elif self.action == "quats":
            trs = "rotation_quaternion"
        elif self.action == "trans":
            trs = "location"

        fcurve_paths = {}
        for boneObj in bpy.context.selected_pose_bones:
            path_key = 'pose.bones["' + boneObj.name + '"]'
            fcurve_paths[path_key] = boneObj.name

        armObj = bpy.context.selected_objects[0]
        actionObj = armObj.animation_data.action
        fcurves = actionObj.fcurves
        for fc in fcurves:
            dp, idx = fc.data_path, fc.array_index
            bone_path, delimiter, transform = dp.rpartition(".")

            if bone_path not in fcurve_paths:
                continue

            if transform == trs:
                fcurves.remove(fc)

        return {"FINISHED"}


class OnigiriMotionCycleRig(bpy.types.Operator):
    """This does a seamless export of the selected rig with it's animation in bvh
    file type then imports it back.  This is a way of cleaning up a difficult rig and
    associated animation"""

    bl_idname = "onigiri.motion_cycle_rig"
    bl_label = "Cycle Rig"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        return True

    def execute(self, context):

        oni_motion = bpy.context.window_manager.oni_motion

        armObj = bpy.context.selected_objects[0]

        newObj = rigutils.cycle_rig(armObj)
        if not newObj:
            print("Couldn't recycle rig")
            popup("Cycle failed", "Error", "ERROR")

        return {"FINISHED"}


class OnigiriMotionHipCorrectionStart(bpy.types.Operator):
    """This frame is the frame where your character/rig/animation looks correct,
    it is where you would like your avatar to be instead of the broken frame, which
    you will pick next.  This adjusts location/translation"""

    bl_idname = "onigiri.motion_hip_correction_start"
    bl_label = "Reference frame"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        if motion.props["hip_start"] is not None:
            return False

        if motion.props["hip_rig"] == o:
            return False
        return True


    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        try:
            armObj = bpy.context.selected_objects[0]
            frame_current = bpy.context.scene.frame_current
            motion.props["hip_rig"] = armObj
            motion.props["hip_start"] = frame_current
            motion.props["hip_end"] = None
            print(f"Hip Correction Start gesetzt: Rig={armObj.name}, Frame={frame_current}")
            popup(f"Hip Correction Start gesetzt: Frame {frame_current}", "Info", "INFO")
            return {"FINISHED"}
        except Exception as e:
            print(f"Fehler bei Hip Correction Start: {e}")
            popup(f"Fehler bei Hip Correction Start: {e}", "Fehler", "ERROR")
            return {"CANCELLED"}


class OnigiriMotionHipCorrectionEnd(bpy.types.Operator):
    """After choosing the good frame you'll move the time slider to the spot where
    your avtar looks wrong.  This and all key frames after, will be position corrected
    to bring your animation into the area of the first/good frame"""

    bl_idname = "onigiri.motion_hip_correction_end"
    bl_label = "Bad Frame"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        if motion.props["hip_start"] is None:
            return False
        return True


    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        try:
            frame_current = bpy.context.scene.frame_current
            frame_start = motion.props["hip_start"]
            armObj = bpy.context.selected_objects[0]
            # Hier könnte die eigentliche Korrekturlogik ergänzt werden
            print(f"Hip Correction End gesetzt: Rig={armObj.name}, Start-Frame={frame_start}, End-Frame={frame_current}")
            popup(f"Hip Correction End gesetzt: Frame {frame_current}", "Info", "INFO")
            # Properties zurücksetzen
            motion.props["hip_start"] = None
            motion.props["hip_end"] = None
            motion.props["hip_rig"] = None
            bpy.context.scene.frame_set(frame_start)
            return {"FINISHED"}
        except Exception as e:
            print(f"Fehler bei Hip Correction End: {e}")
            popup(f"Fehler bei Hip Correction End: {e}", "Fehler", "ERROR")
            return {"CANCELLED"}


class OnigiriMotionHipCorrectionReset(bpy.types.Operator):
    """Reset to start.  Choosing a different rig and setting a start/reference
    frame will reset the hip corrector to the new rig and frame.  This button will
    clear it out without doing that to start new"""

    bl_idname = "onigiri.motion_hip_correction_reset"
    bl_label = "Reset"


    def execute(self, context):
        try:
            motion.props["hip_start"] = None
            motion.props["hip_end"] = None
            motion.props["hip_rig"] = None
            print("Hip Correction Reset ausgeführt.")
            popup("Hip Correction wurde zurückgesetzt.", "Info", "INFO")
            return {"FINISHED"}
        except Exception as e:
            print(f"Fehler beim Hip Correction Reset: {e}")
            popup(f"Fehler beim Hip Correction Reset: {e}", "Fehler", "ERROR")
            return {"CANCELLED"}


class OnigiriMotionMapLoad(bpy.types.Operator, ImportHelper):
    """Load a map to use for your retargeting.  If one isn't available it's assumed
    that the target platform is Second Life.  This must be loaded onto the rig that
    contains the animation, not the target / actor"""

    bl_idname = "onigiri.motion_load_map"
    bl_label = "Load Map"

    filter_glob: bpy.props.StringProperty(
        default="*.ctm;*.ccm;*onim", options={"HIDDEN"}
    )

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion

        armObj = bpy.context.selected_objects[0]

        file_path = self.properties.filepath
        path, name = os.path.split(self.properties.filepath)
        file_prefix = name.split(".")[0]
        ext = name.split(".")[-1]

        try:
            namespace = {}
            exec(open(file_path, "r", encoding="UTF8").read(), namespace)
        except Exception as e:
            print(traceback.format_exc())
            return {"FINISHED"}

        template = {}
        for container in namespace:

            if container.startswith("__"):
                continue
            template[container] = namespace[container]

        template_map = template.get("template_map", {})
        rename_map = template.get("rename", {})

        if len(template_map) == 0 and len(rename_map) == 0:
            print("The map you loaded is unusable")
            popup("Unusable map", "Error", "ERROR")
            return {"FINISHED"}

        rename = {}
        bone_map = {}
        lock_map = {}

        if len(rename_map) != 0:
            print("Found CCM")
            for bone in rename_map:
                rename[bone] = rename_map[bone]
            armObj["oni_onemap_rename"] = rename
        elif len(template_map) != 0:
            print("Found CTM")
            for sbone in template_map:
                ((tarm, tbone),) = template_map[sbone].items()
                bone_map[tbone] = sbone
            armObj["oni_onemap_rename"] = bone_map

        if template.get("lock") is not None:
            lock_map = template["lock"]
            armObj["oni_onemap_lock"] = lock_map
            print("Lock map loaded!")

        rename_map = armObj["oni_onemap_rename"].to_dict()
        bad_bones = []
        good_bones = []
        for bone in rename_map:
            if bone not in armObj.data.bones:
                bad_bones.append(bone)
            else:
                good_bones.append(bone)
        if len(good_bones) == 0:
            print("There are no mappable bones in the loaded file")
            popup("The file does not match your rig", "Error", "ERROR")
            return {"FINISHED"}
        if len(bad_bones) > 0:
            print("Some bones didn't match your rig:")
            print(bad_bones)

        print("retarget map loaded")

        return {"FINISHED"}


class OnigiriMotionMapSave(bpy.types.Operator, ExportHelper):
    """Retarget maps do not honor reskin methods so be careful when saving this.
    If you intended to save a character converter map this is probably not the process
    you wanted.  This is for animations, a reskin map is not loaded or saved"""

    bl_idname = "onigiri.motion_save_map"
    bl_label = "Save map"

    filename_ext = ".onim"

    filter_glob: bpy.props.StringProperty(default="*.onim", options={"HIDDEN"})

    def invoke(self, context, event):
        load_path = script_dir + data_path
        self.filepath = load_path
        wm = context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        inRig = motion.get_director(o)
        if not inRig:
            return False
        if inRig.get("oni_onemap_rename") is None:
            return False
        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        inRig = bpy.context.selected_objects[0]

        armObj = motion.get_director(inRig)
        if not armObj:
            print("No director found for saving the map from")
            popup("No director found", "Error", "ERROR")
            return {"FINISHED"}

        file_path = self.properties.filepath
        path, name = os.path.split(self.properties.filepath)
        file_prefix = name.split(".")[0]
        ext = name.split(".")[-1]

        result = snap.save_map(input=armObj, file=self.filepath)
        if not result:
            print("Something weird happened when saving the map")
            popup("Something strange happened when saving", "Error", "ERROR")

        else:
            print("Map saved!")

        return {"FINISHED"}


class OnigiriMotionMatchMap(bpy.types.Operator):
    """This creates a map for you that will match your existing bones.  This is
    useful when you have an existing SL compatible rig that is animated and you are
    simply retargeting the animation, i.e. converted character"""

    bl_idname = "onigiri.motion_match_map"
    bl_label = "Match Map"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False

        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        armObj = bpy.context.selected_objects[0]
        rename_map = {}

        for boneObj in armObj.data.bones:
            bone = boneObj.name
            rename_map[bone] = bone

        armObj["oni_onemap_rename"] = rename_map

        print("Match map assigned!")

        return {"FINISHED"}


class OnigiriMotionMapClean(bpy.types.Operator):
    """Clean out the map"""

    bl_idname = "onigiri.motion_clean_map"
    bl_label = "Clean Map"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.get("oni_onemap_rename") is None:
            return False
        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion

        armObj = bpy.context.selected_objects[0]

        del armObj["oni_onemap_rename"]

        return {"FINISHED"}


class OnigiriMotionReset(bpy.types.Operator):
    """Reset the retargeter.  This will not remove your map"""

    bl_idname = "onigiri.motion_reset"
    bl_label = "Reset the retargeter"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False

        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        armObj = bpy.context.selected_objects[0]

        bpy.ops.object.mode_set(mode="OBJECT")
        utils.activate(armObj)

        inRig = motion.get_director(armObj, report=True)

        if inRig:

            print("Found director:", inRig.name)
            proxyRig = inRig.get("oni_motion_proxy")
            inRig.pop("oni_onemap_proxy", "")
            inRig.pop("oni_motion_proxy", "")

            inRig.show_in_front = inRig.pop("oni_show_in_front", True)

            if proxyRig is not None:
                if proxyRig.name in bpy.context.scene.objects:

                    print("Proxy rig found", proxyRig.name, "marking for deletion")
                    proxyRig.hide_set(False)
                    state = utils.get_state()
                    proxyRig.select_set(True)
                    bpy.ops.object.delete()
                    utils.purge_orphans()
                    utils.set_state(state)
            else:
                print("Missing proxy rig")

            stickyRig = inRig.get("oni_motion_stabilizer")
            inRig.pop("oni_motion_stabilizer", "")
            if stickyRig is not None:
                if stickyRig.name in bpy.context.scene.objects:
                    print("Sticky rig found", stickyRig.name, "marking for deletion")
                    stickyRig.hide_set(False)
                    stickyRig.select_set(True)
            else:
                print("Missing sticky rig")
            outRig = inRig["oni_motion_actor"]
            outRig.pop("oni_motion_director", "")

            if utils.is_valid(outRig):

                for o in bpy.context.selected_objects:
                    o.select_set(False)
                outRig.select_set(True)
                utils.activate(outRig)

                for boneObj in outRig.pose.bones:
                    for C in boneObj.constraints:
                        boneObj.constraints.remove(C)
            else:
                print("outRig missing:", outRig.name)

            selected = bpy.context.selected_objects
            if len(selected) > 0:
                o = bpy.context.selected_objects[0]
                if o == inRig:
                    o.select_set(False)
                    print(
                        "Something weird happened, the inRig was slated for deletion and this should never happen"
                    )

            bpy.ops.object.delete()
            inRig.pop("oni_motion_actor", "")
            inRig.pop("oni_motion_glue", "")

            for o in bpy.context.selected_objects:
                o.select_set(False)
            inRig.select_set(True)
            utils.activate(inRig)

        pop_items = [
            "oni_motion_actor",
            "oni_motion_director",
            "oni_motion_proxy",
            "oni_motion_stabilizer",
        ]
        for p in pop_items:
            armObj.pop(p, "")

        oni_motion["motion_target"] = False
        oni_motion.motion_target_name = ""

        oni_motion["motion_interactive_menu_enabled"] = False

        print("Motion reset")

        return {"FINISHED"}


class OnigiriMotionAction(bpy.types.Operator):
    """Start the retargeter.  Once engaged you can use (Interactive Retarget Mapping)
    to reassign bones"""

    bl_idname = "onigiri.motion_action"
    bl_label = "Start retargeting"

    report: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False

        if o.get("oni_motion_actor") is not None or o.get("oni_motion_director") is not None:
            return False
        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        inRig = bpy.context.selected_objects[0]

        state = utils.get_state()
        try:
            print("Resetting snap mapper just in case")
            bpy.ops.onigiri.snap_reset(report=False)
        except:
            print("snap mapper was not engaged")
        utils.set_state(state)

        rigutils.get_layer_state(inRig)

        if inRig.get("oni_onemap_rename") is None:
            inRig["oni_onemap_rename"] = {}

        if oni_motion.motion_glue:
            result = motion.retarget_hard(inRig)
            if not result:
                print("An error occurred when attempting to engage the retargeter")
                popup("There was an error, see console", "Error", "ERROR")
                return {"FINISHED"}

            inRig["oni_motion_glue"] = True
        else:
            result = motion.retarget_soft(inRig)
            if not result:
                print("An error occurred when attempting to engage the retargeter")
                popup("There was an error, see console", "Error", "ERROR")
                return {"FINISHED"}

        for o in bpy.context.selected_objects:
            o.select_set(False)
        outRig = inRig["oni_motion_actor"]

        if oni_motion.motion_to_animation:
            has_action = False
            if inRig.animation_data is not None:
                if inRig.animation_data.action is not None:
                    has_action = True
                    inRig.select_set(True)
                    utils.activate(inRig)
                    print("Running acquire_animation_details")
                    bpy.ops.onigiri.acquire_animation_details()
            if not has_action:
                print(
                    "No animation to transfer, you can still inherit motion but your time settings must be set manually"
                )

        motion.add_groups(inRig=inRig, outRig=outRig)

        result = motion.update_map(inRig=inRig)
        if not result:
            print(
                "motion update_map returned False, is this a Match Map and you forgot to tick Custom Target when not using an SL rig?"
            )
            bpy.ops.onigiri.motion_reset()
            return {"FINISHED"}

        rigutils.get_layer_state(outRig)

        inRig.select_set(False)
        outRig.select_set(True)
        utils.activate(outRig)

        inRig["oni_show_in_front"] = inRig.show_in_front

        rename_map = inRig["oni_onemap_rename"]
        for sbone in rename_map.keys():
            tbone = rename_map[sbone]
            if tbone in outRig.data.bones:
                outRig.data.bones[tbone].hide = False

        if inRig.get("oni_onemap_lock") is not None:
            lock_map = inRig["oni_onemap_lock"].to_dict()
            for bone in lock_map:
                if bone not in outRig.data.bones:

                    print("lock bone not in outRig:", bone)

                    continue
                boneObj = outRig.pose.bones[bone]
                for conObj in boneObj.constraints:
                    transform = conObj.type
                    if transform not in lock_map[bone]["constraints"]:

                        print("constraint missing:", transform)

                        continue
                    conObj.owner_space = lock_map[bone]["constraints"][transform][
                        "owner_space"
                    ]
                    conObj.target_space = lock_map[bone]["constraints"][transform][
                        "target_space"
                    ]
                    conObj.influence = lock_map[bone]["constraints"][transform][
                        "influence"
                    ]
            print("Locks engaged!")

        state = utils.get_state()
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=0.1, enter_editmode=False, align="WORLD", location=(0, 0, 0)
        )
        shapeObj = context.object

        blender3 = False

        for boneObj in outRig.pose.bones:
            dBone = boneObj.bone
            scale = dBone.length / 2
            boneObj.custom_shape = shapeObj
            boneObj.use_custom_shape_bone_size = True

            try:
                boneObj.custom_shape_scale = 0.5

            except:
                blender3 = True
                boneObj.custom_shape_scale_xyz = (0.5, 0.5, 0.05)

        if blender3:
            print("Detected Blender 3 and adjusted property for custom shape scale")

        outRig.data.show_bone_custom_shapes = oni_motion.motion_use_shapes

        shapeObj.select_set(True)
        utils.activate(shapeObj)
        bpy.ops.object.delete()

        print("Toggling map updater 668")
        motion.update_map(inRig=inRig)

        utils.set_state(state)

        print("Motion Action Engaged!")

        return {"FINISHED"}


class OnigiriMotionAnchor(bpy.types.Operator):
    """Control the location and rotation influence of the root/hip/pelvis, this is
    a toggle switch"""

    axis: bpy.props.StringProperty(default="")
    transform: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.motion_anchor"
    bl_label = "Load Map"

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        if len(bpy.context.selected_objects) == 0:
            print("Nothing to do without a set")
            return {"FINISHED"}
        armObj = bpy.context.selected_objects[0]
        inRig = motion.get_director(armObj)
        if not inRig:
            print("Nothing to do without a set")
            return {"FINISHED"}
        outRig = inRig["oni_motion_actor"]

        if self.axis == "x":
            axis = "use_x"
        elif self.axis == "y":
            axis = "use_y"
        elif self.axis == "z":
            axis = "use_z"
        if self.transform == "rotation":
            transform = "COPY_ROTATION"
        elif self.transform == "location":
            transform = "COPY_LOCATION"

        boneObj = outRig.pose.bones[0]
        for C in boneObj.constraints:
            if C.type == transform:
                state = getattr(C, axis)
                state = not state
                setattr(C, axis, state)

        return {"FINISHED"}


class OnigiriMotionMesh(bpy.types.Operator):
    """Hide or show the mesh associated with the rigs"""

    bl_idname = "onigiri.motion_mesh"
    bl_label = "Mesh Visibility"

    action: bpy.props.StringProperty(default="")

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False

        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        armObj = bpy.context.selected_objects[0]

        state = False
        if self.action == "hide":
            state = True

        inRig = motion.get_director(armObj)
        if inRig:
            mesh = inRig.children
            for m in mesh:
                if m.type == "MESH":
                    m.hide_set(state)
        mesh = armObj.children
        for m in mesh:
            if m.type == "MESH":
                m.hide_set(state)

        return {"FINISHED"}


class OnigiriMotionViewBones(bpy.types.Operator):
    """Show / Hide mapped bones"""

    bl_idname = "onigiri.motion_view_bones"
    bl_label = "View or Hide bones"

    action: bpy.props.StringProperty(default="")

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        if bpy.context.selected_objects[0].type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        oni_motion = bpy.context.window_manager.oni_motion
        inRig = motion.get_director(bpy.context.selected_objects[0].name)
        if not inRig:
            print("The Director rig is not available")
            return {"FINISHED"}
        outRig = inRig["oni_motion_actor"]

        rename_map = inRig.get("oni_onemap_rename")

        rigutils.get_layer_state(outRig)

        if self.action == "show":
            for boneObj in outRig.data.bones:
                boneObj.hide = False
        else:
            if rename_map is None:
                print("No map is available")
                return {"FINISHED"}

            rename_rev = {}
            for bone in rename_map.keys():
                sbone = rename_map[bone]
                rename_rev[sbone] = bone

            for boneObj in outRig.data.bones:
                if boneObj.name not in rename_rev:
                    boneObj.hide = True

        return {"FINISHED"}


class OnigiriMotionHideTarget(bpy.types.Operator):
    """Hides all of the bones in the target, giving you an easier tim selecting
    bones in the animation source rig in case you need to arrange for some of them
    to be locked or unlocked, use (View All Bones) to revert"""

    bl_idname = "onigiri.motion_hide_target"
    bl_label = "Hide target bones"

    def execute(self, context):
        armObj = bpy.context.selected_objects[0]
        inRig = motion.get_director(armObj)
        if not inRig:
            print("No director present")
            return {"FINISHED"}
        outRig = inRig["oni_motion_actor"]

        for boneObj in outRig.data.bones:
            boneObj.hide = True

        return {"FINISHED"}


class OnigiriMotionMapAdd(bpy.types.Operator):
    """Add the chosen bones to the map"""

    bl_idname = "onigiri.motion_map_add"
    bl_label = "Map bones"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        inRig = motion.get_director(o)
        if not inRig:
            return False
        return True

    def execute(self, context):

        in_bone = motion.props["director_bone"]
        out_bone = motion.props["actor_bone"]
        if in_bone == "" or out_bone == "":
            print("Nothing to do, slots are not full yet")
            return {"FINISHED"}

        inRig = bpy.context.selected_objects[0]

        if inRig.get("oni_onemap_rename") is None:
            inRig["oni_onemap_rename"] = {}
        outRig = inRig["oni_motion_actor"]

        actor_bones = []
        director_bones = []

        rename_map = inRig["oni_onemap_rename"]

        rename_rev = {}
        for sbone in rename_map:
            tbone = rename_map[sbone]
            rename_rev[tbone] = sbone
        if out_bone in rename_rev:
            sbone = rename_rev[out_bone]
            rename_map.pop(sbone, "")

        if in_bone in rename_map:
            tbone = rename_map[in_bone]
            if tbone in rename_rev:
                sbone = rename_rev[tbone]
                rename_map.pop(sbone, "")

        rename_map[in_bone] = out_bone

        motion.update_map(inRig=inRig)

        props["director_bone"] = ""
        props["actor_bone"] = ""

        return {"FINISHED"}


class OnigiriMotionMapRemove(bpy.types.Operator):
    """Remove selected bones from the map"""

    bl_idname = "onigiri.motion_map_remove"
    bl_label = "Remove bones"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        inRig = motion.get_director(o)
        if not inRig:
            return False
        return True

    def execute(self, context):
        inRig = bpy.context.selected_objects[0]

        if inRig.get("oni_onemap_rename") is None:
            inRig["oni_onemap_rename"] = {}

        rename_map = inRig["oni_onemap_rename"]
        outRig = inRig["oni_motion_actor"]

        directors = []
        actors = []
        for boneObj in bpy.context.selected_pose_bones:
            if boneObj.id_data == inRig:
                directors.append(boneObj.name)
            elif boneObj.id_data == outRig:
                actors.append(boneObj.name)
            else:
                print(
                    "Got an included bone that doesn't match the rigs, [bone/rig]:",
                    boneObj.name,
                    boneObj.id_data.name,
                )

        rename_map = inRig["oni_onemap_rename"]
        for bone in directors:
            rename_map.pop(bone, "")
        rename_map_rev = {}
        for sbone in rename_map:
            tbone = rename_map[sbone]
            rename_map_rev[tbone] = sbone
        for bone in actors:
            if bone in rename_map_rev:
                sbone = rename_map_rev[bone]
                rename_map.pop(sbone, "")

        inRig["oni_onemap_rename"] = rename_map

        motion.update_map(inRig=inRig)

        for boneObj in inRig.data.bones:
            boneObj.select = False
        for boneObj in outRig.data.bones:
            boneObj.select = False

        motion.props["actor_bone"] = ""
        motion.props["director_bone"] = ""

        return {"FINISHED"}


class OnigiriMotionMapSelect(bpy.types.Operator):
    """You can select the bone indicated here by clicking this button"""

    bl_idname = "onigiri.motion_map_select"
    bl_label = "Select bones"

    in_bone: bpy.props.StringProperty(default="")
    out_bone: bpy.props.StringProperty(default="")

    def execute(self, context):
        inRig = bpy.context.selected_objects[0]

        if inRig.get("oni_onemap_rename") is None:
            inRig["oni_onemap_rename"] = {}

        rename_map = inRig["oni_onemap_rename"]
        outRig = inRig["oni_motion_actor"]

        if self.in_bone != "":
            inRig.data.bones[self.in_bone].select = True
        if self.out_bone != "":
            outRig.data.bones[self.out_bone].select = True

        return {"FINISHED"}


class OnigiriMotionLockSelected(bpy.types.Operator):
    """Lock / Unlock the transform type of the selected bones.  This allows you to mix
    location influences of absolute and relative types with rotation data.  One use for this
    is when you are using extra/unused bones in a non-custom character"""

    bl_idname = "onigiri.motion_lock_selected"
    bl_label = "Lock / Unlock Selected"

    action: bpy.props.StringProperty(default="")
    transform: bpy.props.StringProperty(default="")

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        inRig = motion.get_director(o)
        if not inRig:
            return False
        if inRig.get("oni_onemap_rename") is None:
            return False
        if len(bpy.context.selected_pose_bones) == 0:
            return False
        return True

    def execute(self, context):
        print("Transform:", self.transform)
        print("Action:", self.action)

        armObj = bpy.context.selected_objects[0]
        inRig = motion.get_director(armObj)

        if not inRig:
            print("Couldn't find the director")
            popup("No actor/director association", "Error", "ERROR")
            return {"FINISHED"}

        if inRig.get("oni_onemap_rename") is None:
            print(
                "No map available, this tool needs a map in order to enable the transforms"
            )
            popup("No map avaialble, see console", "No map", "INFO")
            return {"FINISHED"}

        if inRig.get("oni_onemap_rename") is None:
            inRig["oni_onemap_rename"] = {}
        outRig = inRig["oni_motion_actor"]
        rename_map = inRig["oni_onemap_rename"]

        if self.action == "lock":
            transform_state = True
            transform_space = "WORLD"
        else:
            transform_state = False
            transform_space = "LOCAL_WITH_PARENT"

        if self.transform == "rotation":
            transform_type = "COPY_ROTATION"
        elif self.transform == "location":
            transform_type = "COPY_LOCATION"
        else:
            print("Unknown transform type:", self.transform)
            return {"FINISHED"}

        rename_rev = {}
        for sbone in rename_map:
            tbone = rename_map[sbone]
            rename_rev[tbone] = sbone

        bones_list = []
        for boneObj in bpy.context.selected_pose_bones:
            bone = boneObj.name
            if boneObj.id_data == outRig:
                if bone in rename_rev:
                    bones_list.append(boneObj)
            if boneObj.id_data == inRig:
                if bone in rename_map:
                    tbone = rename_map[bone]

                    if tbone in outRig.data.bones:
                        bones_list.append(outRig.pose.bones[tbone])
        if len(bones_list) == 0:
            print(
                "After filtering selected bones there were none left to process, is the map compatible?"
            )
            popup("No actor bones were chosen, see console", "Error", "ERROR")
            return {"FINISHED"}

        for boneObj in bones_list:

            for conObj in boneObj.constraints:
                if conObj.type == transform_type:
                    if conObj.target:
                        conObj.influence = transform_state
                        conObj.owner_space = transform_space
                        conObj.target_space = transform_space

        lock_map = {}
        for boneObj in outRig.pose.bones:
            bone = boneObj.name
            for conObj in boneObj.constraints:
                if conObj.type == "COPY_ROTATION":
                    transform = "COPY_ROTATION"
                elif conObj.type == "COPY_LOCATION":
                    transform = "COPY_LOCATION"
                elif conObj.type == "COPY_TRANSFORMS":
                    transform = "COPY_TRANSFORMS"
                else:
                    continue
                influence = conObj.influence
                owner_space = conObj.owner_space
                target_space = conObj.target_space
                if bone not in lock_map:
                    lock_map[bone] = {}
                if "constraints" not in lock_map[bone]:
                    lock_map[bone]["constraints"] = {}
                lock_map[bone]["constraints"][transform] = {}
                lock_map[bone]["constraints"][transform]["owner_space"] = owner_space
                lock_map[bone]["constraints"][transform]["target_space"] = target_space
                lock_map[bone]["constraints"][transform]["influence"] = influence

        inRig["oni_onemap_lock"] = lock_map

        return {"FINISHED"}


class OnigiriMotionLockRemove(bpy.types.Operator):
    """NOTE: HIT THIS BUTTON NOW, IT'S SAFE!  This feature was not well documented
    and can cause issues. : This removes the lock map on the director and prevent the bones
    from utilizing it on the next retarget (Action!)"""

    bl_idname = "onigiri.motion_remove_lock"
    bl_label = "Remove Lock Map"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        armObj = bpy.context.selected_objects[0]
        inRig = motion.get_director(armObj)

        if not inRig:
            print("Couldn't find the director, will cleanup existing rig instead...")
            if armObj.get("oni_onemap_lock") is not None:
                del armObj["oni_onemap_lock"]
                print("Lock map removed from selected rig!")
            else:
                print("No lock map found on the selected rig")
            return {"FINISHED"}
        else:
            if inRig.get("oni_onemap_lock") is None:
                print("No lock map existed on the director")
            else:
                inRig.pop("oni_onemap_lock")
                print("Lock map removed from director!")

        return {"FINISHED"}


class OnigiriMotionApplyScale(bpy.types.Operator):
    """Apply scale to the Actor rig.  This is designed to only work with the actor for
    a reason, you don't want to do this to an animated Director, use the clean tool for that
    """

    bl_idname = "onigiri.motion_apply_scale"
    bl_label = "Apply Scale"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 0:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        armObj = bpy.context.selected_objects[0]
        inRig = motion.get_director(armObj)

        if not inRig:
            print("Couldn't find the director")
            popup("No director found", "Error", "ERROR")
            return {"FINISHED"}

        if inRig.get("oni_motion_actor") is None:
            print("not an actor")
            popup("Not an actor", "Error", "ERROR")
            return {"FINISHED"}
        outRig = inRig["oni_motion_actor"]
        state = utils.get_state()
        outRig.select_set(True)
        utils.activate(outRig)

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        utils.set_state(state)

        return {"FINISHED"}


class OnigiriMotionMixerProperties(bpy.types.PropertyGroup):

    def update_mixer_cleanup(self, context):
        if oni_settings["terminate"]:
            oni_settings["terminate"] = False
            return
        oni_mixer = bpy.context.window_manager.oni_mixer
        oni_settings["terminate"] = True
        oni_mixer.mixer_cleanup = False

        print("mixer_cleanup")
        tObj = oni_mixer.get("target")
        if tObj:
            if tObj.name not in bpy.context.scene.objects:
                bpy.data.objects.remove(tObj)

        targetObj = oni_mixer.pop("target", None)
        sources = oni_mixer.pop("sources", None)

        maps = oni_mixer.pop("maps", "")
        oni_mixer.mixer_target_name = ""
        oni_mixer.mixer_anchor_name = ""
        oni_mixer.mixer_active_rig_name = ""
        oni_mixer.property_unset("mixer_ready")
        oni_mixer.property_unset("mixer_target_locked")

        old_mode = bpy.context.mode
        if old_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        for o in bpy.context.selected_objects:
            o.select_set(False)
        if targetObj:
            targetObj.select_set(True)
            print("Bone groups reset")

            bpy.context.view_layer.objects.active = targetObj
            for g in targetObj.data.collections:
                targetObj.data.collections.remove(g)
            for boneObj in targetObj.pose.bones:
                constraints = boneObj.constraints
                for c in constraints:
                    boneObj.constraints.remove(c)
        if sources:
            for o in sources:
                for g in o.data.collections:
                    o.data.collections.remove(g)

        return

    def update_mixer_target_locked(self, context):
        if oni_settings["terminate"]:
            oni_settings["terminate"] = False
            return
        oni_mixer = bpy.context.window_manager.oni_mixer
        if oni_mixer.mixer_target_locked:
            print("Mixer target:", bpy.context.selected_objects[0].name)
        else:

            oni_mixer.mixer_cleanup = True

        return

    mixer_menu_enabled: bpy.props.BoolProperty(
        name="", description="Open the animation mixer", default=False
    )
    mixer_target_locked: bpy.props.BoolProperty(
        name="",
        description="This shows that your target is enabled and you're now ready to choose sources",
        default=False,
        update=update_mixer_target_locked,
    )
    mixer_target_name: bpy.props.StringProperty(
        name="",
        description="-- internal, target name",
        default=" ",
    )

    mixer_cleanup: bpy.props.BoolProperty(
        name="", description="--internal", default=False, update=update_mixer_cleanup
    )

    def update_mixer_transform_info(self, context):
        bpy.context.window_manager.oni_mixer.property_unset("mixer_transform_info")
        return

    mixer_transform_info: bpy.props.BoolProperty(
        name="",
        description="This button is informative only"
        "\n\n"
        "Location, Rotation and Scale are initial settings when you add bones to the mixer.  Scale data cannot be used in SL, yet, "
        "and we're not aware of any plans that will allow for that but the feature is here for future growth.  Rotation and Location "
        "are the focus for Second Life with (Location) being the least used so the default here is (Rotation) only.  However, the "
        "versatile utility of Onigiri does allow for location data to be used in animations with your BVH and anim exports and "
        "is usually required when you auto-map a custom character.  You can tick the feature off per bone for testing it out and "
        "watching the viewport.",
        default=False,
        update=update_mixer_transform_info,
    )

    mixer_location: bpy.props.BoolProperty(
        name="",
        description="Enable location transform influence as a default for new bone additions",
        default=False,
    )
    mixer_rotation: bpy.props.BoolProperty(
        name="",
        description="Enable rotation transform influence as a default for new bone additions",
        default=True,
    )
    mixer_scale: bpy.props.BoolProperty(
        name="",
        description="Enable scale transform influence as a default for new bone additions (no recommended)",
        default=False,
    )

    def update_mixer_anchor(self, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if not oni_mixer.mixer_anchor:
            obj = bpy.data.objects
            source = oni_mixer.mixer_anchor_name
            oni_mixer.mixer_anchor_name = ""

            for boneObj in bpy.context.selected_pose_bones:
                dBone = boneObj.bone
                dBone.select = False
            armObj = obj[source]
            bpy.context.view_layer.objects.active = armObj
            armObj.data.bones["mPelvis"].select = True
            bpy.ops.onigiri.mixer_remove_bones()
            oni_mixer.property_unset("mixer_anchor")
            print("Removed anchor from", source)
        return

    mixer_anchor: bpy.props.BoolProperty(
        name="",
        description="Disable this anchor",
        default=True,
        update=update_mixer_anchor,
    )
    mixer_anchor_name: bpy.props.StringProperty(
        name="",
        description="--internal name for the anchor",
        default="",
    )

    def update_mixer_active_rig(self, context):
        oni_mixer = bpy.context.window_manager.oni_mixer
        oni_mixer.mixer_active_rig_name = ""
        oni_mixer.property_unset("mixer_active_rig")
        return

    mixer_active_rig: bpy.props.BoolProperty(
        name="",
        description="Click to close the list or click another rig name to swap views.",
        default=False,
        update=update_mixer_active_rig,
    )
    mixer_active_rig_name: bpy.props.StringProperty(
        name="",
        description="--internal, holds the name of the active rig showing a list of associated bones that influence the target",
        default="",
    )

    def update_mixer_ready(self, context):

        oni_mixer = bpy.context.window_manager.oni_mixer
        if oni_mixer.mixer_ready:
            return
        old_mode = bpy.context.mode
        if old_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        for o in bpy.context.selected_objects:
            o.select_set(False)
        return

    mixer_ready: bpy.props.BoolProperty(
        name="",
        description="Click to suspend (ready) mode if you need to choose more rigs or remove existing ones.",
        default=False,
        update=update_mixer_ready,
    )

    def update_mixer_location_set(self, context):

        oni_mixer = bpy.context.window_manager.oni_mixer
        if not oni_mixer.mixer_location_set:
            bone = globals.oni_mixer["bone_location_set"]
            globals.oni_mixer["constraints"][bone]["location"].influence = 0
            oni_mixer.property_unset("mixer_location_set")

            if bone == "mPelvis":
                print("Disabled anchor")
                oni_mixer.mixer_anchor_name = ""
            print("L bone:", bone)
            print("active bone name:", oni_mixer.mixer_active_bone_name)
        return

    def update_mixer_rotation_set(self, context):
        oni_mixer = bpy.context.window_manager.oni_mixer
        if not oni_mixer.mixer_rotation_set:
            bone = globals.oni_mixer["bone_rotation_set"]
            globals.oni_mixer["constraints"][bone]["rotation"].influence = 0
            oni_mixer.property_unset("mixer_rotation_set")
            print("R bone:", bone)
            print("active bone name:", oni_mixer.mixer_active_bone_name)
        return

    def update_mixer_scale_set(self, context):
        oni_mixer = bpy.context.window_manager.oni_mixer
        if not oni_mixer.mixer_scale_set:
            bone = globals.oni_mixer["bone_scale_set"]
            globals.oni_mixer["constraints"][bone]["scale"].influence = 0
            oni_mixer.property_unset("mixer_scale_set")
            print("S bone:", bone)
            print("active bone name:", oni_mixer.mixer_active_bone_name)
        return

    mixer_location_set: bpy.props.BoolProperty(
        name="",
        description="Click this to disable the position influence for this bone",
        default=True,
        update=update_mixer_location_set,
    )
    mixer_rotation_set: bpy.props.BoolProperty(
        name="",
        description="Click this to disable the rotation influence for this bone",
        default=True,
        update=update_mixer_rotation_set,
    )
    mixer_scale_set: bpy.props.BoolProperty(
        name="",
        description="Click this to disable the scale influence for this bone",
        default=True,
        update=update_mixer_scale_set,
    )
    mixer_active_bone_name: bpy.props.StringProperty(
        name="",
        description="-internal",
        default="",
    )


class OnigiriMotionMixerLockTarget(bpy.types.Operator):
    """Add the main target rig, this is the armature that will receive all of the
    motion from your animated source rigs.  These must all be Onigiri rigs so
    retarget your animations first then motion mix with this tool"""

    bl_idname = "onigiri.mixer_lock_target"
    bl_label = "Lock the target armature"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) == 1:
            if bpy.context.selected_objects[0].type == "ARMATURE":
                if bpy.context.selected_objects[0].get("onigiri") is not None:
                    return True
        return False

    def execute(self, context):
        oni_mixer = bpy.context.window_manager.oni_mixer
        targetObj = bpy.context.selected_objects[0]
        oni_mixer.mixer_target_locked = True
        oni_mixer.mixer_target_name = targetObj.name
        oni_mixer["target"] = targetObj

        old_mode = bpy.context.mode
        if old_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        if old_mode.startswith("EDIT"):
            old_mode = "EDIT"

        bpy.context.view_layer.objects.active = targetObj
        bpy.ops.object.mode_set(mode="OBJECT")

        for g in targetObj.data.collections:
            targetObj.data.collections.remove(g)

        bpy.ops.object.mode_set(mode="POSE")

        inactiveCollection = targetObj.data.collections.new(mixer_group_target_inactive_name)

        targetObj.data.collections.new(mixer_group_target_active_name)
        #targetObj.data.collections.active.color_set = mixer_group_target_active_theme

        for boneObj in targetObj.pose.bones:
            inactiveCollection.assign(boneObj)
            boneObj.color.palette = mixer_group_target_inactive_theme

        bpy.ops.object.mode_set(mode="OBJECT")

        rigutils.remove_deps(armature=targetObj.name)

        for boneObj in targetObj.pose.bones:

            if 1 == 1:
                bone = boneObj.name

                print("targetObj.name / boneObj.name:", targetObj.name, boneObj.name)

                targetObj.data.bones.active = targetObj.data.bones[bone]
                bc = boneObj.constraints
                bc.new("COPY_LOCATION")

                bc["Copy Location"].target_space = "LOCAL"
                bc["Copy Location"].owner_space = "LOCAL"
                bc["Copy Location"].influence = 0
                globals.oni_mixer["constraints"][bone]["location"] = bc["Copy Location"]
                bc["Copy Location"].name = "ONI Copy Location"

                bc = boneObj.constraints
                bc.new("COPY_ROTATION")

                bc["Copy Rotation"].target_space = "LOCAL"
                bc["Copy Rotation"].owner_space = "LOCAL"
                bc["Copy Rotation"].influence = 0
                globals.oni_mixer["constraints"][bone]["rotation"] = bc["Copy Rotation"]
                bc["Copy Rotation"].name = "ONI Copy Rotation"

                bc = boneObj.constraints
                bc.new("COPY_SCALE")

                bc["Copy Scale"].target_space = "LOCAL"
                bc["Copy Scale"].owner_space = "LOCAL"
                bc["Copy Scale"].influence = 0
                globals.oni_mixer["constraints"][bone]["scale"] = bc["Copy Scale"]
                bc["Copy Scale"].name = "ONI Copy Scale"
            else:
                bone = boneObj.name
                targetObj.data.bones.active = targetObj.data.bones[bone]
                bc = boneObj.constraints
                bc.new("CHILD_OF")
                conObj = bc.new(constraint)
                cname = conObj.name
                conObj.target = targetObj

                conObj.target_space = "LOCAL"
                conObj.owner_space = "LOCAL"
                conObj.influence = 0
                if constraint == "CHILD_OF":
                    context_py = bpy.context.copy()
                    context_py["constraint"] = bc.active
                    utils.set_inverse(context_py, cname)

                globals.oni_mixer["constraints"][bone]["child_of"] = conObj["Child Of"]
                conObj.name = "ONI " + cname

        return {"FINISHED"}


class OnigiriMotionMixerAddSource(bpy.types.Operator):
    """Add an animated source rig, it must be a Onigiri rig.  You can get these
    sources by retargeting existing animated sources or creating your own, possibly
    loading them onto a rig from the action library or baking from the animation lib"""

    bl_idname = "onigiri.mixer_add_source"
    bl_label = "Add an animated source rig"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if oni_mixer.mixer_ready:
            return False

        if len(bpy.context.selected_objects) == 0:
            return False

        for o in bpy.context.selected_objects:
            if o.type == "ARMATURE":
                if o.get("onigiri") is not None:

                    if oni_mixer.get("target") != o:
                        return True
        return False

    def execute(self, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        selected = [o for o in bpy.context.selected_objects]

        old_mode = bpy.context.mode
        if old_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        if old_mode.startswith("EDIT"):
            old_mode = "EDIT"

        for o in selected:
            o.select_set(False)

        candidates = []
        for o in selected:
            if o.type == "ARMATURE":
                if o.get("onigiri") is not None:
                    if oni_mixer["target"] != o:
                        candidates.append(o)
                    else:
                        print("Target in source selection, skipping:", o.name)

        sources = oni_mixer.get("sources", [])

        verified = []
        for sourceObj in candidates:
            if sourceObj not in sources:
                sources.append(sourceObj)
                verified.append(sourceObj)
            else:
                print("Source already recorded:", sourceObj.name)

            oni_mixer["sources"] = sources

        for sourceObj in verified:

            print("Verified source is:", sourceObj.name)

            sourceObj.select_set(True)
            bpy.context.view_layer.objects.active = sourceObj
            for g in sourceObj.data.collections:
                sourceObj.data.collections.remove(g)

            bpy.ops.object.mode_set(mode="POSE")

            sourceObj.data.collections.new(mixer_group_source_inactive_name)
            sourceObj.data.collections.new(mixer_group_source_active_name)


            for boneObj in sourceObj.data.bones:
                sourceObj.data.collections[mixer_group_source_inactive_name].assign(boneObj)
                boneObj.color.palette = mixer_group_source_inactive_theme

            bpy.ops.object.mode_set(mode="OBJECT")
            sourceObj.select_set(False)

        bpy.ops.object.mode_set(mode=old_mode)

        return {"FINISHED"}


class OnigiriMotionMixerRemoveSource(bpy.types.Operator):
    """Remove a source rig from the list of influences"""

    name: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_remove_source"
    bl_label = "Remove a source rig"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if oni_mixer.mixer_ready:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        if self.name not in obj:
            print("Something strange happened, the object is not in the scene.")

        if oni_mixer.get("maps") is None:
            oni_mixer["maps"] = {}
        if oni_mixer["maps"].get("sources") is None:
            oni_mixer["maps"]["sources"] = {}

        sources = []
        for sourceObj in oni_mixer["sources"]:
            if sourceObj.name == self.name:
                continue
            sources.append(sourceObj)

        if len(sources) == 0:
            oni_mixer.pop("sources", [])
        else:
            oni_mixer["sources"] = sources

        old_mode = bpy.context.mode
        if old_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        if old_mode.startswith("EDIT"):
            old_mode = "EDIT"

        for o in bpy.context.selected_objects:
            o.select_set(False)

        sourceObj = obj[self.name]
        sourceObj.select_set(True)
        bpy.context.view_layer.objects.active = sourceObj

        for g in sourceObj.data.collections:
            sourceObj.data.collections.remove(g)

        targetObj = oni_mixer["target"]
        target = targetObj.name

        sources = oni_mixer["maps"]["sources"].get(self.name, [])

        for bone in sources:
            targetObj.data.collections[mixer_group_target_inactive_name].assign(bone)
            bone.color.palette = mixer_group_target_active_theme

            constraints = targetObj.pose.bones[bone].constraints
            for c in constraints:
                if c.type == "COPY_LOCATION":
                    c.target = None
                    targetObj.pose.bones[bone].constraints[c.name].influence = 0
                if c.type == "COPY_ROTATION":
                    c.target = None
                    targetObj.pose.bones[bone].constraints[c.name].influence = 0
                if c.type == "COPY_SCALE":
                    c.target = None
                    targetObj.pose.bones[bone].constraints[c.name].influence = 0

        oni_mixer["maps"]["sources"].pop(self.name, "")

        return {"FINISHED"}


class OnigiriMotionMixerReady(bpy.types.Operator):
    """Click this when you're ready to start picking influence bones.  The resulting
    state will also allow you to click it again when you need to add or remove rigs
    from/to the influences."""

    bl_idname = "onigiri.mixer_ready"
    bl_label = "Enable this to start picking bones"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if oni_mixer.get("target") is None:
            return False
        sources = oni_mixer.get("sources", [])
        if len(sources) == 0:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        old_mode = bpy.context.mode
        if old_mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        if old_mode.startswith("EDIT"):
            old_mode = "EDIT"

        for o in bpy.context.selected_objects:
            o.select_set(False)
        targetObj = oni_mixer["target"]
        sources = oni_mixer["sources"]
        for o in sources:
            o.select_set(True)
        targetObj.select_set(True)
        bpy.context.view_layer.objects.active = targetObj
        bpy.ops.object.mode_set(mode="POSE")
        oni_mixer.mixer_ready = True

        print("Mixer enabled")

        return {"FINISHED"}


class OnigiriMotionMixerActiveRigName(bpy.types.Operator):
    """Click to show the associated bone list"""

    name: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_active_rig_name"
    bl_label = "Activate bone list"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if not oni_mixer.mixer_ready:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        if oni_mixer.get("maps") is None:
            oni_mixer["maps"] = {}
        if oni_mixer["maps"].get("sources") is None:
            oni_mixer["maps"]["sources"] = {}

        oni_mixer.mixer_active_rig_name = self.name

        return {"FINISHED"}


class OnigiriMotionMixerSetAnchor(bpy.types.Operator):
    """Set the anchor rig, this allows location data on the pelvis, which is
    usually what you want so that one of your source rigs controls the pelvis/hip
    location of the target rig"""

    name: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_set_anchor"
    bl_label = "Set anchor for this rig\n"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if not oni_mixer.mixer_ready:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        bone = "mPelvis"

        if oni_mixer.get("maps") is None:
            oni_mixer["maps"] = {}
        if oni_mixer["maps"].get("sources") is None:
            oni_mixer["maps"]["sources"] = {}

        for sourceObj in oni_mixer["sources"]:
            sourceObj.data.collections[mixer_group_source_inactive_name].assign(sourceObj.pose.bones[bone])

        bone_dict = None
        for rig in oni_mixer["maps"]["sources"]:
            bone_dict = oni_mixer["maps"]["sources"][rig].pop(bone, None)

        rotation = 1
        scale = 0
        if bone_dict is not None:
            rotation = bone_dict["transforms"]["rotation"]
            scale = bone_dict["transforms"]["scale"]

        if self.name not in oni_mixer["maps"]["sources"]:
            oni_mixer["maps"]["sources"][self.name] = {}

        oni_mixer["maps"]["sources"][self.name][bone] = {}
        oni_mixer["maps"]["sources"][self.name][bone]["transforms"] = {
            "location": 1,
            "rotation": rotation,
            "scale": scale,
        }

        targetObj = oni_mixer["target"]
        sourceObj = obj[self.name]

        targetObj.data.collections[mixer_group_source_active_name].assign(targetObj.pose.bones[bone])
        targetObj.pose.bones[bone].color.palette = mixer_group_source_active_theme

        obj[self.name].data.collections[mixer_group_source_active_name].assign(obj[self.name].pose.bones[bone])

        constraints = targetObj.pose.bones[bone].constraints
        for c in constraints:
            if c.type == "COPY_LOCATION":
                c.target = obj[self.name]
                c.subtarget = bone
                targetObj.pose.bones[bone].constraints[c.name].target_space = (
                    motion.props["target_space"]
                )
                targetObj.pose.bones[bone].constraints[c.name].owner_space = (
                    motion.props["owner_space_anchor"]
                )

                targetObj.pose.bones[bone].constraints[c.name].influence = 1
            if c.type == "COPY_ROTATION":
                c.target = obj[self.name]
                c.subtarget = bone
                targetObj.pose.bones[bone].constraints[c.name].target_space = (
                    motion.props["target_space"]
                )
                targetObj.pose.bones[bone].constraints[c.name].owner_space = (
                    motion.props["owner_space_anchor"]
                )
                targetObj.pose.bones[bone].constraints[c.name].mix_mode = motion.props[
                    "mix_mode_anchor"
                ]
                targetObj.pose.bones[bone].constraints[c.name].influence = rotation
            if c.type == "COPY_SCALE":
                c.target = obj[self.name]
                c.subtarget = bone
                targetObj.pose.bones[bone].constraints[c.name].target_space = (
                    motion.props["target_space_anchor"]
                )
                targetObj.pose.bones[bone].constraints[c.name].owner_space = (
                    motion.props["owner_space_anchor"]
                )

                targetObj.pose.bones[bone].constraints[c.name].influence = scale

        oni_mixer.mixer_anchor_name = self.name

        return {"FINISHED"}


class OnigiriMotionMixerMode(bpy.types.Operator):
    """Sets the order of priority for motion.  This effects the selected bones.
    There is no feed back for flags to show.  If your motion is weird use this on
    parent bones first to test out it effects the indicated bone motion"""

    action: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_mode"
    bl_label = "Mix Mode\n"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if not oni_mixer.mixer_ready:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        bones = set([b.name for b in bpy.context.selected_pose_bones])

        if len(bones) == 0:
            print("No bones selected")
            return {"FINISHED"}

        targetObj = oni_mixer["target"]
        target = targetObj.name

        for bone in bones:
            boneObj = targetObj.pose.bones[bone]
            for C in boneObj.constraints:
                if C.type == motion.props["rotation_controller"]:
                    C.mix_mode = self.action

        return {"FINISHED"}


class OnigiriMotionMixerSpace(bpy.types.Operator):
    """This is a type of inheritance.  If your bones are not reflecting what you
    expect then try different types of target and owner space.  This, like the (mix)
    type, are advanced features and are here for convenience"""

    action: bpy.props.StringProperty(default="")
    space: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_space"
    bl_label = "Target / Owner space\n"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if not oni_mixer.mixer_ready:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        bones = set([b.name for b in bpy.context.selected_pose_bones])

        if len(bones) == 0:
            print("No bones selected")
            return {"FINISHED"}

        targetObj = oni_mixer["target"]
        target = targetObj.name

        for bone in bones:
            boneObj = targetObj.pose.bones[bone]
            for C in boneObj.constraints:
                if C.type == motion.props["rotation_controller"]:
                    try:
                        setattr(C, self.action, self.space)
                    except:
                        print(
                            "Item not compatible with transform - action / space :",
                            self.action,
                            self.space,
                        )

        return {"FINISHED"}


class OnigiriMotionMixerInherit(bpy.types.Operator):
    """This enables and disables the type of transform inheritance from the parent.
    There may be very little use for it but you have the option in case you have
    a unique rig setup that requires it"""

    transform: bpy.props.StringProperty(default="")
    state: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_inherit"
    bl_label = "Inherit parent orientation"

    @classmethod
    def poll(cls, context):
        oni_mixer = bpy.context.window_manager.oni_mixer

        if not oni_mixer.mixer_ready:
            return False

        return True

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        bones = set([b.name for b in bpy.context.selected_pose_bones])

        if len(bones) == 0:
            print("No bones selected")
            return {"FINISHED"}

        targetObj = oni_mixer["target"]
        target = targetObj.name

        if self.state == "True":
            state = True
        elif self.state == "False":
            state = False

        for bone in bones:
            boneObj = targetObj.data.bones[bone]
            if self.transform == "location":
                boneObj.use_local_location = state
            elif self.transform == "rotation":
                boneObj.use_inherit_rotation = state

        return {"FINISHED"}


class OnigiriMotionMixerAddBones(bpy.types.Operator):
    """Choose bones on the source rigs that will influence the target, allowing
    a link to be established, where the target will acquire the resulting mixed
    animation"""

    bl_idname = "onigiri.mixer_add_bones"
    bl_label = "Add selected bones to the influence"

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer
        bones = [o for o in bpy.context.selected_pose_bones]

        if oni_mixer.get("maps") is None:
            oni_mixer["maps"] = {}
        if oni_mixer["maps"].get("sources") is None:
            oni_mixer["maps"]["sources"] = {}

        targetObj = oni_mixer["target"]
        target = targetObj.name

        location, rotation, scale = (
            oni_mixer.mixer_location,
            oni_mixer.mixer_rotation,
            oni_mixer.mixer_scale,
        )

        for boneObj in bones:
            bone = boneObj.name
            rigObj = boneObj.id_data
            rig = rigObj.name
            for sourceObj in oni_mixer["sources"]:
                sourceObj.data.collections[mixer_group_source_inactive_name].assign(sourceObj.pose.bones[bone])
            if rig in oni_mixer["maps"]["sources"]:
                oni_mixer["maps"]["sources"][rig].pop(bone, "")

        #rig_data = {}
        for boneObj in bones:
            bone = boneObj.name
            rigObj = boneObj.id_data
            rig = rigObj.name

            if rig == target:
                continue

            for sourceObj in oni_mixer["sources"]:
                sourceObj.data.collections[mixer_group_source_inactive_name].assign(sourceObj.pose.bones[bone])

            if rig not in oni_mixer["maps"]["sources"]:

                oni_mixer["maps"]["sources"][rig] = {}
            if bone not in oni_mixer["maps"]["sources"][rig]:
                oni_mixer["maps"]["sources"][rig][bone] = {}
                oni_mixer["maps"]["sources"][rig][bone]["transforms"] = {
                    "location": location,
                    "rotation": rotation,
                    "scale": scale,
                }

            if bone not in rig_data:
                rig_data[bone] = {}
                rig_data[bone]["source"] = rigObj

        bpy.context.view_layer.objects.active = targetObj
        for bone in rig_data:
            armObj = rig_data[bone]["source"]
            arm = armObj.name
            targetObj.data.collections[mixer_group_source_active_name].assign(targetObj.pose.bones[bone])
            obj[arm].data.collections[mixer_group_source_active_name].assign(obj[arm].pose.bones[bone])
            constraints = targetObj.pose.bones[bone].constraints
            for c in constraints:
                if c.type == "COPY_LOCATION":
                    c.target = obj[arm]
                    c.subtarget = bone
                    targetObj.pose.bones[bone].constraints[c.name].target_space = (
                        motion.props["target_space"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].owner_space = (
                        motion.props["owner_space"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].influence = location
                if c.type == "COPY_ROTATION":
                    c.target = obj[arm]
                    c.subtarget = bone
                    targetObj.pose.bones[bone].constraints[c.name].target_space = (
                        motion.props["target_space"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].owner_space = (
                        motion.props["owner_space"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].mix_mode = (
                        motion.props["mix_mode"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].influence = rotation
                if c.type == "COPY_SCALE":
                    c.target = obj[arm]
                    c.subtarget = bone
                    targetObj.pose.bones[bone].constraints[c.name].target_space = (
                        motion.props["target_space"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].owner_space = (
                        motion.props["owner_space"]
                    )
                    targetObj.pose.bones[bone].constraints[c.name].influence = scale

        return {"FINISHED"}


class OnigiriMotionMixerRemoveBones(bpy.types.Operator):
    """Remove the selected bones from the influence, you can also do this bone by
    bone in the list if you expand it"""

    name: bpy.props.StringProperty(default="")

    bl_idname = "onigiri.mixer_remove_bones"
    bl_label = "Remove selected bones from influence"

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        if self.name != "":
            print("Remove single bone:", self.name)
            for boneObj in bpy.context.selected_pose_bones:
                dBone = boneObj.bone
                dBone.select = False

            armObj = bpy.context.active_object
            armObj.data.bones[self.name].select = True

        if oni_mixer.get("maps") is None:
            oni_mixer["maps"] = {}
        if oni_mixer["maps"].get("sources") is None:
            oni_mixer["maps"]["sources"] = {}

        bones = [o for o in bpy.context.selected_pose_bones]
        bone_names = set([o.name for o in bones])

        targetObj = oni_mixer["target"]
        target = targetObj.name

        for bone in bone_names:
            for sourceObj in oni_mixer["sources"]:
                sourceObj.data.collections[mixer_group_source_inactive_name].assign(bone)
                #bone.color.palette = mixer_group_source_inactive_theme

            targetObj.data.collections[mixer_group_target_inactive_name].assign(bone)

            for arm in oni_mixer["maps"]["sources"]:
                oni_mixer["maps"]["sources"][arm].pop(bone, "")

            constraints = targetObj.pose.bones[bone].constraints
            for c in constraints:
                if c.type == "COPY_LOCATION":
                    c.target = None
                    targetObj.pose.bones[bone].constraints[c.name].influence = 0
                if c.type == "COPY_ROTATION":
                    c.target = None
                    targetObj.pose.bones[bone].constraints[c.name].influence = 0
                if c.type == "COPY_SCALE":
                    c.target = None
                    targetObj.pose.bones[bone].constraints[c.name].influence = 0

        for rig in oni_mixer["maps"]["sources"]:
            if len(oni_mixer["maps"]["sources"][rig]) == 0:
                del oni_mixer["maps"]["sources"][rig]

        if "mPelvis" in bone_names:
            print("Bone removal included the anchor")
            oni_mixer.mixer_anchor_name = ""

        self.name = ""

        return {"FINISHED"}


class OnigiriMotionMixerSetLocation(bpy.types.Operator):
    """Toggle location influence for this bone"""

    name: bpy.props.StringProperty(default="")
    influence: bpy.props.IntProperty(default=0)

    bl_idname = "onigiri.mixer_set_location"
    bl_label = "Enable location influence"

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        globals.oni_mixer["constraints"][self.name][
            "location"
        ].influence = self.influence

        if self.name == "mPelvis":
            if self.influence:
                arm = globals.oni_mixer["constraints"][self.name][
                    "location"
                ].target.name
                oni_mixer.mixer_anchor_name = arm
            else:
                oni_mixer.mixer_anchor_name = ""

        self.name = ""

        return {"FINISHED"}


class OnigiriMotionMixerSetRotation(bpy.types.Operator):
    """Toggle rotation influence for this bone"""

    name: bpy.props.StringProperty(default="")
    influence: bpy.props.IntProperty(default=0)

    bl_idname = "onigiri.mixer_set_rotation"
    bl_label = "Enable rotation influence"

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        globals.oni_mixer["constraints"][self.name][
            "rotation"
        ].influence = self.influence

        self.name = ""

        return {"FINISHED"}


class OnigiriMotionMixerSetScale(bpy.types.Operator):
    """Toggle scale influence for this bone"""

    name: bpy.props.StringProperty(default="")
    influence: bpy.props.IntProperty(default=0)

    bl_idname = "onigiri.mixer_set_scale"
    bl_label = "Enable scale influence"

    def execute(self, context):
        obj = bpy.data.objects
        oni_mixer = bpy.context.window_manager.oni_mixer

        globals.oni_mixer["constraints"][self.name]["scale"].influence = self.influence

        self.name = ""

        return {"FINISHED"}


class OnigiriMotionSpliceProperties(bpy.types.PropertyGroup):

    def update_splice_blank(self, context):

        self["splice_blank"] = False

    splice_blank: bpy.props.BoolProperty(
        name="", description="", default=False, update=update_splice_blank
    )
    splice_menu_enabled: bpy.props.BoolProperty(
        name="", description="Expand the motion splicer features", default=False
    )

    def update_splice_target_locked(self, context):

        oni_splice = self
        if oni_splice.splice_target_locked:
            if len(bpy.context.selected_objects) != 1:
                oni_splice["splice_target_locked"] = False
                oni_splice.splice_message = "Splice target needs a single rig"
                print(
                    "Choose the rig you'll apply all of the actions to and click this button, only 1 rig"
                )
                return
            armObj = bpy.context.selected_objects[0]
            if armObj.type != "ARMATURE":
                oni_splice["splice_target_locked"] = False
                return
            if not oni_splice.splice_disable_onigiri_check:
                if armObj.get("onigiri") is None:
                    print(
                        "Onigiri check disallows foreign rigs from being used in this fashion."
                    )
                    print(
                        "If you really want to do this then use (Disable Onigiri Check)."
                    )
                    oni_splice["splice_target_locked"] = False
                    oni_splice.splice_message = "Onigiri only, see console"
                    return

            bpy.ops.object.mode_set(mode="EDIT")
            for boneObj in armObj.data.edit_bones:
                boneObj.use_connect = False
            bpy.ops.object.mode_set(mode="OBJECT")

            utils.get_state()
            oni_splice.splice_target_name = armObj.name
            oni_splice.splice_message = "Pick source"
            return
        else:
            oni_splice.splice_message = "Select a target rig"
            return

    splice_message: bpy.props.StringProperty(
        name="", description="", default="Look here for messages"
    )

    splice_target_locked: bpy.props.BoolProperty(
        name="",
        description="Click this to lock the target.  The target is where your animations will end up.  If your target already "
        "has an animation then the new source will be appended, which is essentially the function of this tool.  "
        "After you enable this you'll pick a source rig, one that contains an animation you want to append to the "
        "existing one on this rig and then disable this button to perform tha action.  Use the (Gap) property to "
        "tell the splicer how many frames to skip before adding the next action/animation.",
        default=False,
        update=update_splice_target_locked,
    )
    splice_target_name: bpy.props.StringProperty(
        name="", description="--internal", default=""
    )

    def update_splice_type(self, context):
        if not self.splice_keys and not self.splice_motion:
            self["splice_motion"] = True

    splice_keys: bpy.props.BoolProperty(
        name="",
        description="You  must have (keys) and/or (motion) enabled"
        "\n\n"
        "If there are animation keys on the source you may want to capture those.  You can capture those as well as "
        "motion.  Capturing keys allows for keys to be generated for joints that do not move but are still keyed, which "
        "can be beneficial if you are attempting to prevent a joint from moving at some point.",
        default=False,
        update=update_splice_type,
    )
    splice_motion: bpy.props.BoolProperty(
        name="",
        description="You  must have (keys) and/or (motion) enabled"
        "\n\n"
        "This detects motion from the source and keys those transforms onto the target rig.",
        default=True,
        update=update_splice_type,
    )
    splice_gap_insert: bpy.props.BoolProperty(
        name="",
        description="If you enable this then the new, source, animation will be inserted into the timeline where your animation "
        "cursor currently is.  The gaps will be used to tell the splicer how to place this source animation.",
        default=False,
    )
    splice_gap_start: bpy.props.IntProperty(
        name="",
        description="This is how far away from your existing animation, in frames, you will like to place the new clip.  If (Gap Insert) "
        "is enabled then this is how far away from the animation cursor that you want to insert the new clip.  Using "
        "negative numbers will have some interesting effects but a value of 1 for both, Gap Start and Gap End, will leave no "
        "space and does not overwrite any keys.",
        default=1,
    )
    splice_gap_end: bpy.props.IntProperty(
        name="",
        description="This has no use unless (Insert) is enabled"
        "\n\n"
        "Place your animation cursor somewhere, enable (Gap Insert).  Your animation will be inserted into the existing one on "
        "the target and there will be empty space on either side of the new clip, unless you had a different purpose.  Setting the "
        "values to gap 1 is no space, using any other values you can achieve interesting results.",
        default=1,
    )
    splice_spread_enabled: bpy.props.BoolProperty(
        name="",
        description="Enable this to fine tune the area of capture or the entire action will be recorded",
        default=False,
    )
    splice_spread_start: bpy.props.IntProperty(
        name="",
        description="The start and stop frames allow you to choose a portion of your source animation for appending rather than "
        "the entire thing.  Enable the feature and then adjust these values.",
        default=1,
    )
    splice_spread_end: bpy.props.IntProperty(
        name="",
        description="The start and stop frames allow you to choose a portion of your source animation for appending rather than "
        "the entire thing.  Enable the feature and then adjust these values.",
        default=1,
    )
    splice_disable_onigiri_check: bpy.props.BoolProperty(
        name="",
        description="Disable this to work with foreign rigs, it should work fine, but this is enabled by default to to keep the "
        "the head scratching low when animations don't do anything in SL.",
        default=False,
    )


class OnigiriMotionSpliceSync(bpy.types.Operator):

    bl_idname = "onigiri.splice_sync"
    bl_label = "Sync action range with spread"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        o = bpy.context.selected_objects[0]
        if o.type != "ARMATURE":
            return False
        if o.animation_data is None:
            return False
        if o.animation_data.action is None:
            return False
        return True

    def execute(self, context):
        oni_splice = bpy.context.scene.oni_splice
        armObj = bpy.context.selected_objects[0]
        spread_start, spread_end = armObj.animation_data.action.frame_range
        oni_splice.splice_spread_start = int(spread_start)
        oni_splice.splice_spread_end = int(spread_end)

        return {"FINISHED"}


class OnigiriMotionSpliceReset(bpy.types.Operator):

    bl_idname = "onigiri.splice_reset"
    bl_label = "Reset the splicer"

    def execute(self, context):

        oni_splice = bpy.context.scene.oni_splice
        state = utils.get_state()

        for prop in list(bpy.context.scene["oni_splice"]):
            try:
                oni_splice.property_unset(prop)
            except:
                print(
                    "Property",
                    prop,
                    "cannot be unsetted, if that's even a word.  We'll lets make it a word \o/",
                )

        utils.set_state(state)
        return {"FINISHED"}


class OnigiriMotionSpliceCapture(bpy.types.Operator):

    bl_idname = "onigiri.splice_capture"
    bl_label = "Capture the segment"

    @classmethod
    def poll(cls, context):
        if len(bpy.context.selected_objects) != 1:
            return False
        if bpy.context.selected_objects[0].type != "ARMATURE":
            return False
        return True

    def execute(self, context):
        obj = bpy.data.objects

        oni_splice = bpy.context.scene.oni_splice

        armObj = bpy.context.selected_objects[0]

        state = utils.get_state()

        if armObj.name == oni_splice.splice_target_name:
            print(
                "Target and source cannot be the same, if you want to insert or append the same animation"
            )
            print(
                "from target TO target then make a copy of the rig and then use the copy as source"
            )
            oni_splice.splice_message = "Error - source = target"
            popup("The source and target are the same, see console", "Error", "ERROR")
            return {"FINISHED"}

        target = oni_splice.splice_target_name
        for boneObj in armObj.data.bones:
            if boneObj.name not in obj[target].data.bones:
                print(
                    "The rigs are not compatible, did you choose the wrong animation source?  It has to be a ONI rig."
                )
                popup("Not a ONI rig, wrong source", "Error", "ERROR")
                return {"FINISHED"}

        gap_insert = oni_splice.splice_gap_insert
        gap_start = oni_splice.splice_gap_start
        gap_end = oni_splice.splice_gap_end
        spread_enabled = oni_splice.splice_spread_enabled
        spread_start = oni_splice.splice_spread_start
        spread_end = oni_splice.splice_spread_end
        splice.props["camera"] = True
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

        result = splice.main(
            target=oni_splice.splice_target_name,
            source=armObj.name,
            keys=oni_splice.splice_keys,
            motion=oni_splice.splice_motion,
            gap_insert=gap_insert,
            gap_start=gap_start,
            gap_end=gap_end,
            spread_enabled=spread_enabled,
            spread_start=spread_start,
            spread_end=spread_end,
        )
        splice.props["camera"] = False

        if result:
            oni_splice.splice_message = "Finished!"
        else:
            oni_splice.splice_message = "Error!"

        state = utils.activate(oni_splice.splice_target_name, safe=True)

        return {"FINISHED"}
# endregion OnigiriMotionProperties
