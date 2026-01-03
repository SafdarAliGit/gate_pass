// Copyright (c) 2024, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Outward Pass', {
    refresh: function (frm) {
        if (frm.is_new()) {
            frm.set_value('date', frappe.datetime.now_datetime());
        }
        frm.fields_dict['dn_no'].get_query = function (doc) {
            return {
                filters: [
                    ["Delivery Note", "customer", "=", doc.customer], ["Delivery Note", "docstatus", "=", 1]
                ]

            };
        };
        frm.fields_dict['po_no'].get_query = function (doc) {
            return {
                filters: [
                    ["Purchase Order", "supplier", "=", doc.supplier], ["Purchase Order", "docstatus", "=", 1]
                ]

            };
        };
        frm.fields_dict['prr_no'].get_query = function (doc) {
            return {
                filters: [
                    ["Purchase Receipt", "supplier", "=", doc.supplier], ["Purchase Receipt", "docstatus", "=", 1],["Purchase Receipt", "is_return", "=", 1]
                ]

            };
        };
        frm.fields_dict['transporter'].get_query = function (doc) {
            return {
                filters: [
                    ["Supplier", "supplier_group", "=", "Transporter"]
                ]

            };
        };
    },
    get_items: function (frm) {
        let no = null;
        let source = null;

        if (frm.doc.dn_no) {
            no = frm.doc.dn_no;
            source = "DN";
        } else if (frm.doc.po_no) {
            no = frm.doc.po_no;
            source = "PO";
        } else if (frm.doc.prr_no) {
            no = frm.doc.prr_no;
            source = "PRR";
        }

        if (no) {
            fetch_gop_items(frm, no, source);
        } else {
            frappe.msgprint(__('Please select at least one reference'));
        }
    },
});

function fetch_gop_items(frm, no,source) {
    if (no) {
        
        // Clear existing data before adding new entries
        frm.clear_table("gate_outward_pass_items");

        frappe.call({
            method: "gate_pass.gate_pass.doctype.utils.fetch_items.fetch_gop_items",
            args: {
                no: no,
                source: source
            },
            callback: function (response) {
                if (response.message.dni) {
                    response.message.dni.forEach(function (p) {
                        let entry = frm.add_child("gate_outward_pass_items");
                        entry.item_code = p.item_code,
                            entry.qty = p.qty,
                            entry.uom = p.uom,
                            entry.description = p.description

                    });
                }
                frm.refresh_field('gate_outward_pass_items');
            }
        });
    }
}
