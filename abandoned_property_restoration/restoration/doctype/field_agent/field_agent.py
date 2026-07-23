import frappe
from frappe.model.document import Document


class FieldAgent(Document):
    def validate(self):
        if not self.field_agent_name:
            frappe.throw("Field Agent Name is required")
