import frappe
from frappe.model.document import Document


class ProjectCost(Document):
    def validate(self):
        if not self.cost_id:
            frappe.throw("Cost ID is required")
        if self.amount <= 0:
            frappe.throw("Amount must be greater than 0")
