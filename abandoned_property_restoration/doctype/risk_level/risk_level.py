import frappe
from frappe.model.document import Document


class RiskLevel(Document):
    def validate(self):
        if not self.risk_level_name:
            frappe.throw("Risk Level Name is required")
