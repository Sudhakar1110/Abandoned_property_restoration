import frappe
from frappe.model.document import Document


class DigitalTimeCapsule(Document):
    def validate(self):
        if not self.capsule_id:
            frappe.throw("Capsule ID is required")
        if not self.capsule_name:
            frappe.throw("Capsule Name is required")
