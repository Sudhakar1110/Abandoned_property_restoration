import frappe
from frappe.model.document import Document


class MaintenanceSchedule(Document):
    def validate(self):
        if not self.schedule_id:
            frappe.throw("Schedule ID is required")
        if not self.property:
            frappe.throw("Property is required")
