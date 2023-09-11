import bpy
from mathutils import Vector


conditions = [
    {
        "type": "Name",
        "conditions": [
            "Is",
            "Is Not",
            "Starts With",
            "Ends With",
            "Contains"
        ],
        "function": "evaluate_name"
    },
    {
        "type": "Belongs To",
        "conditions": [
            "Collection",
            "Recursive",
        ],
        "function": "evaluate_belongs_to"
    },
    {
        "type": "Poly Count",
        "conditions": [
            "Greater Than",
            "Less Than"
        ],
        "function": "evaluate_polygon_count"
    },
    {
        "type": "Color",
        "conditions": [
            "Object",
            "Material",
        ],
        "function": "evaluate_color"
    },
]

def get_avail_objs(condition, value, col_value):
    props = bpy.context.window_manager.cf_props_pg
    avail_objs = []
    if props.limit_selectable == 'ALL':
        avail_objs = [obj for obj in bpy.context.scene.objects]
    elif props.limit_selectable == 'SELECTABLE':
        avail_objs = [obj for obj in bpy.context.selectable_objects]
    for idx, rule in enumerate(props.rules):
        me = props.rules[idx]
        if me.condition == condition and me.value == value:
            break
        if me.lock_affected and me.enable:
            me_affects = execute_rule(me)
            avail_objs = list(set(avail_objs)-set(me_affects))
    return avail_objs

def evaluate_color(condition, value, col_value):
    avail_objs = get_avail_objs(condition, value, col_value)
    if condition == "OBJECT":
        return [obj for obj in avail_objs if Vector(obj.color) == Vector(col_value)]
    elif condition == "MATERIAL":
        objs = []
        for obj in avail_objs:
            if obj.material_slots:
                for mat in obj.material_slots:
                    if Vector(mat.material.diffuse_color) == Vector(col_value):
                        objs.append(obj)
                        break
        return objs
    else:
        return []

def evaluate_name(condition, value, col_value):
    avail_objs = get_avail_objs(condition, value, col_value)
    if condition == get_enum_string("Is"):
        return [obj for obj in avail_objs if obj.name == value]
    elif condition == get_enum_string("Is Not"):
        return [obj for obj in avail_objs if obj.name != value]
    elif condition == get_enum_string("Starts With"):
        return [obj for obj in avail_objs if obj.name.startswith(value)]
    elif condition == get_enum_string("Ends With"):
        return [obj for obj in avail_objs if obj.name.endswith(value)]
    elif condition == get_enum_string("Contains"):
        return [obj for obj in avail_objs if value in obj.name]
    else:
        return []

def evaluate_belongs_to(condition, value, col_value):
    avail_objs = get_avail_objs(condition, value, col_value)
    if condition == get_enum_string("Collection") and bpy.data.collections.get(value):
        return [obj for obj in avail_objs \
            if obj.name in bpy.data.collections[value].objects]
    elif condition == get_enum_string("Recursive") and bpy.data.collections.get(value):
        objs = []
        start_coll = bpy.data.collections.get(value)
        for ob in start_coll.objects:
            if ob in avail_objs:
                objs.append(ob)
        for child_coll in start_coll.children_recursive:
            for ob in child_coll.objects:
                if ob in avail_objs:
                    objs.append(ob)
        return objs
    else:
        return []

def evaluate_polygon_count(condition, value, col_value):
    avail_objs = get_avail_objs(condition, value, col_value)
    if condition == get_enum_string("Greater Than") and value.isnumeric():
        return [obj for obj in avail_objs \
            if obj.type == 'MESH' and \
                len(obj.data.polygons) > int(value)]
    elif condition == get_enum_string("Less Than") and value.isnumeric():
        return [obj for obj in avail_objs \
            if obj.type == 'MESH' and \
                len(obj.data.polygons) < int(value)]
    else:
        return []

def get_enum_string(text):
    return text.upper().replace(" ",  "_")

def get_conditions(self, context):
    for condition in conditions:
        if condition["type"].upper().replace(" ",  "_") == self.evaluate:
            return [(get_enum_string(con), con, "", i+1) \
                for i, con in enumerate(condition["conditions"])]

def get_evaluator(condition_type):
    for condition in conditions:
        if get_enum_string(condition["type"]) == condition_type:
            return condition["function"]

def execute_rule(rule):
    props = bpy.context.window_manager.cf_props_pg
    evaluator = globals()[get_evaluator(rule.evaluate)]
    for obj in evaluator(rule.condition, rule.value, rule.col_value):
        if rule.enable:
            if rule.output != "OBJCOLOR":
                obj.display_type = rule.output
            else:
                obj.color = rule.op_col
    if rule.enable and props.enable_rules:
        return evaluator(rule.condition, rule.value, rule.col_value)
    else:
        return []

def execute_all_rules(scene):
    for rule in bpy.context.window_manager.cf_props_pg.rules:
        if rule.enable:
            execute_rule(rule)

classes = [
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
