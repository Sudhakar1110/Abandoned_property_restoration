import frappe
from frappe.model.document import Document


class Client(Document):
    def validate(self):
        if not self.client_name:
            frappe.throw("Client Name is required")
        self.update_totals()
    
    def update_totals(self):
        reports = frappe.db.count("Client Property Report", {"client": self.name})
        self.total_reports = reports
        
        rewards = frappe.db.sql("""
            SELECT SUM(reward_amount) as total 
            FROM `tabReward Claim` 
            WHERE client = %s AND claim_status = 'Paid'
        """, self.name)
        self.total_rewards = rewards[0][0] if rewards and rewards[0][0] else 0
