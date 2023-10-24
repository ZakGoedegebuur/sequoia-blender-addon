import bpy
import json

class SequoiaTestExport(bpy.types.Operator):
    bl_idname = "object.sqo_test_export"
    bl_label = "Test Export"
    bl_description = "Export test data to a file"

    @classmethod
    def poll(cls, context):
      return True

    def execute(self, context):
        data = []
        for obj in bpy.data.objects:
           obj_data = { "name": obj.name, "custom_message": obj.sequoia.get("custom_message", None) }
           data.append(obj_data)

        json_data = json.dumps(data, indent=2)
        
        file = open("C:/Dev/python/tutorial/data.json", "wb", 0)
        self.report({'INFO'}, json_data)
        file.write(bytes(json_data, "utf-8"))

        return {'FINISHED'}