import bpy

class SequoiaObjectProperties(bpy.types.PropertyGroup):
    custom_message: bpy.props.StringProperty(name="Custom message", maxlen=128)

class SequoiaSceneProperties(bpy.types.PropertyGroup):
    limit_to_selected: bpy.props.BoolProperty(name="Limit to selected", default=False)
    limit_to_visible: bpy.props.BoolProperty(name="Limit to visible", default=False)
    
    model_copyright: bpy.props.StringProperty(name="Copyright")