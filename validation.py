import bpy
import re

def get_violations(pattern):
    try:
        regex = re.compile(pattern)
    except re.error:
        return []
    violations = []
    for obj in bpy.data.objects:
        if not regex.match(obj.name):
            violations.append(obj)
    return violations
