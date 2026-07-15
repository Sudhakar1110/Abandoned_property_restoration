import frappe
from frappe.model.document import Document


class RestorationProgress(Document):
    def validate(self):
        if not self.progress_id:
            frappe.throw("Progress ID is required")
        if not self.restoration_project:
            frappe.throw("Restoration Project is required")
    
    def on_submit(self):
        self.update_project_progress()
    
    def update_project_progress(self):
        if self.restoration_project:
            frappe.db.set_value(
                "Restoration Project",
                self.restoration_project,
                "progress_percentage",
                self.progress_percentage,
                update_modified=False
            )
