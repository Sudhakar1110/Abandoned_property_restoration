import frappe


def after_install():
    create_module_def()
    create_roles()
    create_reports()
    create_workspace()
    create_custom_fields()
    create_property_doctypes()
    frappe.db.commit()
    frappe.publish_realtime("bench_event", {"message": "Abandoned Property Restoration installed successfully"})


def after_migrate():
    """Ensure Module Def exists and reports, charts & workspace are updated after migration."""
    create_module_def()
    create_reports()
    create_workspace()
    frappe.db.commit()


def after_uninstall():
    pass


def create_module_def():
    """Ensure the Module Def for restoration exists so Frappe can find report modules."""
    if not frappe.db.exists("Module Def", "restoration"):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "restoration",
            "app_name": "abandoned_property_restoration",
        }).insert(ignore_permissions=True)


def create_reports():
    """Create all 14 reports as Report Builder reports programmatically."""
    reports = [
        {"name": "Abandoned Property Summary", "ref_doctype": "Abandoned Property"},
        {"name": "Citizen Reward Report", "ref_doctype": "Reward Claim"},
        {"name": "Digital Archive Report", "ref_doctype": "Digital Time Capsule"},
        {"name": "District Wise Restoration Report", "ref_doctype": "Abandoned Property"},
        {"name": "Historical Records Report", "ref_doctype": "Historical Record"},
        {"name": "Maintenance Report", "ref_doctype": "Maintenance Schedule"},
        {"name": "Material Exchange Report", "ref_doctype": "Material Exchange"},
        {"name": "Material Salvage Report", "ref_doctype": "Material Salvage"},
        {"name": "Project Progress Report", "ref_doctype": "Restoration Progress"},
        {"name": "Property Inspection Report", "ref_doctype": "Property Inspection"},
        {"name": "Property Timeline Report", "ref_doctype": "Property Timeline"},
        {"name": "Restoration Cost Report", "ref_doctype": "Project Cost"},
        {"name": "Restoration Status Report", "ref_doctype": "Restoration Project"},
        {"name": "Top Contributors Report", "ref_doctype": "Client Property Report"},
    ]
    
    for report_data in reports:
        try:
            if frappe.db.exists("Report", report_data["name"]):
                report = frappe.get_doc("Report", report_data["name"])
                if report.report_type != "Report Builder":
                    report.report_type = "Report Builder"
                    report.is_standard = "Yes"
                    report.save(ignore_permissions=True)
            else:
                report = frappe.get_doc({
                    "doctype": "Report",
                    "name": report_data["name"],
                    "report_name": report_data["name"],
                    "module": "restoration",
                    "is_standard": "Yes",
                    "ref_doctype": report_data["ref_doctype"],
                    "report_type": "Report Builder",
                    "disabled": 0,
                })
                report.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Could not create/update report {report_data['name']}: {e}")

def create_roles():
    """Create custom roles required by the app before workspace creation."""
    roles = [
        {"role_name": "Property Manager", "desk_access": 1},
        {"role_name": "Restoration Manager", "desk_access": 1},
        {"role_name": "Approver", "desk_access": 1},
        {"role_name": "View Only User", "desk_access": 0},
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role_data["role_name"],
                "desk_access": role_data["desk_access"],
            }).insert(ignore_permissions=True)


