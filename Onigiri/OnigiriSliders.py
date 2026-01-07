
import bpy # type: ignore
import os
from . import utils
from . import rigutils
from . import mod_settings

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = oni_settings["paths"]["data"]

# region OnigiriSlidersProperties
class OnigiriSlidersProperties(bpy.types.PropertyGroup):
	def update_sliders_blank(self, context):
		self["sliders_blank"] = False

	sliders_blank: bpy.props.BoolProperty = bpy.props.BoolProperty(default=False, update=update_sliders_blank)

	def sliders_menu_enabled(self, context):
		if self.sliders_menu_enabled:
			print("Body Shop - enabled")
		else:
			print("Body Shop - disabled")
			sliders.restore_rig()

	sliders_menu_enabled: bpy.props.BoolProperty = bpy.props.BoolProperty(
		name="",
		description="NOTE: For efficiency sake, disable this menu item when not in use!"
		"\n\n"
		"WARNING: Only use this with rigs and associated content that has not been scaled, i.e. your own custom content only. "
		"There is no other reason to use this tool except for your content that is not transformed.  If you do not honor this "
		"warning you may very well damage your product."
		"\n\n"
		"This is a slider system for use with correcting weight problems but you can also use it as a character "
		"shaper if you're careful.  If you're freezing the mesh your bone properties will be returned to their "
		"natural state, the sliders neutralized, and you can start a new round of shaping.  Note that it's always "
		"best to do your major work on the mesh itself and only use this for tweaking and/or deformation testing",
		default=False,
		update=sliders_menu_enabled,
	)

	def update_scale(self, context):
		if self.sliders_scale:
			self["sliders_location"] = False

	def update_location(self, context):
		if self.sliders_location:
			self["sliders_scale"] = False

	sliders_location: bpy.props.BoolProperty = bpy.props.BoolProperty(
		name="",
		description="Enable the position sliders for view and manipulation",
		default=False,
		update=update_location,
	)
	sliders_scale: bpy.props.BoolProperty = bpy.props.BoolProperty(
		name="",
		description="Enable the sizing sliders for view and manipulation",
		default=True,
		update=update_scale,
	)
	sliders_show_all: bpy.props.BoolProperty = bpy.props.BoolProperty(
		name="",
		description="Enable the view of all bones in the selected rig.  This can be a lot of clutter.  The default is to show only selected pose bones",
		default=False,
	)

	@staticmethod
	def sliders_set_rig(self):
		sliders.set_rig()
		return 1

	sliders_set_rig: bpy.props.IntProperty = bpy.props.IntProperty(
		name="",
		description="- internal setter for sliders.set_rig()",
		default=0,
		get=sliders_set_rig,
	)

	@staticmethod
	def sliders_restore_rig(self):
		sliders.restore_rig()
		return 1

	sliders_restore_rig: bpy.props.IntProperty = bpy.props.IntProperty(
		name="",
		description="- internal getter for sliders.restore_rig()",
		default=0,
		get=sliders_restore_rig,
	)

	def sliders_rig_display_stick(self, context):
		armObj = utils.rig_is_selected()
		if armObj:
			if self.sliders_rig_display_stick:
				if armObj.get("oni_sliders_display_type") is None:
					armObj["oni_sliders_display_type"] = armObj.data.display_type
				armObj.data.display_type = "STICK"

			else:
				display_type = armObj.get(
					"oni_sliders_display_type", armObj.data.display_type
				)
				armObj.data.display_type = display_type

	sliders_rig_display_stick: bpy.props.BoolProperty = bpy.props.BoolProperty(
		name="",
		description="Enable the view of all bones in the selected rig.  This can be a lot of clutter.  The default is to show only selected pose bones",
		default=False,
		update=sliders_rig_display_stick,
	)


