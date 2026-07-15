import frappe
from frappe.model.document import Document


class MaterialCondition(Document):
    def validate(self):
        if not self.condition_name:
            frappe.throw("Condition Name is required")
