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
    """Ensure Module Def exists and reports & workspace are updated after migration."""
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
    # Content JSON defines the workspace layout structure (headers + empty cards)
    # Individual links are managed via the links child table below
    workspace_content = [
        {"id": "hdr_masters", "type": "header", "data": {"text": "Masters", "col": 12}},
        {"id": "card_masters", "type": "card", "data": {"card_name": "Masters"}},
        {"id": "hdr_transactions", "type": "header", "data": {"text": "Transactions", "col": 12}},
        {"id": "card_transactions", "type": "card", "data": {"card_name": "Transactions"}},
        {"id": "hdr_reports", "type": "header", "data": {"text": "Reports", "col": 12}},
        {"id": "card_reports", "type": "card", "data": {"card_name": "Reports"}}
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


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
