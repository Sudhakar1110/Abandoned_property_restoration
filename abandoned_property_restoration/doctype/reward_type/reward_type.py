import frappe
from frappe.model.document import Document


class RewardType(Document):
    def validate(self):
        if not self.reward_type_name:
            frappe.throw("Reward Type Name is required")
