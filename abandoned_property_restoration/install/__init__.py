import frappe


def after_install():
    create_roles()
    create_workspace()
    create_custom_fields()
    create_property_doctypes()
    frappe.db.commit()
    frappe.publish_realtime("bench_event", {"message": "Abandoned Property Restoration installed successfully"})


def after_uninstall():
    pass


def create_roles():
    """Create custom roles required by the app before workspace creation."""
    roles = [
        {"role_name": "Property Administrator", "desk_access": 1},
        {"role_name": "Restoration Manager", "desk_access": 1},
        {"role_name": "Government Officer", "desk_access": 1},
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
                    {"type": "link", "label": "Citizen", "link_to": "Citizen", "link_type": "DocType"},
                    {"type": "link", "label": "Contractor", "link_to": "Contractor", "link_type": "DocType"},
                    {"type": "link", "label": "Engineer", "link_to": "Engineer", "link_type": "DocType"},
                    {"type": "link", "label": "Inspector", "link_to": "Inspector", "link_type": "DocType"},
                    {"type": "link", "label": "Government Department", "link_to": "Government Department", "link_type": "DocType"},
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
                    {"type": "link", "label": "Citizen Property Report", "link_to": "Citizen Property Report", "link_type": "DocType"},
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
    
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        # Update existing workspace
        workspace = frappe.get_doc("Workspace", "Abandoned Property Restoration")
        workspace.content = frappe.json.dumps(workspace_content)
        workspace.icon = "fa fa-home"
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
        roles = ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]
        for role in roles:
            workspace.append("roles", {"role": role})
        
        workspace.insert(ignore_permissions=True)
    
    frappe.db.commit()


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
