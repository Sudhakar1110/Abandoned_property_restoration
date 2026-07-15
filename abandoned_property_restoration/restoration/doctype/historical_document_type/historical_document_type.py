import frappe
from frappe.model.document import Document


class HistoricalDocumentType(Document):
    def validate(self):
        if not self.document_type_name:
            frappe.throw("Document Type Name is required")
