import frappe
from frappe.model.document import Document


class District(Document):
    def validate(self):
        if not self.district_name:
            frappe.throw("District Name is required")
