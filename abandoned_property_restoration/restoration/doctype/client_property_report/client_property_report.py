import frappe
from frappe.model.document import Document


class ClientPropertyReport(Document):
    def validate(self):
        self.validate_required_fields()
        self.set_report_id()
    
    def validate_required_fields(self):
        if not self.property_name:
            frappe.throw("Property Name is required")
        if not self.client_name:
            frappe.throw("Client Name is required")
    
    def set_report_id(self):
        if not self.report_id:
            self.report_id = frappe.generate_hash(length=10)
    
    def on_submit(self):
        self.create_reward_claim_if_eligible()
    
    def create_reward_claim_if_eligible(self):
        if self.reward_eligible and not self.reward_claimed:
            reward_claim = frappe.new_doc("Reward Claim")
            reward_claim.report_name = self.name
            reward_claim.client = self.client
            reward_claim.client_name = self.client_name
            reward_claim.property_name = self.property_name
            reward_claim.reward_type = self.reward_type
            reward_claim.reward_amount = self.reward_amount
            reward_claim.claim_status = "Pending"
            reward_claim.insert(ignore_permissions=True)
            frappe.db.set_value("Client Property Report", self.name, "reward_claimed", 1)
