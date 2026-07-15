import frappe
from frappe.model.document import Document


class ProjectAssignment(Document):
    def validate(self):
        if not self.assignment_id:
            frappe.throw("Assignment ID is required")
        if not self.property:
            frappe.throw("Property is required")
