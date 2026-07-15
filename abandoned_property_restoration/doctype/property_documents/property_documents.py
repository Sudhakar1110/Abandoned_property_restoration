import frappe
from frappe.model.document import Document


class PropertyDocuments(Document):
    def validate(self):
        if not self.document_id:
            frappe.throw("Document ID is required")
        if not self.property:
            frappe.throw("Property is required")
