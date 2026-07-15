import frappe
from frappe.model.document import Document


class MaterialExchange(Document):
    def validate(self):
        self.validate_required_fields()
    
    def validate_required_fields(self):
        if not self.exchange_id:
            frappe.throw("Exchange ID is required")
        if not self.material:
            frappe.throw("Material is required")
        if not self.destination_project:
            frappe.throw("Destination Project is required")
        if self.quantity <= 0:
            frappe.throw("Quantity must be greater than 0")
    
    def on_submit(self):
        self.update_material_status()
        self.update_project_counts()
    
    def update_material_status(self):
        if self.exchange_status == "Completed":
            frappe.db.set_value(
                "Material Salvage",
                self.material,
                "status",
                "Exchanged",
                update_modified=False
            )
    
    def update_project_counts(self):
        if self.destination_project:
            count = frappe.db.count("Material Exchange", {"destination_project": self.destination_project})
            frappe.db.set_value(
                "Restoration Project",
                self.destination_project,
                "material_exchange_count",
                count,
                update_modified=False
            )
