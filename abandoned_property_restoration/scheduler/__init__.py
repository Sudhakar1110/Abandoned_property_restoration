import frappe


def all():
    pass


def daily():
    maintenance_due_check()
    project_delayed_check()


def hourly():
    status_check()


def weekly():
    pass


def monthly():
    pass


def yearly():
    pass


def maintenance_due_check():
    today = frappe.utils.today()
    
    due_maintenance = frappe.get_all(
        "Maintenance Schedule",
        filters={
            "maintenance_date": today,
            "maintenance_status": "Scheduled"
        },
        fields=["name", "property", "maintenance_type"]
    )
    
    for maintenance in due_maintenance:
        try:
            users = frappe.get_all(
                "Has Role",
                filters={"role": "Contractor"},
                pluck="parent"
            )
            
            for user in users:
                notification = frappe.new_doc("Notification Log")
                notification.update({
                    "type": "Alert",
                    "document_type": "Maintenance Schedule",
                    "document_name": maintenance.name,
                    "subject": "Maintenance Due Today",
                    "message": f"Maintenance scheduled for property {maintenance.property}",
                    "for_user": user
                })
                notification.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Error in maintenance_due_check: {str(e)}", "Scheduler Error")


def project_delayed_check():
    delayed_projects = frappe.get_all(
        "Restoration Project",
        filters={
            "project_status": "In Progress",
            "expected_end_date": ["<", frappe.utils.today()]
        },
        fields=["name", "property", "expected_end_date"]
    )
    
    for project in delayed_projects:
        try:
            users = frappe.get_all(
                "Has Role",
                filters={"role": ["in", ["Property Administrator", "Restoration Manager"]]},
                pluck="parent"
            )
            
            for user in users:
                notification = frappe.new_doc("Notification Log")
                notification.update({
                    "type": "Alert",
                    "document_type": "Restoration Project",
                    "document_name": project.name,
                    "subject": "Project Delayed",
                    "message": f"Restoration project {project.name} for property {project.property} is overdue",
                    "for_user": user
                })
                notification.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Error in project_delayed_check: {str(e)}", "Scheduler Error")


def status_check():
    pass
