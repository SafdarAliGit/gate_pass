# Copyright (c) 2024, Tech Ventures and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CheckIn(Document):

    def on_submit(self):

        if self.employee:
            checkins = frappe.db.sql("""
                    SELECT name FROM `tabEmployee Checkin`
                    WHERE employee = %s AND DATE(time) = %s
                """, (self.employee, frappe.utils.nowdate()), as_dict=True)

            if not checkins:
                # Create a new Employee Checkin document
                ec = frappe.new_doc("Employee Checkin")
                ec.employee = self.employee
                ec.log_type = self.log_type
                ec.time =  frappe.utils.now()
                ec.device_id = self.employee_id
                ec.insert()  # Save the new Employee Checkin document
            else:
                # Raise an error if an Employee Checkin already exists for today
                frappe.throw(f"Employee Checkin for {self.employee} already exists on {frappe.utils.nowdate()}")
