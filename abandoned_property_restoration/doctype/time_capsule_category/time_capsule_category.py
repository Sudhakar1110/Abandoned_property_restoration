import frappe
from frappe.model.document import Document


class TimeCapsuleCategory(Document):
    def validate(self):
        if not self.category_name:
            frappe.throw("Category Name is required")
