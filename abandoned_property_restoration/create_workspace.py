#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.create_workspace.create_abandoned_property_workspace
"""

import frappe
import secrets
import string

def generate_id():
    """Generate a random ID like ERPNext does."""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(10))

def create_abandoned_property_workspace():
    """Create the Abandoned Property Restoration workspace."""
    
    # Delete existing workspace if it exists
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        frappe.delete_doc("Workspace", "Abandoned Property Restoration", force=True)
        print("Deleted existing workspace")
    
    # Create workspace
    workspace = frappe.new_doc("Workspace")
    workspace.name = "Abandoned Property Restoration"
    workspace.title = "Abandoned Property Restoration"
    workspace.label = "Abandoned Property Restoration"
    workspace.icon = "fa fa-home"
    workspace.module = "restoration"
    workspace.public = 1
    workspace.sequence_id = 1
    workspace.is_standard = 1
    
    # Add roles
    roles = ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]
    for role in roles:
        workspace.append("roles", {"role": role})
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Add shortcuts to child table
    shortcuts = [
        "Property Category", "Property Type", "Restoration Category", "Material Category", "Material Condition",
        "Citizen", "Contractor", "Engineer", "Inspector", "Government Department", "Reward Type",
        "Abandoned Property", "Citizen Property Report", "Property Inspection", "Restoration Project",
        "Material Salvage", "Material Exchange", "Material Sale", "Reward Claim"
    ]
    
    for sc_name in shortcuts:
        ws_sc = frappe.new_doc("Workspace Shortcut")
        ws_sc.parent = "Abandoned Property Restoration"
        ws_sc.parentfield = "shortcuts"
        ws_sc.parenttype = "Workspace"
        ws_sc.label = sc_name
        ws_sc.shortcut_name = sc_name
        ws_sc.col = 3
        ws_sc.insert(ignore_permissions=True)
    
    frappe.db.commit()
    
    # Create content JSON with number cards for each section
    content_blocks = [
        {"id": generate_id(), "type": "card", "data": {"card_name": "Masters", "col": 4}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Transactions", "col": 4}},
    ]
    
    # Update content via SQL
    frappe.db.sql("""
        UPDATE `tabWorkspace` 
        SET content = %s 
        WHERE name = %s
    """, (frappe.json.dumps(content_blocks), "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("- Shortcuts: {0}".format(len(shortcuts)))
    print("- Cards: Masters, Transactions")
    print("Please hard refresh your browser (Ctrl+Shift+R)")
