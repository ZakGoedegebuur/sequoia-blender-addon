import bpy

class SequoiaObjectProperties(bpy.types.PropertyGroup):
    custom_message: bpy.props.StringProperty(name="Custom message", maxlen=128)

class SequoiaSceneProperties(bpy.types.PropertyGroup):
    model_copyright: bpy.props.StringProperty(name="Copyright")
    
    limit_to_selected: bpy.props.BoolProperty(name="Limit to selected", default=False)
    limit_to_visible: bpy.props.BoolProperty(name="Limit to visible", default=False)
    
    force_32_bit_indices: bpy.props.BoolProperty(
        name = "Force 32 bit indices", 
        default = False, 
        description = "todo - When this setting is off meshes in the scene can choose between exporting with 32 bit and 16 bit indices. When this setting is turned on all mesh indices in the exported model are guaranteed to use 32 bit integers.\n\nThis may result in larger files, but if the target renderer requires 32 bit indices, it will mean no conversions from 16 bit to 32 bit will be necessary."
        )