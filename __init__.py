bl_info = {
    "name": "Sequoia-Exporter",
    "blender": (3, 4, 1),
    "category": "Import-Export",
    "location": "view3D",
	"author": "Zak Goedegebuur",
    "version": (1,0,0),
}

import bpy

from .sqo_pnl import SequoiaMeshPanel
from .sqo_test_export import SequoiaTestExport
from .sqo_props import (SequoiaObjectProperties, SequoiaSceneProperties)
from .sqo_export import (SequoiaExportSQO, SQO_PT_export_include_settings, SQO_PT_export_mesh_settings)

classes = (
    SequoiaObjectProperties, 
    SequoiaSceneProperties, 
    SequoiaMeshPanel, 
    SequoiaTestExport, 
    SequoiaExportSQO, 
    SQO_PT_export_include_settings,
    SQO_PT_export_mesh_settings
    )

def menu_function_export(self, context):
    self.layout.operator(SequoiaExportSQO.bl_idname,
                         text="SQO (.sqo)")

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_export.append(menu_function_export)
    bpy.types.Object.sequoia = bpy.props.PointerProperty(type=SequoiaObjectProperties)
    bpy.types.Scene.sequoia = bpy.props.PointerProperty(type=SequoiaSceneProperties)

def unregister():
    for c in classes:
      bpy.utils.unregister_class(c)
    del bpy.types.Object.sequoia
    del bpy.types.Scene.sequoia