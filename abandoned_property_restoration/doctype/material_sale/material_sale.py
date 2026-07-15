import frappe
from frappe.model.document import Document


class MaterialSale(Document):
    def validate(self):
        self.validate_required_fields()
        self.calculate_total()
    
    def validate_required_fields(self):
        if not self.sale_id:
            frappe.throw("Sale ID is required")
        if not self.material:
            frappe.throw("Material is required")
        if not self.buyer_name:
            frappe.throw("Buyer Name is required")
        if self.quantity <= 0:
            frappe.throw("Quantity must be greater than 0")
        if self.unit_price <= 0:
            frappe.throw("Unit Price must be greater than 0")
    
    def calculate_total(self):
        self.total_amount = self.quantity * self.unit_price
    
    def on_submit(self):
        self.update_material_status()
    
    def update_material_status(self):
        if self.sale_status == "Completed":
            frappe.db.set_value(
                "Material Salvage",
                self.material,
                "status",
                "Sold",
                update_modified=False
            )
