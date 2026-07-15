import frappe
from frappe.model.document import Document


class InspectionReport(Document):
    def validate(self):
        if not self.report_id:
            frappe.throw("Report ID is required")
        if not self.property:
            frappe.throw("Property is required")
