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
    """Create the Abandoned Property Restoration workspace with proper cards."""
    
    # Delete existing workspace if it exists
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        frappe.delete_doc("Workspace", "Abandoned Property Restoration", force=True)
        print("Deleted existing workspace")
    
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
    
    # Add roles
    roles = ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]
    for role in roles:
        workspace.append("roles", {"role": role})
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # ERPNext format: cards use 'card_name' not 'label', headers use 'text' with HTML
    workspace_content = [
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Property Masters", "col": 4}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Material Masters", "col": 4}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "People", "col": 4}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Organization", "col": 4}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Property Management", "col": 4}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Restoration", "col": 4}},
        {"id": generate_id(), "type": "card", "data": {"card_name": "Rewards", "col": 4}},
    ]
    
    # Update via SQL
    frappe.db.sql("""
        UPDATE `tabWorkspace` 
        SET content = %s 
        WHERE name = %s
    """, (frappe.json.dumps(workspace_content), "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} blocks!".format(len(workspace_content)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
