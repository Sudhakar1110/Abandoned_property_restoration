import frappe
from frappe.model.document import Document


class PropertyType(Document):
    def validate(self):
        self.validate_name()
    
    def validate_name(self):
        if not self.property_type_name:
            frappe.throw("Property Type Name is required")
