// Copyright (c) 2024, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Visitor', {
    refresh: function (frm) {
        if (frm.is_new()) {
            frm.set_value('date', frappe.datetime.now_datetime());
        }
        frm.set_value('visitor_no', frm.doc.name);
    },

    after_save: function (frm) {
        frappe.set_route("Form", "Visitor", "new-visitor");
    }
});
