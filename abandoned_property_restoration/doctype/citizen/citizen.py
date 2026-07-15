import frappe
from frappe.model.document import Document


class Citizen(Document):
    def validate(self):
        if not self.citizen_name:
            frappe.throw("Citizen Name is required")
        self.update_totals()
    
    def update_totals(self):
        reports = frappe.db.count("Citizen Property Report", {"citizen": self.name})
        self.total_reports = reports
        
        rewards = frappe.db.sql("""
            SELECT SUM(reward_amount) as total 
            FROM `tabReward Claim` 
            WHERE citizen = %s AND claim_status = 'Paid'
        """, self.name)
        self.total_rewards = rewards[0][0] if rewards and rewards[0][0] else 0
