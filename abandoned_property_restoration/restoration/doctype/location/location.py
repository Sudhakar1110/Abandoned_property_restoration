import frappe
from frappe.model.document import Document


class Location(Document):
    def validate(self):
        if not self.location_name:
            frappe.throw("Location Name is required")
