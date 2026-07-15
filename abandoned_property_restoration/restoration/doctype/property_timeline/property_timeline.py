import frappe
from frappe.model.document import Document


class PropertyTimeline(Document):
    def validate(self):
        if not self.timeline_id:
            frappe.throw("Timeline ID is required")
        if not self.property:
            frappe.throw("Property is required")
