import frappe
from frappe.model.document import Document


class PropertyInspection(Document):
    def validate(self):
        self.validate_required_fields()
    
    def validate_required_fields(self):
        if not self.inspection_id:
            frappe.throw("Inspection ID is required")
        if not self.property:
            frappe.throw("Property is required")
        if not self.inspector:
            frappe.throw("Inspector is required")
    
    def on_submit(self):
        self.update_property_risk_level()
    
    def update_property_risk_level(self):
        if self.property and self.risk_level:
            frappe.db.set_value(
                "Abandoned Property",
                self.property,
                "risk_level",
                self.risk_level,
                update_modified=False
            )
