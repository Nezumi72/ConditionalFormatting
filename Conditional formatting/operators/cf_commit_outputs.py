import bpy
from .cf_rule_ops import execute_all_rules as execute_all_rules


class OBJECT_OT_cf_commit(bpy.types.Operator):
    bl_idname = 'object.cf_commit'
    bl_label = "Commit"

    @classmethod
    def poll(cls, context):
        props = context.window_manager.cf_props_pg
        return props.enable_rules
    
    def execute(self, context):
        props = context.window_manager.cf_props_pg
        props.affected_objs.clear()
        for obj in bpy.data.objects:
            item = props.affected_objs.add()
            item.obj = obj
            item.display = obj.display_type
            item.obj_col = obj.color
        return {'FINISHED'}


classes = [
    OBJECT_OT_cf_commit,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
