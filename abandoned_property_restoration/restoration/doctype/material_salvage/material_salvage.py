import frappe
from frappe.model.document import Document


class MaterialSalvage(Document):
    def validate(self):
        self.validate_required_fields()
        self.update_restoration_project_count()
    
    def validate_required_fields(self):
        if not self.material_id:
            frappe.throw("Material ID is required")
        if not self.material_name:
            frappe.throw("Material Name is required")
        if not self.material_type:
            frappe.throw("Material Type is required")
        if self.quantity <= 0:
            frappe.throw("Quantity must be greater than 0")
    
    def update_restoration_project_count(self):
        if self.restoration_project:
            count = frappe.db.count("Material Salvage", {"restoration_project": self.restoration_project})
            frappe.db.set_value(
                "Restoration Project",
                self.restoration_project,
                "material_salvage_count",
                count,
                update_modified=False
            )
