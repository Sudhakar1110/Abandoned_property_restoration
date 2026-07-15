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
    
    # First create the workspace without shortcuts
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
    
    # Now add shortcuts to the child table via SQL
    shortcuts = [
        {"label": "Property Category", "shortcut_name": "Property Category", "url": "/app/property-category", "icon": "fa fa-th", "col": 3},
        {"label": "Property Type", "shortcut_name": "Property Type", "url": "/app/property-type", "icon": "fa fa-building", "col": 3},
        {"label": "Restoration Category", "shortcut_name": "Restoration Category", "url": "/app/restoration-category", "icon": "fa fa-refresh", "col": 3},
        {"label": "Material Category", "shortcut_name": "Material Category", "url": "/app/material-category", "icon": "fa fa-cubes", "col": 3},
        {"label": "Material Condition", "shortcut_name": "Material Condition", "url": "/app/material-condition", "icon": "fa fa-check-circle", "col": 3},
        {"label": "Citizen", "shortcut_name": "Citizen", "url": "/app/citizen", "icon": "fa fa-user", "col": 3},
        {"label": "Contractor", "shortcut_name": "Contractor", "url": "/app/contractor", "icon": "fa fa-briefcase", "col": 3},
        {"label": "Engineer", "shortcut_name": "Engineer", "url": "/app/engineer", "icon": "fa fa-wrench", "col": 3},
        {"label": "Inspector", "shortcut_name": "Inspector", "url": "/app/inspector", "icon": "fa fa-search", "col": 3},
        {"label": "Government Department", "shortcut_name": "Government Department", "url": "/app/government-department", "icon": "fa fa-institution", "col": 3},
        {"label": "Reward Type", "shortcut_name": "Reward Type", "url": "/app/reward-type", "icon": "fa fa-gift", "col": 3},
        {"label": "Abandoned Property", "shortcut_name": "Abandoned Property", "url": "/app/abandoned-property", "icon": "fa fa-home", "col": 3},
        {"label": "Citizen Property Report", "shortcut_name": "Citizen Property Report", "url": "/app/citizen-property-report", "icon": "fa fa-flag", "col": 3},
        {"label": "Property Inspection", "shortcut_name": "Property Inspection", "url": "/app/property-inspection", "icon": "fa fa-clipboard", "col": 3},
        {"label": "Restoration Project", "shortcut_name": "Restoration Project", "url": "/app/restoration-project", "icon": "fa fa-tasks", "col": 3},
        {"label": "Material Salvage", "shortcut_name": "Material Salvage", "url": "/app/material-salvage", "icon": "fa fa-recycle", "col": 3},
        {"label": "Material Exchange", "shortcut_name": "Material Exchange", "url": "/app/material-exchange", "icon": "fa fa-exchange", "col": 3},
        {"label": "Material Sale", "shortcut_name": "Material Sale", "url": "/app/material-sale", "icon": "fa fa-shopping-cart", "col": 3},
        {"label": "Reward Claim", "shortcut_name": "Reward Claim", "url": "/app/reward-claim", "icon": "fa fa-money", "col": 3},
    ]
    
    for sc in shortcuts:
        # Insert into Workspace Shortcut table
        ws_shortcut = frappe.new_doc("Workspace Shortcut")
        ws_shortcut.parent = "Abandoned Property Restoration"
        ws_shortcut.parentfield = "shortcuts"
        ws_shortcut.parenttype = "Workspace"
        ws_shortcut.label = sc["label"]
        ws_shortcut.shortcut_name = sc["shortcut_name"]
        ws_shortcut.url = sc["url"]
        ws_shortcut.icon = sc["icon"]
        ws_shortcut.col = sc["col"]
        ws_shortcut.insert(ignore_permissions=True)
    
    frappe.db.commit()
    
    # Create content JSON
    content_blocks = [
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
    ]
    
    # Masters shortcuts
    masters = shortcuts[:11]
    for sc in masters:
        content_blocks.append({"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": sc["shortcut_name"], "col": sc["col"]}})
    
    content_blocks.append({"id": generate_id(), "type": "spacer", "data": {"col": 12}})
    content_blocks.append({"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}})
    
    # Transactions shortcuts
    transactions = shortcuts[11:]
    for sc in transactions:
        content_blocks.append({"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": sc["shortcut_name"], "col": sc["col"]}})
    
    # Update content via SQL
    frappe.db.sql("""
        UPDATE `tabWorkspace` 
        SET content = %s 
        WHERE name = %s
    """, (frappe.json.dumps(content_blocks), "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} shortcuts!".format(len(shortcuts)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
