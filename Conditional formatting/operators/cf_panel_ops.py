import bpy
from .cf_rule_ops import execute_rule as execute_rule


class OBJECT_OT_cf_panel_ops(bpy.types.Operator):
    bl_idname = 'ui.cf_panel_ops'
    bl_label = "Rule Ops"

    operation_type: bpy.props.EnumProperty(
        name="operation_type",
        items=(
            ("add", "add", "Add new rule"),
            ("del_act", "del_act", "Remove Selected rule from list"),
            ("move_up", "move_up", "Move Selected rule up"),
            ("move_dn", "move_dn", "Move Selected rule down"),
        ),
        default="add",
    )
    idx: bpy.props.IntProperty(default=-1)

    @classmethod
    def poll(cls, context):
        props = context.window_manager.cf_props_pg
        return props.enable_rules

    def execute(self, context):
        props = context.window_manager.cf_props_pg
        if self.operation_type == "add":
                me = props.rules.add()
                me.name = "Rule"
                execute_rule(me)
        elif self.operation_type == "del_act":
            props.rules.remove(self.idx)
            props.act_rule_idx = min(max(0, self.idx - 1), len(props.rules) - 1)
            if len(props.rules) == 0:
                props.enable_rules = False
                props.enable_rules = True
        elif self.operation_type == "move_up" and self.idx > 0:
            props.act_rule_idx = self.idx - 1
            props.rules.move(self.idx, self.idx-1)
        elif self.operation_type == "move_dn" and self.idx < len(props.rules)-1:
            props.act_rule_idx = self.idx + 1
            props.rules.move(self.idx, self.idx+1)
        ori_obj = context.object
        context.view_layer.objects.active = None
        context.view_layer.objects.active = ori_obj
        return {'FINISHED'}

classes = [
    OBJECT_OT_cf_panel_ops,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
