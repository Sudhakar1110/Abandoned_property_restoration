import frappe
from frappe.model.document import Document


class Engineer(Document):
    def validate(self):
        if not self.engineer_name:
            frappe.throw("Engineer Name is required")