class OnigiriSlidersShowAllBones(bpy.types.Operator):
	"""Show all bones in the selected rig"""

	bl_idname = "onigiri.sliders_show_all_bones"
	bl_label = "Show All Bones"

	@classmethod
	def poll(cls, context):
		if len(bpy.context.selected_objects) != 1:
			return False
		if bpy.context.selected_objects[0].type != "ARMATURE":
			return False
		return True

	def execute(self, context):
		oni_misc = bpy.context.window_manager.oni_misc
		oni_misc.enable_base_bones = True
		oni_misc.enable_face_bones = True
		oni_misc.enable_wing_bones = True
		oni_misc.enable_spine_bones = True
		oni_misc.enable_hand_bones = True
		oni_misc.enable_tail_bones = True
		oni_misc.enable_volume_bones = True
		oni_misc.enable_attach_bones = True
		oni_misc.enable_attach2_bones = True

		return {"FINISHED"}


class OnigiriSlidersResetSelected(bpy.types.Operator):
	"""Reset all of the sliders for the selected pose bone for this transform.  To
	reset all of your sliders on the selected pose bones select one of Position or Scale
	and click this, then select the other and click this again"""

	bl_idname = "onigiri.sliders_reset_selected"
	bl_label = "Reset Selected"

	@classmethod
	def poll(cls, context):
		if bpy.context.mode != "POSE":
			return False
		if len(bpy.context.selected_objects) == 0:
			return False
		if len(bpy.context.selected_pose_bones) == 0:
			return False
		return True

	def execute(self, context):
		oni_sliders = bpy.context.scene.oni_sliders

		for boneObj in bpy.context.selected_pose_bones:

			sliders.reset(boneObj)

		return {"FINISHED"}


class OnigiriSlidersResetAll(bpy.types.Operator):
	"""Reset all of the sliders associated with this rig for this transform.  To
	reset all of your sliders select one of Position or Scale and click this, then
	select the other and click this again"""

	bl_idname = "onigiri.sliders_reset_all"
	bl_label = "Reset All"

	@classmethod
	def poll(cls, context):
		if len(bpy.context.selected_objects) == 0:
			return False
		selected = bpy.context.selected_objects
		rigs = 0
		for o in selected:
			if o.type == "ARMATURE":
				rigs += 1
		if rigs != 1:
			return False
		return True

	def execute(self, context):
		oni_sliders = bpy.context.scene.oni_sliders
		armObj = bpy.context.selected_objects[0]

		for boneObj in armObj.pose.bones:

			sliders.reset(boneObj)

		return {"FINISHED"}


class OnigiriSlidersStore(bpy.types.Operator):
	"""Store (save) your mesh shape and rig configuration  for recovery using
	(Restore) in case something goes wrong"""

	bl_idname = "onigiri.sliders_store"
	bl_label = "Restore Mesh Shape"

	@classmethod
	def poll(cls, context):
		if len(bpy.context.selected_objects) > 0:
			return True
		return False

	def execute(self, context):

		selected = bpy.context.selected_objects

		rigs = []
		for o in selected:
			if o.type != "MESH":
				continue
			o["oni_sliders_mesh"] = o.data.copy()
			o["oni_sliders_matrix_world"] = o.matrix_world.copy()

		for armObj in rigs:
			mesh = rigutils.get_associated_mesh
			if not mesh:
				continue
			for o in mesh:
				o["oni_sliders_mesh"] = o.data.copy()
				o["oni_sliders_matrix_world"] = o.matrix_world.copy()

		for o in selected:
			if o.type == "ARMATURE":
				for boneObj in o.data.bones:
					boneObj["oni_sliders_matrix_local"] = boneObj.matrix_local.copy()
					boneObj["oni_sliders_head_local"] = boneObj.head_local.copy()
					boneObj["oni_sliders_tail_local"] = boneObj.tail_local.copy()

		return {"FINISHED"}


