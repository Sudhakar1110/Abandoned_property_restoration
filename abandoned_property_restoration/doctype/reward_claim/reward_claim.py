import frappe
from frappe.model.document import Document


class RewardClaim(Document):
    def validate(self):
        self.validate_required_fields()
    
    def validate_required_fields(self):
        if not self.claim_id:
            frappe.throw("Claim ID is required")
        if not self.citizen:
            frappe.throw("Citizen is required")
        if self.reward_amount <= 0:
            frappe.throw("Reward Amount must be greater than 0")
    
    def on_submit(self):
        if self.claim_status == "Paid":
            self.update_citizen_totals()
    
    def update_citizen_totals(self):
        if self.citizen:
            citizen = frappe.get_doc("Citizen", self.citizen)
            citizen.update_totals()
            citizen.save(ignore_permissions=True)
