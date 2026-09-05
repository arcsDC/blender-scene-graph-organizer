import bpy
from . import core_logic, utils, validation, export_handler

class OT_BatchRename(bpy.types.Operator):
    bl_idname = "object.batch_rename"
    bl_label = "Batch Rename"
    bl_description = "Rename selected objects using the configured template"

    def execute(self, context):
        settings = context.scene.organizer_settings
        objects = utils.get_selected_objects()
        if not objects:
            self.report({'WARNING'}, "No valid objects selected")
            return {'CANCELLED'}
        
        existing = {o.name for o in bpy.data.objects}
        for i, obj in enumerate(objects):
            parent_name = obj.parent.name if obj.parent else "ROOT"
            new_name = core_logic.generate_name(settings.rename_template, parent_name, i, obj.type)
            
            if core_logic.check_collision(new_name, existing):
                new_name = core_logic.resolve_collision(new_name, existing, settings.collision_mode)
            
            if new_name:
                obj.name = new_name
                existing.add(new_name)
        return {'FINISHED'}

class OT_AutoParent(bpy.types.Operator):
    bl_idname = "object.auto_parent"
    bl_label = "Auto Parent"
    bl_description = "Parent unparented objects to their nearest neighbor"

    def execute(self, context):
        settings = context.scene.organizer_settings
        unparented = [o for o in bpy.data.objects if not o.parent]
        if not unparented:
            self.report({'INFO'}, "No unparented objects found")
            return {'CANCELLED'}
            
        for obj in unparented:
            parent = utils.find_nearest_parent(obj, settings.max_depth)
            if parent and not utils.would_create_cycle(obj, parent):
                obj.parent = parent
        return {'FINISHED'}

class OT_FlattenHierarchy(bpy.types.Operator):
    bl_idname = "object.flatten_hierarchy"
    bl_label = "Flatten Hierarchy"
    bl_description = "Merge child objects into their parents"

    def execute(self, context):
        # Iterate over a copy of the list to avoid modification during iteration
        for obj in list(bpy.data.objects):
            if obj.children:
                for child in list(obj.children):
                    # Only merge if child has no modifiers or materials to avoid data loss
                    if not child.modifiers and not child.data.materials:
                        obj.matrix_world = core_logic.merge_transforms(obj.matrix_world, child.matrix_world)
                        bpy.data.objects.remove(child, do_unlink=True)
        return {'FINISHED'}

class OT_ValidateNames(bpy.types.Operator):
    bl_idname = "object.validate_names"
    bl_label = "Validate Names"
    bl_description = "Highlight objects with names violating the regex pattern"

    def execute(self, context):
        settings = context.scene.organizer_settings
        if not core_logic.validate_regex(settings.regex_pattern):
            self.report({'ERROR'}, "Invalid Regex Pattern")
            return {'CANCELLED'}
            
        violations = validation.get_violations(settings.regex_pattern)
        if not violations:
            self.report({'INFO'}, "All names are valid")
            return {'FINISHED'}
            
        # Select only the violating objects
        bpy.ops.object.select_all(action='DESELECT')
        for v in violations:
            v.select_set(True)
        self.report({'WARNING'}, f"Found {len(violations)} naming violations")
        return {'FINISHED'}

class OT_BatchExport(bpy.types.Operator):
    bl_idname = "object.batch_export"
    bl_label = "Batch Export"
    bl_description = "Export selected objects to the configured path"

    def execute(self, context):
        settings = context.scene.organizer_settings
        try:
            export_handler.export_selection(settings.export_path, settings.export_format)
            self.report({'INFO'}, "Export completed")
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}
