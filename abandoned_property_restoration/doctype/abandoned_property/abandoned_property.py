import frappe
from frappe.model.document import Document


class AbandonedProperty(Document):
    def validate(self):
        self.validate_required_fields()
        self.set_title()
    
    def validate_required_fields(self):
        if not self.property_name:
            frappe.throw("Property Name is required")
        if not self.property_status:
            frappe.throw("Property Status is required")
    
    def set_title(self):
        self.title = f"{self.property_name}"
    
    def on_submit(self):
        self.update_property_status()
    
    def update_property_status(self):
        if self.restoration_status:
            frappe.db.set_value(
                "Abandoned Property",
                self.name,
                "property_status",
                "Under Restoration" if self.restoration_status == "In Progress" else self.property_status,
                update_modified=False
            )
