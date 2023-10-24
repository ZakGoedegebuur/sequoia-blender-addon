import bpy
import bpy_extras
import json
import math

def metadata(version_major, version_minor, version_patch, generator = "no name", copyright = "no copyright"):
    return {
        "generator": generator,
        "copyright": copyright,
        "version": {
            "major": version_major,
            "minor": version_minor,
            "patch": version_patch
        }
    }

class SequoiaModelGenerator:
    def __init__(self):
        self.loaded_data = {
        "objects": [],
        }
        self.processed_data = {}

    def load_data(self, passthrough, context):
        passthrough.report({'INFO'}, "loading data")

        for object in bpy.data.objects:
            #passthrough.report({'INFO'}, str(type(object)))
            object_data = {
                "name": object.name,
                "type": object.type,
                "is_hidden": object.hide_get(),
                "is_selected": object.select_get(),
                "parent_type": object.parent_type,
                "parent_object_name": object.parent.name if object.parent != None else None,
                "parent_bone_name": object.parent_bone if object.parent_bone != "" else None,
                "child_bone_names": [],
                "child_names": [],
            }

            for child in object.children:
                object_data["child_names"].append(child.name)

            if object.type == 'MESH':
                depsgraph = bpy.context.evaluated_depsgraph_get()
                obj = object.evaluated_get(depsgraph)
                obj.data.split_faces()

                triangles = obj.data.loop_triangles
                vertices = obj.data.vertices
                object_data["mesh_data"] = {
                    "index_count": len(triangles) * 3,
                    "indices": [],
                    "vertex_count": len(vertices),
                    "vertices": [],
                }

                for tri in triangles:
                    object_data["mesh_data"]["indices"].append(tri.vertices[0])
                    object_data["mesh_data"]["indices"].append(tri.vertices[1])
                    object_data["mesh_data"]["indices"].append(tri.vertices[2])

                for vert in vertices:
                    vertex = {
                        "position": [vert.co.x, vert.co.y, vert.co.z],
                        "normal": [vert.normal.x, vert.normal.y, vert.normal.z]
                    }
                    object_data["mesh_data"]["vertices"].append(vertex)

            elif object.type == 'ARMATURE':
                armature = object.data
                for bone in armature.bones:
                    bone_data = {
                        "name": bone.name,
                        "type": 'BONE',
                        "is_hidden": object.hide_get(),
                        "is_selected": object.select_get(),
                        "parent_type": 'ARMATURE' if bone.parent == "" else 'BONE',
                        "parent_object_name": object.name,
                        "parent_bone_name": bone.parent.name if bone.parent != None else None,
                        "child_bone_names": [],
                        "child_names": [],
                    }

                    for child_bone in bone.children:
                        bone_data["child_bone_names"].append(child_bone.name)

                    self.loaded_data["objects"].append(bone_data)
            
            elif object.type == 'CAMERA':
                camera = object.data
                object_data["camera_data"] = {
                    "type": camera.type,
                    "hfov": math.degrees(camera.angle_x),
                    "clip_start": camera.clip_start,
                    "clip_end": camera.clip_end,
                }

            elif object.type == 'LIGHT':
                light = object.data
                object_data["light_data"] = {
                    "type": light.type,
                    "color": {"r": light.color.r, "g": light.color.g, "b": light.color.b},
                    "energy": light.energy,
                }

                if light.type == 'SUN':
                    object_data["light_data"]["sun_radius_angle"] = math.degrees(light.angle)

            self.loaded_data["objects"].append(object_data)

    def process_data(self, passthrough, context):
        passthrough.report({'INFO'}, "processing data")

        self.processed_data = {
            "metadata": metadata(1, 0, 0, "SQO Original Blender Addon", bpy.context.scene.sequoia.get("model_copyright", None)),
            "nodes": [],
            "cameras": [],
            "lights": [],
            "meshes": [],
            #"materials": ["shiny", "rough", "matte"],
            #"textures": ["pallette.png", "grass.png"]
        }

        for obj in self.loaded_data["objects"]:
            node = {
                "name": obj["name"],
                "type": obj["type"],
                "parent_type": obj["parent_type"],
                "parent_object_name": obj["parent_object_name"],
                "parent_bone_name": obj["parent_bone_name"],
                "child_bone_names": obj["child_bone_names"],
                "child_names": obj["child_names"],
            }

            should_include_extras = True
            cull_hidden = context.scene.sequoia.get("limit_to_visible", False)
            if cull_hidden and obj["is_hidden"]:
                should_include_extras = False
            cull_deselected = context.scene.sequoia.get("limit_to_selected", False)
            if cull_deselected and not obj["is_selected"]:
                should_include_extras = False

            if "mesh_data" in obj and should_include_extras and context.scene.sequoia.get("export_meshes", True):
                node["mesh"] = obj["mesh_data"]

            if "camera_data" in obj and should_include_extras and context.scene.sequoia.get("export_cameras", True):
                node["camera"] = obj["camera_data"]

            if "light_data" in obj and should_include_extras and context.scene.sequoia.get("export_lights", True):
                node["light"] = obj["light_data"]

            self.processed_data["nodes"].append(node)

        for obj in self.processed_data["nodes"]:
            def find_node_index():
                for ind, node in enumerate(self.processed_data["nodes"]):
                    if obj["parent_type"] == 'BONE':
                        if node["name"] == obj["parent_bone_name"] and node["parent_object_name"] == obj["parent_object_name"]:
                            return ind
                    else:
                        if node["name"] == obj["parent_object_name"]:
                            return ind
                return None
            
            if "mesh" in obj:
                mesh = {
                    "parent_object_name": obj["name"],
                    "parent_node_index": find_node_index(),
                    "vertex_count": obj["mesh"]["vertex_count"],
                    "index_count": obj["mesh"]["index_count"],
                    #"vertices": obj["mesh_data"]["vertices"],
                    #"indices": obj["mesh_data"]["indices"]
                }

                del obj["mesh"]
                self.processed_data["meshes"].append(mesh)
            
            if "camera" in obj:
                camera = {
                    "parent_object_name": obj["name"],
                    "parent_node_index": find_node_index(),
                    "camera_type": obj["camera"]["type"],
                    "horizontal_fov": obj["camera"]["hfov"],
                    "clip_start": obj["camera"]["clip_start"],
                    "clip_end": obj["camera"]["clip_end"],
                }

                del obj["camera"]
                self.processed_data["cameras"].append(camera)

            if "light" in obj:
                light = {
                    "type": obj["light"]["type"],
                    "color": obj["light"]["color"],
                    "energy": obj["light"]["energy"],
                }

                if light["type"] == 'SUN':
                    light["sun_radius_angle"] = obj["light"]["sun_radius_angle"]

                del obj["light"]
                self.processed_data["lights"].append(light)

    def dump_json(self, passthrough):
        passthrough.report({'INFO'}, "dumping json")

        return json.dumps(self.processed_data, indent=2)