def create_workspace():
    """Create or update the Abandoned Property Restoration workspace."""
    workspace_content = [
        {"id": "hdr_masters", "type": "header", "data": {"text": "Masters", "col": 12}},
        {
            "id": "card_masters",
            "type": "card",
            "data": {
                "card_name": "Masters",
                "links": [
                    {"type": "link", "label": "Client", "link_to": "Client", "link_type": "DocType"},
                    {"type": "link", "label": "Contractor", "link_to": "Contractor", "link_type": "DocType"},
                    {"type": "link", "label": "Engineer", "link_to": "Engineer", "link_type": "DocType"},
                    {"type": "link", "label": "Field Agent", "link_to": "Field Agent", "link_type": "DocType"},
                    {"type": "link", "label": "Department", "link_to": "Department", "link_type": "DocType"},
                    {"type": "link", "label": "Location", "link_to": "Location", "link_type": "DocType"},
                    {"type": "link", "label": "District", "link_to": "District", "link_type": "DocType"},
                    {"type": "link", "label": "City", "link_to": "City", "link_type": "DocType"},
                    {"type": "link", "label": "State", "link_to": "State", "link_type": "DocType"},
                    {"type": "link", "label": "Country", "link_to": "Country", "link_type": "DocType"},
                    {"type": "link", "label": "Property Category", "link_to": "Property Category", "link_type": "DocType"},
                    {"type": "link", "label": "Property Type", "link_to": "Property Type", "link_type": "DocType"},
                    {"type": "link", "label": "Restoration Category", "link_to": "Restoration Category", "link_type": "DocType"},
                    {"type": "link", "label": "Material Category", "link_to": "Material Category", "link_type": "DocType"},
                    {"type": "link", "label": "Material Condition", "link_to": "Material Condition", "link_type": "DocType"},
                    {"type": "link", "label": "Reward Type", "link_to": "Reward Type", "link_type": "DocType"},
                    {"type": "link", "label": "Ownership Type", "link_to": "Ownership Type", "link_type": "DocType"},
                    {"type": "link", "label": "Risk Level", "link_to": "Risk Level", "link_type": "DocType"},
                    {"type": "link", "label": "Restoration Status", "link_to": "Restoration Status", "link_type": "DocType"},
                    {"type": "link", "label": "Project Priority", "link_to": "Project Priority", "link_type": "DocType"}
                ]
            }
        },
        {"id": "hdr_transactions", "type": "header", "data": {"text": "Transactions", "col": 12}},
        {
            "id": "card_transactions",
            "type": "card",
            "data": {
                "card_name": "Transactions",
                "links": [
                    {"type": "link", "label": "Abandoned Property", "link_to": "Abandoned Property", "link_type": "DocType"},
                    {"type": "link", "label": "Client Property Report", "link_to": "Client Property Report", "link_type": "DocType"},
                    {"type": "link", "label": "Property Inspection", "link_to": "Property Inspection", "link_type": "DocType"},
                    {"type": "link", "label": "Inspection Report", "link_to": "Inspection Report", "link_type": "DocType"},
                    {"type": "link", "label": "Restoration Project", "link_to": "Restoration Project", "link_type": "DocType"},
                    {"type": "link", "label": "Project Assignment", "link_to": "Project Assignment", "link_type": "DocType"},
                    {"type": "link", "label": "Restoration Progress", "link_to": "Restoration Progress", "link_type": "DocType"},
                    {"type": "link", "label": "Before After Visualization", "link_to": "Before After Visualization", "link_type": "DocType"},
                    {"type": "link", "label": "Material Salvage", "link_to": "Material Salvage", "link_type": "DocType"},
                    {"type": "link", "label": "Material Exchange", "link_to": "Material Exchange", "link_type": "DocType"},
                    {"type": "link", "label": "Material Sale", "link_to": "Material Sale", "link_type": "DocType"},
                    {"type": "link", "label": "Digital Time Capsule", "link_to": "Digital Time Capsule", "link_type": "DocType"},
                    {"type": "link", "label": "Historical Record", "link_to": "Historical Record", "link_type": "DocType"},
                    {"type": "link", "label": "Maintenance Schedule", "link_to": "Maintenance Schedule", "link_type": "DocType"},
                    {"type": "link", "label": "Maintenance Visit", "link_to": "Maintenance Visit", "link_type": "DocType"},
                    {"type": "link", "label": "Property Ownership Record", "link_to": "Property Ownership Record", "link_type": "DocType"},
                    {"type": "link", "label": "Property Timeline", "link_to": "Property Timeline", "link_type": "DocType"},
                    {"type": "link", "label": "Property Images", "link_to": "Property Images", "link_type": "DocType"},
                    {"type": "link", "label": "Property Documents", "link_to": "Property Documents", "link_type": "DocType"},
                    {"type": "link", "label": "Reward Claim", "link_to": "Reward Claim", "link_type": "DocType"},
                    {"type": "link", "label": "Project Cost", "link_to": "Project Cost", "link_type": "DocType"},
                    {"type": "link", "label": "Expense Entry", "link_to": "Expense Entry", "link_type": "DocType"}
                ]
            }
        },
        {"id": "hdr_reports", "type": "header", "data": {"text": "Reports", "col": 12}},
        {
            "id": "card_reports",
            "type": "card",
            "data": {
                "card_name": "Reports",
                "links": [
                    {"type": "link", "label": "Abandoned Property Summary", "link_to": "Abandoned Property Summary", "link_type": "Report"},
                    {"type": "link", "label": "Citizen Reward Report", "link_to": "Citizen Reward Report", "link_type": "Report"},
                    {"type": "link", "label": "Digital Archive Report", "link_to": "Digital Archive Report", "link_type": "Report"},
                    {"type": "link", "label": "District Wise Restoration Report", "link_to": "District Wise Restoration Report", "link_type": "Report"},
                    {"type": "link", "label": "Historical Records Report", "link_to": "Historical Records Report", "link_type": "Report"},
                    {"type": "link", "label": "Maintenance Report", "link_to": "Maintenance Report", "link_type": "Report"},
                    {"type": "link", "label": "Material Exchange Report", "link_to": "Material Exchange Report", "link_type": "Report"},
                    {"type": "link", "label": "Material Salvage Report", "link_to": "Material Salvage Report", "link_type": "Report"},
                    {"type": "link", "label": "Project Progress Report", "link_to": "Project Progress Report", "link_type": "Report"},
                    {"type": "link", "label": "Property Inspection Report", "link_to": "Property Inspection Report", "link_type": "Report"},
                    {"type": "link", "label": "Property Timeline Report", "link_to": "Property Timeline Report", "link_type": "Report"},
                    {"type": "link", "label": "Restoration Cost Report", "link_to": "Restoration Cost Report", "link_type": "Report"},
                    {"type": "link", "label": "Restoration Status Report", "link_to": "Restoration Status Report", "link_type": "Report"},
                    {"type": "link", "label": "Top Contributors Report", "link_to": "Top Contributors Report", "link_type": "Report"}
                ]
            }
        }
    ]
    
    # Build the links child table for proper URL resolution
    workspace_links = []
    
    def add_card_break(label):
        workspace_links.append({
            "type": "Card Break",
            "label": label,
            "link_to": "",
            "link_type": "",
            "onboard": 0,
            "hidden": 0,
            "is_query_report": 0,
            "dependencies": "",
            "link_count": 0
        })
    
    def add_link(label, link_to, link_type):
        workspace_links.append({
            "type": "Link",
            "label": label,
            "link_to": link_to,
            "link_type": link_type,
            "onboard": 0,
            "hidden": 0,
            "is_query_report": 0,
            "dependencies": "",
            "link_count": 0
        })
    
    # Masters section
    add_card_break("Masters")
    for item in ["Client", "Contractor", "Engineer", "Field Agent", "Department", "Location", "District", "City", "State", "Country", "Property Category", "Property Type", "Restoration Category", "Material Category", "Material Condition", "Reward Type", "Ownership Type", "Risk Level", "Restoration Status", "Project Priority"]:
        add_link(item, item, "DocType")
    
    # Transactions section
    add_card_break("Transactions")
    for item in ["Abandoned Property", "Client Property Report", "Property Inspection", "Inspection Report", "Restoration Project", "Project Assignment", "Restoration Progress", "Before After Visualization", "Material Salvage", "Material Exchange", "Material Sale", "Digital Time Capsule", "Historical Record", "Maintenance Schedule", "Maintenance Visit", "Property Ownership Record", "Property Timeline", "Property Images", "Property Documents", "Reward Claim", "Project Cost", "Expense Entry"]:
        add_link(item, item, "DocType")
    
    # Reports section
    add_card_break("Reports")
    for item in ["Abandoned Property Summary", "Citizen Reward Report", "Digital Archive Report", "District Wise Restoration Report", "Historical Records Report", "Maintenance Report", "Material Exchange Report", "Material Salvage Report", "Project Progress Report", "Property Inspection Report", "Property Timeline Report", "Restoration Cost Report", "Restoration Status Report", "Top Contributors Report"]:
        add_link(item, item, "Report")
    
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        # Update existing workspace
        workspace = frappe.get_doc("Workspace", "Abandoned Property Restoration")
        workspace.content = frappe.json.dumps(workspace_content)
        workspace.icon = "fa fa-home"
        # Clear and repopulate links child table
        workspace.set("links", [])
        for link_data in workspace_links:
            workspace.append("links", link_data)
        workspace.save(ignore_permissions=True)
    else:
        # Create new workspace
        workspace = frappe.new_doc("Workspace")
        workspace.name = "Abandoned Property Restoration"
        workspace.title = "Abandoned Property Restoration"
        workspace.label = "Abandoned Property Restoration"
        workspace.icon = "fa fa-home"
        workspace.module = "restoration"
        workspace.public = 1
        workspace.sequence_id = 1
        workspace.is_standard = 1
        workspace.content = frappe.json.dumps(workspace_content)
        
        # Add roles
        roles = ["System Manager", "Property Manager", "Restoration Manager", "Approver", "View Only User"]
        for role in roles:
            workspace.append("roles", {"role": role})
        
        # Add links child table for proper URL resolution
        for link_data in workspace_links:
            workspace.append("links", link_data)
        
        workspace.insert(ignore_permissions=True)
    
    frappe.db.commit()


