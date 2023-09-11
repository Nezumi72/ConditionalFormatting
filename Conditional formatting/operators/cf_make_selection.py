import bpy
from .cf_rule_ops import execute_rule as execute_rule


class OBJECT_OT_cf_select(bpy.types.Operator):
    bl_idname = 'object.cf_select'
    bl_label = "Set Selected"

    operation_type: bpy.props.EnumProperty(
        name="selection_type",
        items=(
            ("all", "All Affected", "All affected by all rules"),
            ("last", "Last Affected", "All affected by all rules"),
        ),
        default="all",
    )

    @classmethod
    def poll(cls, context):
        props = context.window_manager.cf_props_pg
        return props.enable_rules
    
    def execute(self, context):
        props = context.window_manager.cf_props_pg
        me_affects = []
        if self.operation_type == 'all':
            for idx, rule in enumerate(props.rules):
                me = props.rules[idx]
                for ob in execute_rule(me):
                    me_affects.append(ob)
        else:
            for idx, rule in enumerate(props.rules):
                me = props.rules[idx]
                if me.enable:
                    me_affects = [ob for ob in execute_rule(me)]
        if not me_affects:
            return {'CANCELLED'}
        bpy.ops.object.select_all(action='DESELECT')
        context.view_layer.objects.active = me_affects[0]
        for ob in me_affects:
            ob.select_set(True)
        return {'FINISHED'}


classes = [
    OBJECT_OT_cf_select,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
