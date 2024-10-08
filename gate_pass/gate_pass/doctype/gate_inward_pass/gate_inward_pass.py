import frappe
from frappe.model.document import Document


class GateInwardPass(Document):
    def on_submit(self):
        # Check if 'po_no' exists
        if self.po_no:
            # Fetch the Purchase Order document
            po = frappe.get_doc("Purchase Order", self.po_no)
            gate_inward_pass_items = self.gate_inward_pass_items

            # Create a new Purchase Receipt document
            pr = frappe.new_doc("Purchase Receipt")
            pr.supplier = po.supplier
            pr.supplier_address = po.supplier_address
            pr.supplier_name = po.supplier_name
            pr.posting_date = po.transaction_date
            pr.posting_time = frappe.utils.now()
            pr.ref_no = self.name
            pr.ref_doctype = "Gate Inward Pass"

            # Add items to the Purchase Receipt
            for item in gate_inward_pass_items:
                pr.append("items", {
                    "item_code": item.item_code,
                    "stock_uom": item.uom,
                    "qty": item.qty,
                    "rate": item.rate,
                    "amount": item.qty * item.rate
                })

            try:
                # Save and submit the Purchase Receipt
                pr.insert()
                pr.submit()

                # Update the Gate Inward Pass with the Purchase Receipt reference
                self.db_set("ref_no", pr.name)
                self.db_set("ref_doctype", "Purchase Receipt")

            except Exception as e:
                # Handle any errors during the creation of the Purchase Receipt
                frappe.throw(frappe._("Error creating Purchase Receipt: {0}".format(str(e))))

        # No Purchase Order reference; only submit the Gate Inward Pass
        # Further logic for only submitting the Gate Inward Pass (if any) can be added here
