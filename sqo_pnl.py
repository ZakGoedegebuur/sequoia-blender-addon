import bpy

class SQO_PT_mesh_panel(bpy.types.Panel):
    bl_idname = "SQO_PT_mesh_panel"
    bl_label = "Sequoia"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None and context.object.type == 'MESH')
        
    def draw_header(self, context):
        layout = self.layout
        #layout.label(text="My Select")
    
    def draw(self, context):
        #context.object["custom_message"] = "ooga booga"

        layout = self.layout
        box = layout.box()

        col = box.column()
        row = col.row()
        row.operator("object.sqo_test_export")

        row = col.row()
        sqo_settings = context.object.sequoia
        row.prop(sqo_settings, "custom_message", text="Custom message")