import frappe
from frappe.model.document import Document


class RestorationStatus(Document):
    def validate(self):
        if not self.status_name:
            frappe.throw("Status Name is required")
