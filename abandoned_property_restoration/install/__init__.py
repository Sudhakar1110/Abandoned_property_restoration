import frappe


def after_install():
    create_module_def()
    create_roles()
    create_reports()
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


def create_demo_data():
    """Create demo data for testing and evaluating the app."""        if frappe.db.exists("Abandoned Property", {"property_name": "Oakwood Manor"}):
        return  # Demo data already exists, skip
    
    try:
        # ===== LOCATIONS =====
        if not frappe.db.exists("Country", {"country_name": "United States"}):
            country = frappe.get_doc({"doctype": "Country", "country_name": "United States", "code": "US"})
            country.insert(ignore_permissions=True)
        
        if not frappe.db.exists("State", {"state_name": "California"}):
            state = frappe.get_doc({"doctype": "State", "state_name": "California", "country": "United States"})
            state.insert(ignore_permissions=True)
        
        if not frappe.db.exists("State", {"state_name": "Texas"}):
            state = frappe.get_doc({"doctype": "State", "state_name": "Texas", "country": "United States"})
            state.insert(ignore_permissions=True)
        
        if not frappe.db.exists("District", {"district_name": "Los Angeles County"}):
            district = frappe.get_doc({"doctype": "District", "district_name": "Los Angeles County", "state": "California"})
            district.insert(ignore_permissions=True)
        
        if not frappe.db.exists("District", {"district_name": "Harris County"}):
            district = frappe.get_doc({"doctype": "District", "district_name": "Harris County", "state": "Texas"})
            district.insert(ignore_permissions=True)
        
        if not frappe.db.exists("City", {"city_name": "Los Angeles"}):
            city = frappe.get_doc({"doctype": "City", "city_name": "Los Angeles", "state": "California", "country": "United States"})
            city.insert(ignore_permissions=True)
        
        if not frappe.db.exists("City", {"city_name": "Houston"}):
            city = frappe.get_doc({"doctype": "City", "city_name": "Houston", "state": "Texas", "country": "United States"})
            city.insert(ignore_permissions=True)
        
        frappe.db.commit()  # Commit locations before creating other records

        # ===== PEOPLES & ENTITIES =====
        client_names = ["sarah_johnson", "michael_chen", "emily_rodriguez"]
        if not frappe.db.exists("Client", client_names[0]):
            clients = [
                {"client_id": "sarah_johnson", "client_name": "Sarah Johnson", "email": "sarah.j@email.com", "phone": "+1-555-0101"},
                {"client_id": "michael_chen", "client_name": "Michael Chen", "email": "michael.c@email.com", "phone": "+1-555-0102"},
                {"client_id": "emily_rodriguez", "client_name": "Emily Rodriguez", "email": "emily.r@email.com", "phone": "+1-555-0103"},
            ]
            for cd in clients:
                frappe.get_doc({"doctype": "Client", **cd}).insert(ignore_permissions=True)

        if not frappe.db.exists("Contractor", "Premier Builders Inc"):
            frappe.get_doc({"doctype": "Contractor", "contractor_name": "Premier Builders Inc", "email": "info@premierbuilders.com", "phone": "+1-555-0201"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Contractor", "contractor_name": "Heritage Restoration LLC", "email": "contact@heritagerestoration.com", "phone": "+1-555-0202"}).insert(ignore_permissions=True)

        if not frappe.db.exists("Engineer", "David Wilson"):
            frappe.get_doc({"doctype": "Engineer", "engineer_id": "david_wilson", "engineer_name": "David Wilson", "email": "david.w@engineering.com", "phone": "+1-555-0301"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Engineer", "engineer_id": "lisa_thompson", "engineer_name": "Lisa Thompson", "email": "lisa.t@engineering.com", "phone": "+1-555-0302"}).insert(ignore_permissions=True)

        if not frappe.db.exists("Field Agent", "james_martinez"):
            frappe.get_doc({"doctype": "Field Agent", "field_agent_id": "james_martinez", "field_agent_name": "James Martinez", "email": "james.m@fieldservices.com", "phone": "+1-555-0401"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Field Agent", "field_agent_id": "amanda_lee", "field_agent_name": "Amanda Lee", "email": "amanda.l@fieldservices.com", "phone": "+1-555-0402"}).insert(ignore_permissions=True)

        if not frappe.db.exists("Department", "property_acquisitions"):
            frappe.get_doc({"doctype": "Department", "department_id": "property_acquisitions", "department_name": "Property Acquisitions", "contact_person": "Robert Brown", "email": "acquisitions@company.com"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Department", "department_id": "restoration_operations", "department_name": "Restoration Operations", "contact_person": "Karen Davis", "email": "operations@company.com"}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== ABANDONED PROPERTIES =====
        property_list = [
            {"property_name": "Oakwood Manor", "address": "123 Oak Street", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "property_type": "House", "property_category": "Residential", "property_status": "Under Restoration", "risk_level": "Medium", "ownership_type": "Private", "estimated_area": 2500},
            {"property_name": "Maple Warehouse", "address": "456 Maple Avenue", "city": "Houston", "state": "Texas", "country": "United States", "district": "Harris County", "property_type": "Factory", "property_category": "Commercial", "property_status": "Identified", "risk_level": "High", "ownership_type": "Company", "estimated_area": 15000},
            {"property_name": "Pine Street Apartments", "address": "789 Pine Road", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "property_type": "Apartment", "property_category": "Residential", "property_status": "Restored", "risk_level": "Low", "ownership_type": "Corporate", "estimated_area": 8000},
            {"property_name": "Cedar Mill", "address": "321 Cedar Lane", "city": "Houston", "state": "Texas", "country": "United States", "district": "Harris County", "property_type": "Warehouse", "property_category": "Industrial", "property_status": "Under Assessment", "risk_level": "Critical", "ownership_type": "Private", "estimated_area": 20000},
            {"property_name": "Birchwood Villa", "address": "555 Birch Boulevard", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "property_type": "Townhouse", "property_category": "Residential", "property_status": "Under Restoration", "risk_level": "Medium", "ownership_type": "Trust", "estimated_area": 1800},
        ]
        for idx, p in enumerate(property_list, 1):
            p["naming_series"] = "AP-.YYYY.-"
            doc = frappe.get_doc({"doctype": "Abandoned Property", **p})
            doc.insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== CLIENT PROPERTY REPORTS =====
        report_list = [
            {"report_id": "CPR-001", "property_name": "Oakwood Manor", "client": "sarah_johnson", "client_name": "Sarah Johnson", "address": "123 Oak Street", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "risk_level": "Medium", "status": "Restoration Assigned"},
            {"report_id": "CPR-002", "property_name": "Cedar Mill", "client": "michael_chen", "client_name": "Michael Chen", "address": "321 Cedar Lane", "city": "Houston", "state": "Texas", "country": "United States", "district": "Harris County", "risk_level": "Critical", "status": "Verified"},
            {"report_id": "CPR-003", "property_name": "Birchwood Villa", "client": "emily_rodriguez", "client_name": "Emily Rodriguez", "address": "555 Birch Boulevard", "city": "Los Angeles", "state": "California", "country": "United States", "district": "Los Angeles County", "risk_level": "Medium", "status": "New"},
        ]
        for rd in report_list:
            if not frappe.db.exists("Client Property Report", {"report_id": rd["report_id"]}):
                frappe.get_doc({"doctype": "Client Property Report", **rd}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== PROPERTY INSPECTIONS =====
        inspection_list = [
            {"inspection_id": "INS-001", "property": "Oakwood Manor", "field_agent": "james_martinez", "engineer": "david_wilson", "inspection_date": "2026-06-15 10:00:00", "inspection_type": "Initial Inspection", "inspection_status": "Completed", "structure_condition": "Fair", "foundation_condition": "Good", "roof_condition": "Poor", "risk_level": "Medium", "estimated_restoration_cost": 150000},
            {"inspection_id": "INS-002", "property": "Cedar Mill", "field_agent": "amanda_lee", "engineer": "lisa_thompson", "inspection_date": "2026-06-20 14:00:00", "inspection_type": "Initial Inspection", "inspection_status": "Completed", "structure_condition": "Poor", "foundation_condition": "Fair", "roof_condition": "Critical", "risk_level": "Critical", "estimated_restoration_cost": 450000},
            {"inspection_id": "INS-003", "property": "Birchwood Villa", "field_agent": "james_martinez", "engineer": "david_wilson", "inspection_date": "2026-07-01 09:00:00", "inspection_type": "Initial Inspection", "inspection_status": "In Progress", "structure_condition": "Good", "foundation_condition": "Good", "roof_condition": "Fair", "risk_level": "Medium", "estimated_restoration_cost": 85000},
        ]
        for ins in inspection_list:
            if not frappe.db.exists("Property Inspection", {"inspection_id": ins["inspection_id"]}):
                frappe.get_doc({"doctype": "Property Inspection", **ins}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== RESTORATION PROJECTS =====
        if not frappe.db.exists("Restoration Project", {"project_name": "Oakwood Manor Restoration"}):
            frappe.get_doc({"doctype": "Restoration Project", "naming_series": "RP-.YYYY.-", "project_name": "Oakwood Manor Restoration", "property": "Oakwood Manor", "project_status": "In Progress", "project_priority": "High", "start_date": "2026-07-01", "expected_end_date": "2026-12-31", "engineer": "david_wilson", "contractor": "Premier Builders Inc", "estimated_cost": 150000, "progress_percentage": 35, "current_phase": "Structural Repairs"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Restoration Project", "naming_series": "RP-.YYYY.-", "project_name": "Birchwood Villa Restoration", "property": "Birchwood Villa", "project_status": "Planning", "project_priority": "Medium", "start_date": "2026-08-15", "expected_end_date": "2027-02-28", "engineer": "lisa_thompson", "contractor": "Heritage Restoration LLC", "estimated_cost": 85000, "progress_percentage": 10, "current_phase": "Assessment & Planning"}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== RESTORATION PROGRESS =====
        progress_list = [
            {"restoration_project": "Oakwood Manor Restoration", "property": "Oakwood Manor", "update_date": "2026-07-15", "progress_percentage": 15, "work_completed": "Initial debris removal and structural assessment", "current_phase": "Assessment"},
            {"restoration_project": "Oakwood Manor Restoration", "property": "Oakwood Manor", "update_date": "2026-08-01", "progress_percentage": 25, "work_completed": "Roof protection installed, interior demolition done", "current_phase": "Structural Repairs"},
            {"restoration_project": "Oakwood Manor Restoration", "property": "Oakwood Manor", "update_date": "2026-08-20", "progress_percentage": 35, "work_completed": "Foundation repairs done, electrical rewiring started", "current_phase": "Structural Repairs"},
        ]
        for pe in progress_list:
            frappe.get_doc({"doctype": "Restoration Progress", **pe}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== MATERIAL SALVAGE =====
        material_list = [
            {"property": "Oakwood Manor", "material_name": "Vintage Hardwood Flooring", "material_category": "Wood", "quantity": 500, "condition": "Good", "status": "Available"},
            {"property": "Oakwood Manor", "material_name": "Brass Door Handles", "material_category": "Metal", "quantity": 25, "condition": "Excellent", "status": "Available"},
            {"property": "Oakwood Manor", "material_name": "Clay Roof Tiles", "material_category": "Brick", "quantity": 2000, "condition": "Fair", "status": "Available"},
            {"property": "Cedar Mill", "material_name": "Steel Beams", "material_category": "Metal", "quantity": 50, "condition": "Good", "status": "Available"},
        ]
        for m in material_list:
            frappe.get_doc({"doctype": "Material Salvage", **m}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== DIGITAL TIME CAPSULE =====
        if not frappe.db.exists("Digital Time Capsule", {"capsule_name": "Oakwood Manor History"}):
            frappe.get_doc({"doctype": "Digital Time Capsule", "capsule_name": "Oakwood Manor History", "property": "Oakwood Manor", "category": "Documentation", "title": "Oakwood Manor - Original Blueprints", "description": "Original architectural blueprints from 1925, scanned and preserved", "record_date": "2026-07-01", "preservation_method": "Digital Only", "status": "Active"}).insert(ignore_permissions=True)

        # ===== HISTORICAL RECORD =====
        if not frappe.db.exists("Historical Record", {"record_title": "Oakwood Manor - Historical Assessment"}):
            frappe.get_doc({"doctype": "Historical Record", "record_title": "Oakwood Manor - Historical Assessment", "property": "Oakwood Manor", "document_type": "Assessment Report", "description": "Historical significance assessment for Oakwood Manor (1925) by architect Frank Peterson", "record_date": "2026-06-20", "record_status": "Archived"}).insert(ignore_permissions=True)

        frappe.db.commit()

        # ===== REWARD CLAIMS =====
        if not frappe.db.exists("Reward Claim", {"claim_id": "RWD-001"}):
            frappe.get_doc({"doctype": "Reward Claim", "claim_id": "RWD-001", "property_name": "Cedar Mill", "client": "michael_chen", "client_name": "Michael Chen", "reward_type": "Cash", "reward_amount": 5000, "claim_status": "Approved"}).insert(ignore_permissions=True)
            frappe.get_doc({"doctype": "Reward Claim", "claim_id": "RWD-002", "property_name": "Birchwood Villa", "client": "emily_rodriguez", "client_name": "Emily Rodriguez", "reward_type": "Cash", "reward_amount": 2500, "claim_status": "Pending"}).insert(ignore_permissions=True)

        frappe.db.commit()
        frappe.publish_realtime("bench_event", {"message": "Demo data created successfully"})
    except Exception as e:
        frappe.log_error(f"Could not create demo data: {e}", "Demo Data Creation")


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
