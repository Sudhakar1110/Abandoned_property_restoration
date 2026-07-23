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
    """Ensure Module Def exists and reports are created after migration."""
    create_module_def()
    create_reports()
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
    """Create all 14 Query Reports programmatically."""
    reports = [
        {
            "name": "Abandoned Property Summary",
            "ref_doctype": "Abandoned Property",
            "query": "SELECT name, property_name, address, property_status, risk_level, property_type, owner_name FROM `tabAbandoned Property` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Citizen Reward Report",
            "ref_doctype": "Reward Claim",
            "query": "SELECT name, citizen, report_name, reward_type, reward_amount, claim_status FROM `tabReward Claim` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Digital Archive Report",
            "ref_doctype": "Digital Time Capsule",
            "query": "SELECT name, property, capsule_name, category, creation_date, status FROM `tabDigital Time Capsule` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "District Wise Restoration Report",
            "ref_doctype": "Abandoned Property",
            "query": "SELECT COALESCE(ap.district, 'Unknown') as district, COALESCE(ap.city, 'Unknown') as city, COUNT(*) as total_properties, SUM(CASE WHEN ap.property_status = 'Reported' THEN 1 ELSE 0 END) as reported, SUM(CASE WHEN ap.property_status = 'Under Inspection' THEN 1 ELSE 0 END) as under_inspection, SUM(CASE WHEN ap.property_status = 'In Restoration' THEN 1 ELSE 0 END) as in_restoration, SUM(CASE WHEN ap.property_status = 'Restored' THEN 1 ELSE 0 END) as restored FROM `tabAbandoned Property` ap WHERE ap.docstatus < 2 GROUP BY ap.district, ap.city ORDER BY total_properties DESC"
        },
        {
            "name": "Historical Records Report",
            "ref_doctype": "Historical Record",
            "query": "SELECT name, property, document_type, title, record_date, source_name FROM `tabHistorical Record` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Maintenance Report",
            "ref_doctype": "Maintenance Schedule",
            "query": "SELECT name, property, schedule_type, schedule_date, schedule_status, contractor, estimated_cost FROM `tabMaintenance Schedule` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Material Exchange Report",
            "ref_doctype": "Material Exchange",
            "query": "SELECT name, material_name, source_project, destination_project, quantity, exchange_date, exchange_status FROM `tabMaterial Exchange` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Material Salvage Report",
            "ref_doctype": "Material Salvage",
            "query": "SELECT name, property, material_name, material_category, quantity, condition, status FROM `tabMaterial Salvage` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Project Progress Report",
            "ref_doctype": "Restoration Progress",
            "query": "SELECT name, restoration_project, property, update_date, progress_percentage, work_completed, current_phase FROM `tabRestoration Progress` WHERE docstatus < 2 ORDER BY update_date DESC"
        },
        {
            "name": "Property Inspection Report",
            "ref_doctype": "Property Inspection",
            "query": "SELECT name, property, inspector, inspection_date, structure_condition, risk_level, inspection_status FROM `tabProperty Inspection` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Property Timeline Report",
            "ref_doctype": "Property Timeline",
            "query": "SELECT name, property, event_type, event_title, event_date, created_by FROM `tabProperty Timeline` WHERE docstatus < 2 ORDER BY event_date DESC"
        },
        {
            "name": "Restoration Cost Report",
            "ref_doctype": "Project Cost",
            "query": "SELECT name, restoration_project, cost_type, amount, expense_date, vendor, payment_status FROM `tabProject Cost` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Restoration Status Report",
            "ref_doctype": "Restoration Project",
            "query": "SELECT name, property, project_status, start_date, expected_end_date, progress_percentage, estimated_cost FROM `tabRestoration Project` WHERE docstatus < 2 ORDER BY modified DESC"
        },
        {
            "name": "Top Contributors Report",
            "ref_doctype": "Citizen",
            "query": "SELECT cpr.citizen, COUNT(*) as total_reports, SUM(CASE WHEN cpr.status = 'Verified' THEN 1 ELSE 0 END) as verified_reports, SUM(CASE WHEN cpr.status = 'Pending' THEN 1 ELSE 0 END) as pending_reports, SUM(CASE WHEN cpr.status = 'Rejected' THEN 1 ELSE 0 END) as rejected_reports, COALESCE(SUM(rc.reward_amount), 0) as total_rewards FROM `tabCitizen Property Report` cpr LEFT JOIN `tabReward Claim` rc ON rc.property_report = cpr.name AND rc.claim_status = 'Approved' WHERE cpr.docstatus < 2 GROUP BY cpr.citizen ORDER BY total_reports DESC"
        },
    ]
    
    for report_data in reports:
        try:
            if frappe.db.exists("Report", report_data["name"]):
                # Update existing report to Query Report type
                report = frappe.get_doc("Report", report_data["name"])
                if report.report_type != "Query Report":
                    report.report_type = "Query Report"
                    report.query = report_data["query"]
                    report.report_name = report_data["name"]
                    report.is_standard = "Yes"
                    report.save(ignore_permissions=True)
            else:
                # Create new report
                report = frappe.get_doc({
                    "doctype": "Report",
                    "name": report_data["name"],
                    "report_name": report_data["name"],
                    "module": "restoration",
                    "is_standard": "Yes",
                    "ref_doctype": report_data["ref_doctype"],
                    "report_type": "Query Report",
                    "query": report_data["query"],
                    "disabled": 0,
                })
                report.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Could not create/update report {report_data['name']}: {e}")

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
    for item in ["Citizen", "Contractor", "Engineer", "Inspector", "Government Department", "Location", "District", "City", "State", "Country", "Property Category", "Property Type", "Restoration Category", "Material Category", "Material Condition", "Reward Type", "Ownership Type", "Risk Level", "Restoration Status", "Project Priority"]:
        add_link(item, item, "DocType")
    
    # Transactions section
    add_card_break("Transactions")
    for item in ["Abandoned Property", "Citizen Property Report", "Property Inspection", "Inspection Report", "Restoration Project", "Project Assignment", "Restoration Progress", "Before After Visualization", "Material Salvage", "Material Exchange", "Material Sale", "Digital Time Capsule", "Historical Record", "Maintenance Schedule", "Maintenance Visit", "Property Ownership Record", "Property Timeline", "Property Images", "Property Documents", "Reward Claim", "Project Cost", "Expense Entry"]:
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
        roles = ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]
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
