import frappe
from frappe.model.document import Document


class MaintenanceVisit(Document):
    def validate(self):
        if not self.visit_id:
            frappe.throw("Visit ID is required")
        if not self.property:
            frappe.throw("Property is required")
    
    def on_submit(self):
        self.update_schedule_status()
    
    def update_schedule_status(self):
        if self.maintenance_schedule and self.visit_status == "Completed":
            frappe.db.set_value(
                "Maintenance Schedule",
                self.maintenance_schedule,
                "schedule_status",
                "Completed",
                update_modified=False
            )
            frappe.db.set_value(
                "Maintenance Schedule",
                self.maintenance_schedule,
                "completed_date",
                self.visit_date,
                update_modified=False
            )
