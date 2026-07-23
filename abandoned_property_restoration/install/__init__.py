import frappe


def after_install():
    create_module_def()
    create_roles()
    create_reports()
    create_dashboard_charts()
    create_workspace()
    create_demo_data()
    create_custom_fields()
    create_property_doctypes()
    frappe.db.commit()
    frappe.publish_realtime("bench_event", {"message": "Abandoned Property Restoration installed successfully"})


def after_migrate():
    """Ensure Module Def exists and reports, workspace & demo data are updated after migration."""
    create_module_def()
    create_reports()
    create_dashboard_charts()
    create_workspace()
    create_demo_data()
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

def create_dashboard_charts():
    """Create interactive dashboard charts for the workspace."""
    charts = [
        {
            "chart_name": "Property Status Distribution",
            "chart_type": "Group By",
            "document_type": "Abandoned Property",
            "group_by_based_on": "property_status",
            "group_by_type": "Count",
            "type": "Donut",
            "is_public": 1,
            "filters_json": "[]",
        },
        {
            "chart_name": "Restoration Project Status",
            "chart_type": "Group By",
            "document_type": "Restoration Project",
            "group_by_based_on": "project_status",
            "group_by_type": "Count",
            "type": "Bar",
            "is_public": 1,
            "filters_json": "[]",
        },
        {
            "chart_name": "Risk Level Distribution",
            "chart_type": "Group By",
            "document_type": "Abandoned Property",
            "group_by_based_on": "risk_level",
            "group_by_type": "Count",
            "type": "Pie",
            "is_public": 1,
            "filters_json": "[]",
        },
        {
            "chart_name": "Inspection Status Overview",
            "chart_type": "Group By",
            "document_type": "Property Inspection",
            "group_by_based_on": "inspection_status",
            "group_by_type": "Count",
            "type": "Bar",
            "is_public": 1,
            "filters_json": "[]",
        },
    ]
    for chart_data in charts:
        if not frappe.db.exists("Dashboard Chart", chart_data["chart_name"]):
            try:
                doc = frappe.get_doc({
                    "doctype": "Dashboard Chart",
                    **chart_data,
                })
                doc.insert(ignore_permissions=True)
            except Exception as e:
                _safe_log_error("Dashboard Charts", f"Failed to create chart '{chart_data['chart_name']}': {str(e)[:80]}")


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
    # Content JSON defines the workspace layout structure (headers, charts, cards)
    # Individual links are managed via the links child table below
    workspace_content = [
        {"id": "hdr_dashboard", "type": "header", "data": {"text": "Dashboard", "col": 12}},
        {"id": "hdr_masters", "type": "header", "data": {"text": "Masters", "col": 12}},
        {"id": "card_masters", "type": "card", "data": {"card_name": "Masters"}},
        {"id": "hdr_transactions", "type": "header", "data": {"text": "Transactions", "col": 12}},
        {"id": "card_transactions", "type": "card", "data": {"card_name": "Transactions"}},
        {"id": "hdr_reports", "type": "header", "data": {"text": "Reports", "col": 12}},
        {"id": "card_reports", "type": "card", "data": {"card_name": "Reports"}}
    ]
    
    # Chart entries for the workspace charts child table
    workspace_charts = [
        {"chart_name": "Property Status Distribution", "label": "Property Status"},
        {"chart_name": "Restoration Project Status", "label": "Project Status"},
        {"chart_name": "Risk Level Distribution", "label": "Risk Level"},
        {"chart_name": "Inspection Status Overview", "label": "Inspection Status"},
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
        # Clear and repopulate charts child table
        workspace.set("charts", [])
        for chart_data in workspace_charts:
            workspace.append("charts", chart_data)
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
        
        # Add charts child table
        for chart_data in workspace_charts:
            workspace.append("charts", chart_data)
        
        workspace.insert(ignore_permissions=True)
    
    frappe.db.commit()


def _ensure_fixture_records():
    """Ensure fixture-like reference records needed by demo data exist.
    
    This is needed because fixture files are only loaded on install_app,
    not on migrate. On existing sites, newly added fixture values won't
    exist unless we create them here.
    """
    # Property Types
    for pt_name in ["Townhouse"]:
        if not frappe.db.exists("Property Type", pt_name):
            try:
                frappe.get_doc({
                    "doctype": "Property Type",
                    "property_type_name": pt_name,
                }).insert(ignore_permissions=True)
            except Exception:
                pass  # Skip if it already exists by another name

    # Material Categories
    for mc_name in ["Brick"]:
        if not frappe.db.exists("Material Category", {"category_name": mc_name}):
            try:
                frappe.get_doc({
                    "doctype": "Material Category",
                    "category_name": mc_name,
                }).insert(ignore_permissions=True)
            except Exception:
                pass

    # Time Capsule Categories
    for tc_name in ["Documentation"]:
        if not frappe.db.exists("Time Capsule Category", tc_name):
            try:
                frappe.get_doc({
                    "doctype": "Time Capsule Category",
                    "category_name": tc_name,
                }).insert(ignore_permissions=True)
            except Exception:
                pass

    # Historical Document Types
    for dt_name in ["Assessment Report"]:
        if not frappe.db.exists("Historical Document Type", dt_name):
            try:
                frappe.get_doc({
                    "doctype": "Historical Document Type",
                    "document_type_name": dt_name,
                }).insert(ignore_permissions=True)
            except Exception:
                pass

    frappe.db.commit()


def _safe_log_error(title, message):
    """Safely log an error, catching and ignoring secondary failures."""
    try:
        frappe.log_error(str(message)[:100], str(title)[:100])
    except Exception:
        pass
    # Also print to console so errors are visible during migrate
    try:
        print(f"[Demo Data Error] {title}: {str(message)[:100]}")
    except Exception:
        pass


def _create_section(label, create_fn):
    """Wrap a demo data section in its own try/except to prevent cascade failures."""
    try:
        create_fn()
        frappe.db.commit()
    except Exception as e:
        _safe_log_error("Demo Data", f"Section '{label}' failed: {str(e)[:80]}")


def create_demo_data():
    """Create demo data for testing and evaluating the app."""
    # First, ensure all reference records exist
    _ensure_fixture_records()

    # ===== LOCATIONS =====
    def create_locations():
        if not frappe.db.exists("Country", {"country_name": "United States"}):
            frappe.get_doc({"doctype": "Country", "country_name": "United States", "code": "US"}).insert(ignore_permissions=True)
        if not frappe.db.exists("State", {"state_name": "California"}):
            frappe.get_doc({"doctype": "State", "state_name": "California", "country": "United States"}).insert(ignore_permissions=True)
        if not frappe.db.exists("State", {"state_name": "Texas"}):
            frappe.get_doc({"doctype": "State", "state_name": "Texas", "country": "United States"}).insert(ignore_permissions=True)
        if not frappe.db.exists("District", {"district_name": "Los Angeles County"}):
            frappe.get_doc({"doctype": "District", "district_name": "Los Angeles County", "state": "California"}).insert(ignore_permissions=True)
        if not frappe.db.exists("District", {"district_name": "Harris County"}):
            frappe.get_doc({"doctype": "District", "district_name": "Harris County", "state": "Texas"}).insert(ignore_permissions=True)
        if not frappe.db.exists("City", {"city_name": "Los Angeles"}):
            frappe.get_doc({"doctype": "City", "city_name": "Los Angeles", "state": "California", "country": "United States"}).insert(ignore_permissions=True)
        if not frappe.db.exists("City", {"city_name": "Houston"}):
            frappe.get_doc({"doctype": "City", "city_name": "Houston", "state": "Texas", "country": "United States"}).insert(ignore_permissions=True)
    _create_section("Locations", create_locations)

    # ===== PEOPLES & ENTITIES =====
    def create_peoples():
        if not frappe.db.exists("Client", "sarah_johnson"):
            clients = [
                {"client_id": "sarah_johnson", "client_name": "Sarah Johnson", "email": "sarah.j@email.com", "phone": "+1-555-0101"},
                {"client_id": "michael_chen", "client_name": "Michael Chen", "email": "michael.c@email.com", "phone": "+1-555-0102"},
                {"client_id": "emily_rodriguez", "client_name": "Emily Rodriguez", "email": "emily.r@email.com", "phone": "+1-555-0103"},
            ]
            for cd in clients:
                frappe.get_doc({"doctype": "Client", **cd}).insert(ignore_permissions=True)
        if not frappe.db.exists("Contractor", {"contractor_name": "Premier Builders Inc"}):
            frappe.get_doc({"doctype": "Contractor", "contractor_id": "premier_builders_inc", "contractor_name": "Premier Builders Inc", "email": "info@premierbuilders.com", "phone": "+1-555-0201"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Contractor", "contractor_id": "heritage_restoration_llc", "contractor_name": "Heritage Restoration LLC", "email": "contact@heritagerestoration.com", "phone": "+1-555-0202"}).insert(ignore_permissions=True)
        if not frappe.db.exists("Engineer", {"engineer_name": "David Wilson"}):
            frappe.get_doc({"doctype": "Engineer", "engineer_id": "david_wilson", "engineer_name": "David Wilson", "email": "david.w@engineering.com", "phone": "+1-555-0301"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Engineer", "engineer_id": "lisa_thompson", "engineer_name": "Lisa Thompson", "email": "lisa.t@engineering.com", "phone": "+1-555-0302"}).insert(ignore_permissions=True)
        if not frappe.db.exists("Field Agent", "james_martinez"):
            frappe.get_doc({"doctype": "Field Agent", "field_agent_id": "james_martinez", "field_agent_name": "James Martinez", "email": "james.m@fieldservices.com", "phone": "+1-555-0401"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Field Agent", "field_agent_id": "amanda_lee", "field_agent_name": "Amanda Lee", "email": "amanda.l@fieldservices.com", "phone": "+1-555-0402"}).insert(ignore_permissions=True)
        if not frappe.db.exists("Department", "property_acquisitions"):
            frappe.get_doc({"doctype": "Department", "department_id": "property_acquisitions", "department_name": "Property Acquisitions", "contact_person": "Robert Brown", "email": "acquisitions@company.com"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Department", "department_id": "restoration_operations", "department_name": "Restoration Operations", "contact_person": "Karen Davis", "email": "operations@company.com"}).insert(ignore_permissions=True)
    _create_section("Peoples & Entities", create_peoples)

    # ===== ABANDONED PROPERTIES =====
    def create_properties():
        property_list = [
            {"property_name": "Oakwood Manor", "address": "123 Oak Street", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "property_type": "House", "property_category": "Residential", "property_status": "Under Restoration", "risk_level": "Medium", "ownership_type": "Private", "estimated_area": 2500},
            {"property_name": "Maple Warehouse", "address": "456 Maple Avenue", "city": "Houston", "state": "Texas", "country": "United States", "district": "Harris County", "property_type": "Factory", "property_category": "Commercial", "property_status": "Vacant", "risk_level": "High", "ownership_type": "Company", "estimated_area": 15000},
            {"property_name": "Pine Street Apartments", "address": "789 Pine Road", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "property_type": "Apartment", "property_category": "Residential", "property_status": "Restored", "risk_level": "Low", "ownership_type": "Corporate", "estimated_area": 8000},
            {"property_name": "Cedar Mill", "address": "321 Cedar Lane", "city": "Houston", "state": "Texas", "country": "United States", "district": "Harris County", "property_type": "Warehouse", "property_category": "Industrial", "property_status": "Abandoned", "risk_level": "Critical", "ownership_type": "Private", "estimated_area": 20000},
            {"property_name": "Birchwood Villa", "address": "555 Birch Boulevard", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "property_type": "Townhouse", "property_category": "Residential", "property_status": "Under Restoration", "risk_level": "Medium", "ownership_type": "Trust", "estimated_area": 1800},
        ]
        for p in property_list:
            if frappe.db.exists("Abandoned Property", p["property_name"]):
                continue
            try:
                doc = frappe.get_doc({"doctype": "Abandoned Property", "naming_series": "AP-.YYYY.-", **p})
                doc.insert(ignore_permissions=True)
            except Exception as e:
                _safe_log_error("Demo Data", f"Property '{p['property_name']}' failed: {str(e)[:80]}")
    _create_section("Abandoned Properties", create_properties)

    # ===== CLIENT PROPERTY REPORTS =====
    def create_client_reports():
        report_list = [
            {"report_id": "CPR-001", "property_name": "Oakwood Manor", "client": "sarah_johnson", "client_name": "Sarah Johnson", "address": "123 Oak Street", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "risk_level": "Medium", "status": "Restoration Assigned"},
            {"report_id": "CPR-002", "property_name": "Cedar Mill", "client": "michael_chen", "client_name": "Michael Chen", "address": "321 Cedar Lane", "city": "Houston", "state": "Texas", "country": "United States", "district": "Harris County", "risk_level": "Critical", "status": "Verified"},
            {"report_id": "CPR-003", "property_name": "Birchwood Villa", "client": "emily_rodriguez", "client_name": "Emily Rodriguez", "address": "555 Birch Boulevard", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "risk_level": "Medium", "status": "New"},
        ]
        for rd in report_list:
            if not frappe.db.exists("Client Property Report", {"report_id": rd["report_id"]}):
                frappe.get_doc({"doctype": "Client Property Report", **rd}).insert(ignore_permissions=True)
    _create_section("Client Property Reports", create_client_reports)        # ===== PROPERTY INSPECTIONS =====
    def create_inspections():
        inspection_list = [
            {"inspection_id": "INS-001", "property": "Oakwood Manor", "inspector": "james_martinez", "engineer": "david_wilson", "inspection_date": "2026-06-15 10:00:00", "inspection_type": "Initial Inspection", "inspection_status": "Completed", "structure_condition": "Fair", "foundation_condition": "Good", "roof_condition": "Poor", "risk_level": "Medium", "estimated_restoration_cost": 150000},
            {"inspection_id": "INS-002", "property": "Cedar Mill", "inspector": "amanda_lee", "engineer": "lisa_thompson", "inspection_date": "2026-06-20 14:00:00", "inspection_type": "Initial Inspection", "inspection_status": "Completed", "structure_condition": "Poor", "foundation_condition": "Fair", "roof_condition": "Critical", "risk_level": "Critical", "estimated_restoration_cost": 450000},
            {"inspection_id": "INS-003", "property": "Birchwood Villa", "inspector": "james_martinez", "engineer": "david_wilson", "inspection_date": "2026-07-01 09:00:00", "inspection_type": "Initial Inspection", "inspection_status": "In Progress", "structure_condition": "Good", "foundation_condition": "Good", "roof_condition": "Fair", "risk_level": "Medium", "estimated_restoration_cost": 85000},
        ]
        for ins in inspection_list:
            if not frappe.db.exists("Property Inspection", {"inspection_id": ins["inspection_id"]}):
                frappe.get_doc({"doctype": "Property Inspection", **ins}).insert(ignore_permissions=True)
    _create_section("Property Inspections", create_inspections)

    # ===== RESTORATION PROJECTS =====
    def create_projects():
        if not frappe.db.exists("Restoration Project", {"project_name": "Oakwood Manor Restoration"}):
            frappe.get_doc({"doctype": "Restoration Project", "naming_series": "RP-.YYYY.-", "project_name": "Oakwood Manor Restoration", "property": "Oakwood Manor", "project_status": "In Progress", "project_priority": "High", "start_date": "2026-07-01", "expected_end_date": "2026-12-31", "engineer": "david_wilson", "contractor": "premier_builders_inc", "estimated_cost": 150000, "progress_percentage": 35, "current_phase": "Structural Repairs"}).insert(ignore_permissions=True)
        if not frappe.db.exists("Restoration Project", {"project_name": "Birchwood Villa Restoration"}):
            frappe.get_doc({"doctype": "Restoration Project", "naming_series": "RP-.YYYY.-", "project_name": "Birchwood Villa Restoration", "property": "Birchwood Villa", "project_status": "Planning", "project_priority": "Medium", "start_date": "2026-08-15", "expected_end_date": "2027-02-28", "engineer": "lisa_thompson", "contractor": "heritage_restoration_llc", "estimated_cost": 85000, "progress_percentage": 10, "current_phase": "Assessment & Planning"}).insert(ignore_permissions=True)
    _create_section("Restoration Projects", create_projects)

    # ===== RESTORATION PROGRESS =====
    def create_progress():
        progress_list = [
            {"progress_id": "PRG-001", "restoration_project": "Oakwood Manor Restoration", "property": "Oakwood Manor", "update_date": "2026-07-15", "progress_percentage": 15, "work_completed": "Initial debris removal and structural assessment", "current_phase": "Assessment"},
            {"progress_id": "PRG-002", "restoration_project": "Oakwood Manor Restoration", "property": "Oakwood Manor", "update_date": "2026-08-01", "progress_percentage": 25, "work_completed": "Roof protection installed, interior demolition done", "current_phase": "Structural Repairs"},
            {"progress_id": "PRG-003", "restoration_project": "Oakwood Manor Restoration", "property": "Oakwood Manor", "update_date": "2026-08-20", "progress_percentage": 35, "work_completed": "Foundation repairs done, electrical rewiring started", "current_phase": "Structural Repairs"},
        ]
        for pe in progress_list:
            frappe.get_doc({"doctype": "Restoration Progress", **pe}).insert(ignore_permissions=True)
    _create_section("Restoration Progress", create_progress)

    # ===== MATERIAL SALVAGE =====
    def create_materials():
        material_list = [
            {"material_id": "MTL-001", "property": "Oakwood Manor", "material_name": "Vintage Hardwood Flooring", "material_type": "Wooden Materials", "material_category": "Wood", "quantity": 500, "unit": "Sq Ft", "condition": "Good", "status": "Available", "salvage_date": "2026-07-20"},
            {"material_id": "MTL-002", "property": "Oakwood Manor", "material_name": "Brass Door Handles", "material_type": "Doors", "material_category": "Metal", "quantity": 25, "unit": "Pieces", "condition": "Excellent", "status": "Available", "salvage_date": "2026-07-20"},
            {"material_id": "MTL-003", "property": "Oakwood Manor", "material_name": "Clay Roof Tiles", "material_type": "Tiles", "material_category": "Brick", "quantity": 2000, "unit": "Pieces", "condition": "Fair", "status": "Available", "salvage_date": "2026-07-25"},
            {"material_id": "MTL-004", "property": "Cedar Mill", "material_name": "Steel Beams", "material_type": "Steel Materials", "material_category": "Metal", "quantity": 50, "unit": "Pieces", "condition": "Good", "status": "Available", "salvage_date": "2026-08-01"},
        ]
        for m in material_list:
            frappe.get_doc({"doctype": "Material Salvage", **m}).insert(ignore_permissions=True)
    _create_section("Material Salvage", create_materials)

    # ===== DIGITAL TIME CAPSULE =====
    def create_time_capsule():
        if not frappe.db.exists("Digital Time Capsule", {"capsule_name": "Oakwood Manor History"}):
            frappe.get_doc({"doctype": "Digital Time Capsule", "capsule_id": "DTC-001", "capsule_name": "Oakwood Manor History", "property": "Oakwood Manor", "category": "Documentation", "title": "Oakwood Manor - Original Blueprints", "description": "Original architectural blueprints from 1925, scanned and preserved", "record_date": "2026-07-01", "preservation_method": "Digital Only", "status": "Sealed", "creation_date": "2026-07-01"}).insert(ignore_permissions=True)
    _create_section("Digital Time Capsule", create_time_capsule)

    # ===== HISTORICAL RECORD =====
    def create_historical():
        if not frappe.db.exists("Historical Record", {"title": "Oakwood Manor - Historical Assessment"}):
            frappe.get_doc({"doctype": "Historical Record", "record_id": "HST-001", "title": "Oakwood Manor - Historical Assessment", "property": "Oakwood Manor", "document_type": "Assessment Report", "description": "Historical significance assessment for Oakwood Manor (1925) by architect Frank Peterson", "record_date": "2026-06-20"}).insert(ignore_permissions=True)
    _create_section("Historical Record", create_historical)

    # ===== REWARD CLAIMS =====
    def create_rewards():
        if not frappe.db.exists("Reward Claim", {"claim_id": "RWD-001"}):
            frappe.get_doc({"doctype": "Reward Claim", "claim_id": "RWD-001", "report_name": "CPR-002", "property_name": "Cedar Mill", "client": "michael_chen", "client_name": "Michael Chen", "reward_type": "Cash", "reward_amount": 5000, "claim_status": "Approved"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Reward Claim", "claim_id": "RWD-002", "report_name": "CPR-003", "property_name": "Birchwood Villa", "client": "emily_rodriguez", "client_name": "Emily Rodriguez", "reward_type": "Cash", "reward_amount": 2500, "claim_status": "Pending"}).insert(ignore_permissions=True)
    _create_section("Reward Claims", create_rewards)

    frappe.publish_realtime("bench_event", {"message": "Demo data creation completed"})


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
