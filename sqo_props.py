import bpy

class SequoiaObjectProperties(bpy.types.PropertyGroup):
    custom_message: bpy.props.StringProperty(name="Custom message", maxlen=128)

class SequoiaSceneProperties(bpy.types.PropertyGroup):
    model_copyright: bpy.props.StringProperty(name="Copyright")
    export_verbose: bpy.props.BoolProperty(name="Export Verbose", default=False, description="When this setting is on, extra information is exported to the file. This information may be helpful for development and debugging")
    
    limit_to_selected: bpy.props.BoolProperty(name="Limit to selected", default=False)
    limit_to_visible: bpy.props.BoolProperty(name="Limit to visible", default=False)
    
    export_meshes: bpy.props.BoolProperty(name="Export Meshes", default=True)
    export_empties: bpy.props.BoolProperty(name="Export Empties", default=True)
    export_materials: bpy.props.BoolProperty(name="Export Materials", default=True)
    export_lights: bpy.props.BoolProperty(name="Export Lights", default=True)
    export_cameras: bpy.props.BoolProperty(name="Export Cameras", default=True)
    export_cubemaps: bpy.props.BoolProperty(name="Export Cubemaps", default=True)
    export_speakers: bpy.props.BoolProperty(name="Export Speakers", default=True)

    force_32_bit_indices: bpy.props.BoolProperty(
        name="Force 32 bit indices", 
        default=False, 
        description="todo - When this setting is off meshes in the scene can choose between exporting with 32 bit and 16 bit indices. When this setting is turned on all mesh indices in the exported model are guaranteed to use 32 bit integers.\n\nThis may result in larger files, but if the target renderer requires 32 bit indices, it will mean no conversions from 16 bit to 32 bit will be necessary"
        )
    
    force_skinned_vertices: bpy.props.BoolProperty(
        name="Force skinned vertices", 
        default=False, 
        description="todo - When this setting is off vertices may either be exported with a single parent node index field, or with 4 parent node index fields and weights. This depends upon whether their mesh is parented to an armature and has the relevant skinning data. If this setting is on, all vertices will be exported with 4 parent node index fields and weights"
        )