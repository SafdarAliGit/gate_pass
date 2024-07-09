import frappe
from frappe.model.document import Document


class GateInwardPass(Document):
    def on_submit(self):
        po = frappe.get_doc("Purchase Order", self.po_no)
        gate_inward_pass_items = self.gate_inward_pass_items
        pr = frappe.new_doc("Purchase Receipt")
        pr.supplier = po.supplier
        pr.supplier_address = po.supplier_address
        pr.supplier_name = po.supplier_name
        pr.posting_date = po.transaction_date
        pr.posting_time = frappe.utils.now()
        pr.ref_no = self.name
        pr.ref_doctype = "Gate Inward Pass"
        for item in gate_inward_pass_items:
            pr.append("items", {
                "item_code": item.item_code,
                "stock_uom": item.uom,
                "qty": item.qty,
                "rate": item.rate,
                "amount": item.qty * item.rate
            })

        try:

            pr.submit()
            frappe.db.commit()
            self.ref_no = pr.name
            self.ref_doctype = "Purchase Receipt"
        except Exception as e:
            frappe.throw(frappe._("Error creating Purchase Receipt: {0}".format(str(e))))
