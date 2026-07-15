import frappe
from frappe.model.document import Document


class OwnershipType(Document):
    def validate(self):
        if not self.ownership_type_name:
            frappe.throw("Ownership Type Name is required")