class OnigiriSlidersRestore(bpy.types.Operator):
	"""Restore your mesh and rig to the last stored (saved) state"""

	bl_idname = "onigiri.sliders_restore"
	bl_label = "Restore Avatar"

	@classmethod
	def poll(cls, context):

		if bpy.context.mode == "EDIT_MESH":
			return False
		if len(bpy.context.selected_objects) > 0:
			return True
		return False

	def execute(self, context):
		oni_slider = bpy.context.scene.oni_sliders
		selected = bpy.context.selected_objects
		state = utils.get_state()

		rigs = []
		for o in selected:
			if o.type == "ARMATURE":
				rigs.append(o)
				continue
			if o.type != "MESH":
				continue
			if o.get("oni_sliders_mesh"):
				print("Restoring selected mesh", o.name)
				meshData = o["oni_sliders_mesh"]
				o.data = meshData
			if o.get("oni_sliders_matrix_world"):
				matrix = o["oni_sliders_matrix_world"]
				o.matrix_world = mathutils.Matrix(matrix)

		for armObj in rigs:
			mesh = rigutils.get_associated_mesh(armObj)
			if not mesh:
				continue

			for meshObj in mesh:
				if meshObj.get("oni_sliders_mesh"):
					meshData = meshObj["oni_sliders_mesh"]
					print("restoring associated mesh", meshObj.name)
					meshObj.data = meshData

				if meshObj.get("oni_sliders_matrix"):
					matrix = meshObj["oni_sliders_matrix_world"]
					meshObj.matrix_world = mathutils.Matrix(matrix)

		for armObj in rigs:
			armObj.select_set(True)
			utils.activate(armObj)
			bpy.ops.object.mode_set(mode="EDIT")
			for boneObj in armObj.data.edit_bones:

				if boneObj.get("oni_sliders_matrix_local") is None:
					print("Nothing stored, skipping (Restore)")
					break
				matrix = mathutils.Matrix(boneObj["oni_sliders_matrix_local"])
				if matrix:
					boneObj.matrix = mathutils.Matrix(matrix)
				head_local = boneObj["oni_sliders_head_local"]
				if head_local:
					boneObj.head = head_local
				tail_local = boneObj["oni_sliders_tail_local"]
				if head_local:
					boneObj.tail = tail_local
				if matrix:
					roll = utils.get_bone_roll(matrix)
					boneObj.roll = roll

				if 1 == 0:
					matrix = mathutils.Matrix(boneObj.get("oni_sliders_matrix"))
					if matrix:
						boneObj.matrix = mathutils.Matrix(matrix)
					head = boneObj.get("oni_sliders_head")
					if head:
						boneObj.head = head
					tail = boneObj.get("oni_sliders_tail")
					if tail:
						boneObj.tail = tail
					roll = boneObj.get("oni_sliders_roll")
					if roll:
						roll = boneObj.get("oni_sliders_roll")

			bpy.ops.object.mode_set(mode="OBJECT")
			armObj.select_set(False)

		utils.update()

		if 1 == 0:
			for armObj in rigs:
				armObj.select_set(True)
				utils.activate(armObj)
				for boneObj in armObj.pose.bones:
					boneObj.matrix = mathutils.Matrix()
				utils.update()

		utils.set_state(state)

		return {"FINISHED"}


class OnigiriSlidersApply(bpy.types.Operator):
	"""Bake the shape into the mesh.  This will freeze the shape of the mesh and
	# then reset the sliders for another go.  It will also store the mesh data before
	freezing so that you can restore it, if there's no mesh data already"""

	bl_idname = "onigiri.sliders_apply"
	bl_label = "Apply Shape"

	@classmethod
	def poll(cls, context):
		selected = bpy.context.selected_objects
		rigs = 0
		for o in selected:
			if o.type == "ARMATURE":
				rigs += 1
		if rigs != 1:
			return False
		return True

	def execute(self, context):
		oni_slider = bpy.context.scene.oni_sliders
		armObj = bpy.context.selected_objects[0]

		mesh = rigutils.get_associated_mesh(armObj)
		if len(mesh) == 0:
			print("no mesh associated with the armature")
			popup("There's no mesh to freeze", "Info", "INFO")
			return {"FINISHED"}

		for o in mesh:
			if o.get("oni_sliders_mesh") is None:
				o["oni_sliders_mesh"] = o.data.copy()
			if o.get("oni_sliders_matrix_world") is None:
				o["oni_sliders_matrix_world"] = o.matrix_world.copy()

		if 1 == 0:
			for boneObj in armObj.data.edit_bones:
				boneObj["oni_sliders_matrix"] = boneObj.matrix.copy()
				boneObj["oni_sliders_head"] = boneObj.head.copy()
				boneObj["oni_sliders_tail"] = boneObj.tail.copy()
				boneObj["oni_sliders_roll"] = boneObj.roll

		for boneObj in armObj.data.bones:
			boneObj["oni_sliders_matrix_local"] = boneObj.matrix_local.copy()
			boneObj["oni_sliders_head_local"] = boneObj.head_local.copy()
			boneObj["oni_sliders_tail_local"] = boneObj.tail_local.copy()

		rigutils.rebind(armObj, keep_animation=True)

		return {"FINISHED"}


