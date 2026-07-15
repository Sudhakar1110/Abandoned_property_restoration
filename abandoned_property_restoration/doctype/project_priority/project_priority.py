import frappe
from frappe.model.document import Document


class ProjectPriority(Document):
    def validate(self):
        if not self.priority_name:
            frappe.throw("Priority Name is required")
