import frappe
from frappe.model.document import Document


class PropertyCategory(Document):
    def validate(self):
        self.validate_name()
    
    def validate_name(self):
        if not self.property_category_name:
            frappe.throw("Property Category Name is required")
