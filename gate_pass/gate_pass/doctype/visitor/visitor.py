import frappe
from frappe.model.document import Document


class Visitor(Document):
    pass



    # def before_save(self):
    #     existing_visitor = frappe.get_all("Visitor", filters={"cnic": self.cnic, "block_list": 1},
    #                                       fields=["name"], limit=1)
    #     if existing_visitor and self.block_list == 1:
    #         frappe.throw(frappe._("A visitor {0} with CNIC {1} is already in the block list.").format(self.visitor_name,
    #                                                                                                   self.cnic))
    #     if existing_visitor and self.block_list == 0:
    #         doc = frappe.get_doc("Visitor", existing_visitor[0].name)
    #         doc.block_list = 0
    #         doc.save()
    #         frappe.db.commit()
