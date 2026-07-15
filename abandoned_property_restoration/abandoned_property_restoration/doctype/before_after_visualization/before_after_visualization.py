import frappe
from frappe.model.document import Document


class BeforeAfterVisualization(Document):
    def validate(self):
        self.validate_required_fields()
    
    def validate_required_fields(self):
        if not self.visualization_id:
            frappe.throw("Visualization ID is required")
        if not self.property:
            frappe.throw("Property is required")
