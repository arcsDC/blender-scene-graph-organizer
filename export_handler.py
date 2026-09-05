import bpy
import os

def export_selection(path, fmt):
    # Ensure path is absolute
    if not os.path.isabs(path):
        # Blender relative paths start with //
        if path.startswith("//"):
            path = bpy.path.abspath(path)
        else:
            path = os.path.abspath(path)
            
    os.makedirs(path, exist_ok=True)
    
    selected = bpy.context.selected_objects
    if not selected:
        raise ValueError("No objects selected for export")

    for obj in selected:
        filename = f"{obj.name}.{fmt.lower()}"
        filepath = os.path.join(path, filename)
        
        # Ensure only this object is selected for export
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        if fmt == "FBX":
            bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True)
        elif fmt == "OBJ":
            bpy.ops.wm.obj_export(filepath=filepath, export_selected_objects=True)
        else:
            raise ValueError(f"Unsupported export format: {fmt}")
