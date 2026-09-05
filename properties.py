import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty

class SceneOrganizerSettings(bpy.types.PropertyGroup):
    rename_template: StringProperty(default="{parent}_{index}_{type}")
    collision_mode: EnumProperty(items=[("SKIP", "Skip", ""), ("SUFFIX", "Suffix", "")], default="SUFFIX")
    regex_pattern: StringProperty(default="^[A-Z][a-zA-Z0-9_]*$")
    export_format: EnumProperty(items=[("FBX", "FBX", ""), ("OBJ", "OBJ", "")], default="FBX")
    export_path: StringProperty(default="//exports/", subtype="DIR_PATH")
    dry_run: BoolProperty(default=True)
    max_depth: IntProperty(default=10, min=1)
