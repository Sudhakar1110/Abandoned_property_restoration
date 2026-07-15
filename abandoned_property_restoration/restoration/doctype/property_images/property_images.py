import frappe
from frappe.model.document import Document


class PropertyImages(Document):
    def validate(self):
        if not self.image_id:
            frappe.throw("Image ID is required")
        if not self.property:
            frappe.throw("Property is required")
