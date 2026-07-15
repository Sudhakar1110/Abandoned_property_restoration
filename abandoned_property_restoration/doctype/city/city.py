import frappe
from frappe.model.document import Document


class City(Document):
    def validate(self):
        if not self.city_name:
            frappe.throw("City Name is required")
