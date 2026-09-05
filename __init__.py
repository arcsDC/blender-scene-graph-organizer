bl_info = {
    "name": "Scene Graph Organizer",
    "author": "Dev",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Scene Organizer",
    "description": "Automates scene cleanup: batch rename, auto-parent, flatten, validate, export.",
    "category": "Object",
}

import bpy
from . import properties, operators, ui_panels

classes = (
    properties.SceneOrganizerSettings,
    operators.OT_BatchRename,
    operators.OT_AutoParent,
    operators.OT_FlattenHierarchy,
    operators.OT_ValidateNames,
    operators.OT_BatchExport,
    ui_panels.SceneOrganizerPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.organizer_settings = bpy.props.PointerProperty(type=properties.SceneOrganizerSettings)

def unregister():
    del bpy.types.Scene.organizer_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
