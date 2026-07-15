import frappe
from frappe.model.document import Document


class HistoricalRecord(Document):
    def validate(self):
        if not self.record_id:
            frappe.throw("Record ID is required")
        if not self.title:
            frappe.throw("Title is required")
