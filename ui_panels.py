import bpy

class SceneOrganizerPanel(bpy.types.Panel):
    bl_label = "Scene Organizer"
    bl_idname = "SCENE_PT_organizer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Organizer"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.organizer_settings
        layout.prop(settings, "rename_template")
        layout.prop(settings, "collision_mode")
        layout.prop(settings, "regex_pattern")
        layout.prop(settings, "export_format")
        layout.prop(settings, "export_path")
        layout.prop(settings, "dry_run")
        layout.operator("object.batch_rename", icon='FILE_REFRESH')
        layout.operator("object.auto_parent", icon='OUTLINER')
        layout.operator("object.flatten_hierarchy", icon='ARROW_DOWN')
        layout.operator("object.validate_names", icon='CHECKMARK')
        layout.operator("object.batch_export", icon='EXPORT')