class OnigiriSlidersClean(bpy.types.Operator):
	"""During the slider process a copy of your mesh data is preserved and also stored
	when you ask.  This can result in a large amount of unused data in your scene so it is
	advised to clean this when you're done, by using this button"""

	bl_idname = "onigiri.sliders_clean"
	bl_label = "Select everything and click"

	@classmethod
	def poll(cls, context):
		if len(bpy.context.selected_objects) > 0:
			return True
		return False

	def execute(self, context):
		oni_sliders = bpy.context.scene.oni_sliders
		for o in bpy.context.selected_objects:
			o.pop("oni_sliders_mesh", "")
			o.pop("oni_sliders_matrix_world", "")

		if o.type == "ARMATURE":
			o.data.display_type = o.pop("oni_sliders_display_type", o.data.display_type)
		oni_sliders.property_unset("sliders_rig_display_stick")

		print("Cleaned")

		return {"FINISHED"}


class OnigiriSlidersMatch(bpy.types.Operator):
	"""Match the adjustments you made to the other side of the rig.  If this is a
	Onigiri rig the it will work, otherwise this feature is most likely disabled"""

	bl_idname = "onigiri.sliders_match"
	bl_label = "Match"

	@classmethod
	def poll(cls, context):
		selected = bpy.context.selected_objects
		rigs = 0
		for o in selected:
			if o.type == "ARMATURE":
				rigs += 1
		if rigs != 1:
			return False

		if bpy.context.mode != "POSE":
			return False
		if len(bpy.context.selected_pose_bones) == 0:
			return False

		if o.get("onigiri") is None:
			return False
		return True


class OnigiriSlidersAddSelected(bpy.types.Operator):
	"""Add selected pose bones to the slider system"""

	bl_idname = "onigiri.sliders_add_selected"
	bl_label = "Add Selected"

	@classmethod
	def poll(cls, context):

		selected = bpy.context.selected_objects
		rigs = 0
		for o in selected:
			if o.type == "ARMATURE":
				rigs += 1
		if rigs != 1:
			return False

		if bpy.context.mode != "POSE":
			return False
		if len(bpy.context.selected_pose_bones) == 0:
			return False
		return True

	def execute(self, context):
		def mookie(self, context):
			print("mookie doo")

		oni_sliders = bpy.context.scene.oni_sliders
		armObj = bpy.context.selected_objects[0]

		pose_bones = bpy.context.selected_pose_bones

		for boneObj in pose_bones:
			print("adding props to bone:", boneObj.name)

			boneObj["oni_sliders_enabled"] = True

		return {"FINISHED"}

		for boneObj in pose_bones:

			if boneObj.get("_RNA_UI"):
				if "oni_sliders_" in boneObj["_RNA_UI"]:
					continue

			if 1 == 0:
				boneObj["oni_sliders_scale"] = {
					"name": "Scale:",
					"description": "adjust bone scale",
					"min": 0.0,
					"max": 2.0,
					"soft_min": 0.0,
					"soft_max": 1.0,
				}
			else:
				boneObj["oni_sliders_scale"] = 0.5

			boneObj["_RNA_UI"] = {}
			boneObj["_RNA_UI"]["oni_sliders_scale"] = {
				"name": "Scale:",
				"description": "adjust bone scale",
				"min": 0.0,
				"max": 2.0,
				"soft_min": 0.0,
				"soft_max": 1.0,
				"update": sliders.scale_update,
			}

		return {"FINISHED"}
# endregion OnigiriSlidersProperties