class SequoiaExportSQO(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "exportsqo.sqo"
    bl_label = "Export SQO"         # Display name in the interface.
    # bl_options = {}
    filename_ext = ".json"

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        generator = SequoiaModelGenerator()
        generator.load_data(self, context)
        generator.process_data(self, context)
        
        json_data = generator.dump_json(self)

        file = open(self.filepath, "wb", 0)
        file.write(bytes(json_data, "utf-8"))
        file.close()

        del generator

        #self.report({'INFO'}, json_data)
        self.report({'INFO'}, "Exporting model to " + self.filepath)

        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sqo_settings = context.scene.sequoia
        
        col = layout.column(heading = "Copyright", align = True)
        col.prop(sqo_settings, "model_copyright")

        col = layout.column(align = True)
        col.prop(sqo_settings, "export_verbose", text="Export Verbose Data")

class SQO_PT_export_include_settings(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Export"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(self, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORTSQO_OT_sqo"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sqo_settings = context.scene.sequoia

        col = layout.column(heading = "Include", align = True)
        col.prop(sqo_settings, "export_meshes", text="Meshes")
        col.prop(sqo_settings, "export_empties", text="Empties")
        col.prop(sqo_settings, "export_lights", text="Lights")
        col.prop(sqo_settings, "export_cameras", text="Cameras")
        col.prop(sqo_settings, "export_cubemaps", text="Cubemaps")
        col.prop(sqo_settings, "export_speakers", text="Speakers")
        col.prop(sqo_settings, "export_materials", text="Materials")

        col = layout.column(heading = "Limit to", align = True)
        col.prop(sqo_settings, "limit_to_selected", text="Selected Objects")
        col.prop(sqo_settings, "limit_to_visible", text="Visible Objects")


class SQO_PT_export_mesh_settings(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Mesh"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(self, context):
        sfile = context.space_data
        operator = sfile.active_operator
        return operator.bl_idname == "EXPORTSQO_OT_sqo"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        sqo_settings = context.scene.sequoia
        col = layout.column(heading = "Override", align = True)
        col.prop(sqo_settings, "force_32_bit_indices", text = "Force 32 bit indices")
        col.prop(sqo_settings, "force_skinned_vertices", text = "Force skinned vertices")

        
