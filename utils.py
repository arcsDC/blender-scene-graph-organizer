import bpy

def get_selected_objects():
    return [o for o in bpy.context.selected_objects if o.type in {'MESH', 'EMPTY'}]

def find_nearest_parent(obj, max_depth):
    best = None
    best_dist = float('inf')
    for other in bpy.data.objects:
        if other == obj or other.parent:
            continue
        dist = (obj.location - other.location).length
        if dist < best_dist:
            best_dist = dist
            best = other
    return best

def would_create_cycle(obj, potential_parent):
    current = potential_parent
    while current:
        if current == obj:
            return True
        current = current.parent
    return False
