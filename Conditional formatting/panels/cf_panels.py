import bpy


class FILE_UL_slots(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, _index):
        slot = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if slot:
                minor = 0.15
                box = layout.box()
                row = box.row().split(factor=minor)
                col = row.column()
                col.prop(slot, "name", text="", emboss=False)
                col = row.column()
                col.prop(slot, "evaluate", text="", emboss=False)
                col.prop(slot, "condition", text="", emboss=False)
                if slot.condition in ["OBJECT", "MATERIAL", ]:
                    col.prop(slot, "col_value", text="", emboss=True)
                else:
                    col.prop(slot, "value", text="", emboss=True)
                col = row.column()
                col.prop(slot, "output", text="", emboss=False)
                if not slot.lock_affected:
                    icon = 'UNLOCKED'
                else:
                    icon = 'LOCKED'
                if slot.output == "OBJCOLOR":
                    col.prop(slot, "op_col", text="", emboss=True)
                else:
                    col.label(text="")
                row = col.row()
                row.prop(slot, "lock_affected", text="", icon=icon, emboss=True, icon_only=True)
                row.separator()
                row.prop(slot, "enable", text="", emboss=True, icon_only=True)
            else:
                layout.label(text="", translate=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")


class VIEW3D_PT_CFMain(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "C-Format"
    bl_idname = "VIEW3D_PT_CFMain"
    bl_label = "Main Panel"

    def draw(self, context):
        layout = self.layout
        props = context.window_manager.cf_props_pg
        layout.prop(props, "enable_rules", text="Enable Rule Set", toggle=1)
        row = layout.row()
        row.label(text="Rule Application")
        row.prop(props, "limit_selectable", text="User Choice", expand=True)
        row = layout.row()
        row = layout.row().split(factor=0.18)
        row.label(text="Rule")
        row.label(text="Criteria")
        row.label(text="Output")
        is_sortable = len(props.rules) > 1
        rows = 3
        if is_sortable:
            rows = 5
        row = layout.row()
        row.template_list("FILE_UL_slots", "", props, "rules", props, "act_rule_idx", rows=rows)
        col = row.column(align=True)
        add_rule = col.operator("ui.cf_panel_ops", icon='ADD', text="")
        add_rule.operation_type = "add"
        if props.rules:
            del_act = col.operator("ui.cf_panel_ops", icon='REMOVE', text="")
            del_act.operation_type = "del_act"
            del_act.idx = props.act_rule_idx
        if is_sortable:
            col.separator()
            move_up = col.operator("ui.cf_panel_ops", icon='TRIA_UP', text="")
            move_up.operation_type = "move_up"
            move_up.idx = props.act_rule_idx
            move_dn = col.operator("ui.cf_panel_ops", icon='TRIA_DOWN', text="")
            move_dn.operation_type = "move_dn"
            move_dn.idx = props.act_rule_idx
        layout.operator("file.cf_gen_report", text="Generate Report")
        row = layout.row()
        row.label(text="Select")
        sel = row.operator("object.cf_select", text="Last Affected")
        sel.operation_type = 'last'
        sel = row.operator("object.cf_select", text="All Affected")
        sel.operation_type = 'all'
        layout.operator("object.cf_commit", text="Apply Effects")


classes = [
    FILE_UL_slots,
    VIEW3D_PT_CFMain,
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
