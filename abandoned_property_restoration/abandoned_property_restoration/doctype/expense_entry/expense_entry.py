import frappe
from frappe.model.document import Document


class ExpenseEntry(Document):
    def validate(self):
        if not self.expense_id:
            frappe.throw("Expense ID is required")
        if self.amount <= 0:
            frappe.throw("Amount must be greater than 0")
