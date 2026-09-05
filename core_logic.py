import re
from mathutils import Matrix

def generate_name(template, parent_name, index, obj_type):
    return template.format(parent=parent_name, index=index, type=obj_type)

def check_collision(name, existing_names):
    return name in existing_names

def resolve_collision(name, existing_names, mode):
    if mode == "SKIP":
        return None
    i = 1
    new_name = f"{name}_{i}"
    while new_name in existing_names:
        i += 1
        new_name = f"{name}_{i}"
    return new_name

def validate_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False

def merge_transforms(parent_matrix, child_matrix):
    return parent_matrix @ child_matrix
