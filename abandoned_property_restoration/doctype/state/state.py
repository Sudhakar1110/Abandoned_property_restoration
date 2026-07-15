import frappe
from frappe.model.document import Document


class State(Document):
    def validate(self):
        if not self.state_name:
            frappe.throw("State Name is required")
