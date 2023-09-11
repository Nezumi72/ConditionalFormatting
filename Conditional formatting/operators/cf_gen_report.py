import bpy
from .cf_rule_ops import execute_rule as execute_rule
from mathutils import Vector


class FILE_OT_cf_gen_report(bpy.types.Operator):
    bl_idname = 'file.cf_gen_report'
    bl_label = "Rule Ops"

    @classmethod
    def poll(cls, context):
        props = context.window_manager.cf_props_pg
        return props.enable_rules
    
    def execute(self, context):
        props = context.window_manager.cf_props_pg
        txtname = 'CF Report'
        if txtname not in bpy.data.texts:
            ntxt = bpy.data.texts.new(txtname)
        else:
            ntxt = bpy.data.texts[txtname]
            ntxt.clear()
        ntxt.write(f"-- Conditional Formatting Report --\n\n")
        ntxt.write(f"-- Settings --\n\n")
        ntxt.write(f"-- Selection limit to: {props.limit_selectable} --\n\n")
        ntxt.write(f"-- Original State objects --\n\n")
        ori_objs = [ob.obj for ob in props.affected_objs]
        ntxt.write(f"{str(list(ori_objs))}\n\n")
        ntxt.write(f"-- Objects added after original state --\n\n")
        objs_added = [obj for obj in bpy.data.objects if obj not in ori_objs]
        ntxt.write(f"{str(list(objs_added))}\n\n")
        ntxt.write(f"-- Rules --\n\n")
        for idx, rule in enumerate(props.rules):
            me = props.rules[idx]
            ntxt.write(f"Index: {idx}\t Name: {me.name}\n")
            ntxt.write(f"\tType: {me.evaluate}\n")
            ntxt.write(f"\tCondition: {me.condition}\n")
            if me.condition in ['OBJECT', 'MATERIAL']:
                ntxt.write(f"\tcolor: {Vector(me.col_value)}\n")
            else:
                ntxt.write(f"\tValue: {me.value}\n")
            ntxt.write(f"\tOutput: {me.output}\n")
            if me.output == "OBJCOLOR":
                ntxt.write(f"\tOutput Color: {me.op_col}\n")
            ntxt.write(f"\tLock Objs at this lvl: {me.lock_affected}\n")
            ntxt.write(f"\tEnabled: {me.enable}\n\n")
            me_affects = execute_rule(me)
            ntxt.write(f"Affected Objects:\n")
            if me_affects:
                ntxt.write(f"{str(list(me_affects))}\n\n")
            else:
                ntxt.write("\n\n")
        return {'FINISHED'}


classes = [
    FILE_OT_cf_gen_report,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
