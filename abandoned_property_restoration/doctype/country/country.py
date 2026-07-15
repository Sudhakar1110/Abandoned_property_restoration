import frappe
from frappe.model.document import Document


class Country(Document):
    def validate(self):
        if not self.country_name:
            frappe.throw("Country Name is required")
