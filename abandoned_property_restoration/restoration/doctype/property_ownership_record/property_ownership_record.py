import frappe
from frappe.model.document import Document


class PropertyOwnershipRecord(Document):
    def validate(self):
        if not self.record_id:
            frappe.throw("Record ID is required")
        if not self.property:
            frappe.throw("Property is required")
