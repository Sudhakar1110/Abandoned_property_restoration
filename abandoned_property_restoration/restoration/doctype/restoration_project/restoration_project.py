import frappe
from frappe.model.document import Document


class RestorationProject(Document):
    def validate(self):
        self.validate_required_fields()
        self.calculate_total_cost()
    
    def validate_required_fields(self):
        if not self.project_name:
            frappe.throw("Project Name is required")
        if not self.property:
            frappe.throw("Property is required")
        if not self.project_status:
            frappe.throw("Project Status is required")
    
    def calculate_total_cost(self):
        if self.name:
            try:
                total = frappe.db.sql("""
                    SELECT SUM(total_amount) as total
                    FROM `tabExpense Entry`
                    WHERE parent_project = %s
                """, self.name)
                if total and total[0][0]:
                    self.total_cost = total[0][0]
            except Exception:
                # Column may not exist yet during fresh install
                pass
    
    def on_submit(self):
        self.update_property_status()
        self.update_client_report()
    
    def update_property_status(self):
        if self.project_status == "Completed":
            frappe.db.set_value(
                "Abandoned Property",
                self.property,
                "restoration_status",
                "Completed",
                update_modified=False
            )
            frappe.db.set_value(
                "Abandoned Property",
                self.property,
                "property_status",
                "Restored",
                update_modified=False
            )
            frappe.db.set_value(
                "Abandoned Property",
                self.property,
                "actual_restoration_cost",
                self.total_cost,
                update_modified=False
            )
    
    def update_client_report(self):
        if self.client_report:
            frappe.db.set_value(
                "Client Property Report",
                self.citizen_report,
                "assigned_project",
                self.name,
                update_modified=False
            )
            frappe.db.set_value(
                "Client Property Report",
                self.citizen_report,
                "status",
                "Restoration Assigned",
                update_modified=False
            )