def create_dashboard_charts():
    """Create or update dashboard charts for the workspace."""
    charts = [
        {
            "chart_name": "Property Status Distribution",
            "chart_type": "Count",
            "document_type": "Abandoned Property",
            "group_by_based_on": "property_status",
            "type": "Donut",
            "timeseries": 0,
            "is_public": 1,
        },
        {
            "chart_name": "Restoration Project Status",
            "chart_type": "Count",
            "document_type": "Restoration Project",
            "group_by_based_on": "project_status",
            "type": "Bar",
            "timeseries": 0,
            "is_public": 1,
        },
        {
            "chart_name": "Monthly Client Reports",
            "chart_type": "Count",
            "document_type": "Client Property Report",
            "group_by_based_on": "creation",
            "type": "Line",
            "timeseries": 1,
            "timespan": "Monthly",
            "time_interval": "Monthly",
            "is_public": 1,
        },
    ]

    for chart_data in charts:
        try:
            if frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
                # Delete old broken chart (might have wrong type) and recreate
                frappe.delete_doc("Dashboard Chart", chart_data["chart_name"], force=True)
            
            chart_doc = frappe.get_doc({
                "doctype": "Dashboard Chart",
                "chart_name": chart_data["chart_name"],
                "chart_type": chart_data["chart_type"],
                "document_type": chart_data["document_type"],
                "group_by_based_on": chart_data["group_by_based_on"],
                "type": chart_data["type"],
                "timeseries": chart_data["timeseries"],
                "is_public": chart_data["is_public"],
            })
            if "timespan" in chart_data:
                chart_doc.timespan = chart_data["timespan"]
            if "time_interval" in chart_data:
                chart_doc.time_interval = chart_data["time_interval"]
            chart_doc.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Could not create/update dashboard chart {chart_data['chart_name']}: {e}")


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
