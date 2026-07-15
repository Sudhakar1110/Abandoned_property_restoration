import frappe
from frappe.model.document import Document


class Contractor(Document):
    def validate(self):
        if not self.contractor_name:
            frappe.throw("Contractor Name is required")
