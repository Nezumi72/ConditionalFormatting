import bpy
from mathutils import Vector
from ..operators.cf_rule_ops import execute_all_rules as execute_all_rules
from ..operators.cf_rule_ops import get_enum_string as get_enum_string
from ..operators.cf_rule_ops import conditions as conditions
from ..operators.cf_rule_ops import get_conditions as get_conditions


def upd_enable_single(self, context):
    props = context.window_manager.cf_props_pg
    if not props.enable_rules:
        return
    idx = []
    for i, h in enumerate(bpy.app.handlers.depsgraph_update_post):
        if hasattr(h, "conditional"):
            idx.append(i)
    for i in idx:
        bpy.app.handlers.depsgraph_update_post.pop(i)
    for item in context.window_manager.cf_props_pg.affected_objs:
        ob = bpy.data.objects.get(item.obj.name)
        if ob:
            ob.display_type = item.display
            ob.color = item.obj_col
    for handler in bpy.app.handlers.depsgraph_update_post:
        if hasattr(handler, "conditional"):
            bpy.app.handlers.depsgraph_update_post.remove(handler)
            break
    bpy.app.handlers.depsgraph_update_post.append(execute_all_rules)
    bpy.app.handlers.depsgraph_update_post[-1].__dict__["conditional"] = True

def upd_enable_rules(self, context):
    if self.enable_rules:
        for handler in bpy.app.handlers.depsgraph_update_post:
            if hasattr(handler, "conditional"):
                bpy.app.handlers.depsgraph_update_post.remove(handler)
                break
        bpy.app.handlers.depsgraph_update_post.append(execute_all_rules)
        bpy.app.handlers.depsgraph_update_post[-1].__dict__["conditional"] = True
        self.affected_objs.clear()
        for obj in bpy.data.objects:
            item = self.affected_objs.add()
            item.obj = obj
            item.display = obj.display_type
            item.obj_col = obj.color
    else:
        idx = []
        for i, h in enumerate(bpy.app.handlers.depsgraph_update_post):
            idx.append(i)
        for i in idx:
            bpy.app.handlers.depsgraph_update_post.pop(i)
        for item in self.affected_objs:
            ob = bpy.data.objects.get(item.obj.name)
            if ob:
                ob.display_type = item.display
                ob.color = item.obj_col


class PROPS_PG_ConditionalRule(bpy.types.PropertyGroup):
    evaluate: bpy.props.EnumProperty(
        items=[
            (get_enum_string(condition["type"]), condition["type"], "", i+1) \
                for i, condition in enumerate(conditions)
        ],
        default=1,
        update=upd_enable_single,
    )
    condition: bpy.props.EnumProperty(
        items=get_conditions,
        default=1,
        update=upd_enable_single,
    )
    value: bpy.props.StringProperty(
        name="value",
        description="item name",
        update=upd_enable_single,
    )
    col_value: bpy.props.FloatVectorProperty(
        name="col_value",
        description="color",
        size=4,
        min=0,
        max=1,
        subtype='COLOR',
        default=[0.800000, 0.800000, 0.800000, 1.000000],
        update=upd_enable_single,
    )
    output: bpy.props.EnumProperty(
        items=[
            ("SOLID", "Display as Solid", "Display as Solid", 'SHADING_SOLID', 1),
            ("WIRE", "Display as Wire", "Display as Wire", 'SHADING_WIRE', 2),
            ("BOUNDS", "Display as Bounds", "Display as Bounds", 'SHADING_BBOX', 3),
            ("TEXTURED", "Display as Textured", "Display as Textured", 'SHADING_TEXTURE', 4),
            ("OBJCOLOR", "Object color", "Object color", 'EYEDROPPER', 5),
        ],
        update=upd_enable_single,
    )
    lock_affected: bpy.props.BoolProperty(
        name="lock_affected",
        description="Lock affected at this rule",
        default=False,
        update=upd_enable_single,
    )
    enable: bpy.props.BoolProperty(
        name="enable",
        description="Show/hide evaluation",
        default=True,
        update=upd_enable_single,
    )
    op_col: bpy.props.FloatVectorProperty(
        name="op_col",
        description="color",
        size=4,
        min=0,
        max=1,
        subtype='COLOR',
        default=[0.800000, 0.800000, 0.800000, 1.000000],
    )


class PROPS_PG_OrignalState(bpy.types.PropertyGroup):
    obj: bpy.props.PointerProperty(
        type=bpy.types.Object)
    display: bpy.props.StringProperty(
        name="display",
        description="Original object display type",
    )
    obj_col: bpy.props.FloatVectorProperty(
        name="obj_col",
        description="color",
        size=4,
        min=0,
        max=1,
        subtype='COLOR',
        default=[0.800000, 0.800000, 0.800000, 1.000000],
    )


class PROPS_PG_ConditionalFormatting(bpy.types.PropertyGroup):
    enable_rules: bpy.props.BoolProperty(
        name="Enaable Rule Set",
        description="Show/hide evaluation",
        default=False,
        update=upd_enable_rules,
    )
    limit_selectable: bpy.props.EnumProperty(
        items=[
            ("ALL", "All Objects", "All Objects"),
            ("SELECTABLE", "Selectable Objects", "Selectable Objects"),
        ],
        update=upd_enable_single,
    )
    rules: bpy.props.CollectionProperty(
        type=PROPS_PG_ConditionalRule,
    )
    act_rule_idx: bpy.props.IntProperty(
        name="act_rule_idx",
        description="Active Index",
        default=0,
        min=0,
    )
    affected_objs: bpy.props.CollectionProperty(
        type=PROPS_PG_OrignalState
    )


classes = [
    PROPS_PG_ConditionalRule,
    PROPS_PG_OrignalState,
    PROPS_PG_ConditionalFormatting,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.cf_props_pg = bpy.props.PointerProperty(
        type=PROPS_PG_ConditionalFormatting)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.cf_props_pg
