import frappe
from frappe.model.document import Document


class Department(Document):
    def validate(self):
        if not self.department_name:
            frappe.throw("Department Name is required")
