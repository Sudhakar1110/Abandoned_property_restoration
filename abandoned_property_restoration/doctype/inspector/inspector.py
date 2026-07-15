import frappe
from frappe.model.document import Document


class Inspector(Document):
    def validate(self):
        if not self.inspector_name:
            frappe.throw("Inspector Name is required")
