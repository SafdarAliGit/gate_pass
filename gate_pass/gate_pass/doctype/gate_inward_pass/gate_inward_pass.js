// Copyright (c) 2024, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Inward Pass', {
    refresh: function (frm) {
        if (frm.is_new()) {
            frm.set_value('date', frappe.datetime.now_datetime());
        }
        frm.set_value('entry_no', frm.doc.name);
        frm.fields_dict['po_no'].get_query = function (doc) {
            return {
                filters: [
                    ["Purchase Order", "supplier", "=", doc.party], ["Purchase Order", "docstatus", "=", 1]
                ]

            };
        };
        frm.set_query('item_code', 'gate_inward_pass_items', function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Item", "item_group", "=", doc.gate_pass_inward_type]
                ]
            };
        });
    },
    get_items: function (frm) {
        var po_no = frm.doc.po_no;
        fetch_gip_items(frm, po_no);

    },

});


function fetch_gip_items(frm, po_no) {
    if (po_no) {
        // Clear existing data before adding new entries
        frm.clear_table("gate_inward_pass_items");

        frappe.call({
            method: "gate_pass.gate_pass.doctype.utils.fetch_items.fetch_gip_items",
            args: {
                po_no: po_no
            },
            callback: function (response) {
                if (response.message.poi) {
                    response.message.poi.forEach(function (p) {
                        let entry = frm.add_child("gate_inward_pass_items");
                        entry.item_code = p.item_code,
                            entry.qty = p.qty,
                            entry.uom = p.uom

                    });
                }
                frm.refresh_field('gate_inward_pass_items');
            }
        });
    }
}
