
import bpy


## Legacy Collada-Export deaktiviert, Wrapper für glTF
def write_collada(armature="", root="", write=False, file_in="", file_out=""):
    """[Legacy] Wrapper für write_gltf, damit alte Aufrufe weiterhin funktionieren."""
    return write_gltf(armature=armature, root=root, write=write, file_in=file_in, file_out=file_out)

## edit_dae als Dummy-Wrapper für Kompatibilität
def edit_dae(*args, **kwargs):
    print("edit_dae ist nicht mehr verfügbar. Bitte glTF verwenden. [Legacy Collada-Funktion]")
    return None


def write_gltf(armature="", root="", write=False, file_in="", file_out=""):
    """Exportiert das angegebene Armature-Objekt als glTF (.glb/.gltf) Datei. [Standard]"""
    armObj = bpy.data.objects[armature]
    bpy.ops.object.select_all(action='DESELECT')
    armObj.select_set(True)
    bpy.context.view_layer.objects.active = armObj
    print(f"Exportiere glTF nach: {file_out} [glTF]")
    bpy.ops.export_scene.gltf(filepath=file_out, export_selected=True)

    # Falls benötigt, hier Variablen korrekt einrücken und verwenden
    # use_offset_volume = oni_mesh.use_offset_volume
    # use_offset_location = oni_mesh.use_offset_location
    # use_offset_rotation = oni_mesh.use_offset_rotation
    # use_offset_scale = oni_mesh.use_offset_scale

    bind_pose = {}
    joint_pose = {}

    print("Running universal exporter [glTF]")

    for pBone in armObj.pose.bones:
        dBone = pBone.bone
        bone = pBone.name

        if bone not in skel.avatar_skeleton:
            print("Found incompatible bone for SL, skipping", bone)
            continue

        joint_pose[bone] = transforms[bone]["local"]["matrix"]
        bind_pose[bone] = transforms[bone]["bind_data"]

    pretty_mats = True

    ET.register_namespace("", "http://www.collada.org/2005/11/COLLADASchema")
    tree = ET.parse(file_in)
    root = tree.getroot()
    n = "{http://www.collada.org/2005/11/COLLADASchema}"
    controller = {}
    skin = {}
    names = list()
    joints = {}
    lc = root.find(f"{n}library_controllers")
    for c in lc:
        cid = c.get("id")
        name = c.get("name")
        controller[cid] = name
        skin = c.find(f"{n}skin")

        for skin_child in skin:

            joint_total = 0
            float_total = 0

            for data in skin_child:
                if data.tag == n + "Name_array":
                    Name_array = data
                    names = data.text.split()

                    Name_array_accessor_count = skin_child.find(
                        f"{n}technique_common/{n}accessor"
                    )

            for data in skin_child:
                if data.tag == n + "float_array":

                    param = skin_child.find(f"{n}technique_common/{n}accessor/{n}param")

                    if param.get("type") == "float4x4":

                        float_array = data

                        float_array_accessor_count = skin_child.find(
                            f"{n}technique_common/{n}accessor"
                        )

                        matrices = list()

                        for i in range(len(names)):
                            joint_total += 1
                            text_mat = list()
                            bone = names[i]
                            m = bind_pose[bone]

                            mat = m.inverted()

                            for m in mat:

                                float_total += 4

                                shorten = [round(a, 6) for a in m]
                                t = [str(a) for a in shorten]

                                if pretty_mats:
                                    text_mat.append("\n")
                                else:
                                    text_mat.append(" ")
                                text_mat.append(" ".join(t))
                            matrices.extend(text_mat)

                            if pretty_mats:
                                matrices.append("\n")
                            else:
                                matrices.append(" ")

                        Name_array.set("count", str(joint_total))
                        float_array.set("count", str(float_total))
                        Name_array_accessor_count.set("count", str(joint_total))
                        float_array_accessor_count.set("count", str(joint_total))

                        data.text = "".join(matrices)
                        del matrices

    if write_nodes:
        for node in root.iter(f"{n}node"):
            if node.get("type") == "JOINT":
                matrix = node.find(f"{n}matrix")
                if node.attrib.get("name") is not None:
                    bone = node.attrib["name"]

                    if bone in joint_pose:
                        tmat = pill.matrix_to_text(joint_pose[bone])
                        matrix.text = " ".join(tmat)
                    else:
                        print(
                            ":library_visual_scene - missing bone, this should never happen",
                            bone,
                        )

    if pretty_mats:
        pretty_nodes(root=root)

    tree.write(file_out, xml_declaration=True, encoding="utf-8", method="xml")

    return True


def pretty_nodes(root=None):

    print("Generating pretty nodes")

    n = "{http://www.collada.org/2005/11/COLLADASchema}"

    for node in root.iter(f"{n}node"):
        if node.get("type") == "JOINT":
            matrix = node.find(f"{n}matrix")
            if node.attrib.get("name") is not None:
                bone = node.attrib["name"]

                tmat = matrix.text.split()

                t = list()
                for r in range(0, 16, 4):
                    t.append("\n")
                    v = tmat[r : r + 4]

                    for tfl in v:
                        rfl = round(float(tfl), 6)
                        t.append(f"{rfl:.6f}")
                        t.append(" ")
                t.append("\n")
                matrix.text = " ".join(t)

    return root


def to_deg(mat):
    eu = mat.to_euler()
    return [math.degrees(round(a, 4)) for a in eu]
