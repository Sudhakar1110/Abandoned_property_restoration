#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.create_workspace.create_abandoned_property_workspace
"""

import frappe
import json
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
    for role in ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]:
        workspace.append("roles", {"role": role})
    
    # Add shortcuts with URLs
    shortcuts = [
        {"name": "Property Category", "url": "/app/property-category"},
        {"name": "Property Type", "url": "/app/property-type"},
        {"name": "Restoration Category", "url": "/app/restoration-category"},
        {"name": "Material Category", "url": "/app/material-category"},
        {"name": "Material Condition", "url": "/app/material-condition"},
        {"name": "Citizen", "url": "/app/citizen"},
        {"name": "Contractor", "url": "/app/contractor"},
        {"name": "Engineer", "url": "/app/engineer"},
        {"name": "Inspector", "url": "/app/inspector"},
        {"name": "Government Department", "url": "/app/government-department"},
        {"name": "Reward Type", "url": "/app/reward-type"},
        {"name": "Abandoned Property", "url": "/app/abandoned-property"},
        {"name": "Citizen Property Report", "url": "/app/citizen-property-report"},
        {"name": "Property Inspection", "url": "/app/property-inspection"},
        {"name": "Restoration Project", "url": "/app/restoration-project"},
        {"name": "Material Salvage", "url": "/app/material-salvage"},
        {"name": "Material Exchange", "url": "/app/material-exchange"},
        {"name": "Material Sale", "url": "/app/material-sale"},
        {"name": "Reward Claim", "url": "/app/reward-claim"},
    ]
    
    for sc in shortcuts:
        workspace.append("shortcuts", {
            "label": sc["name"],
            "shortcut_name": sc["name"],
            "url": sc["url"],
            "col": 3
        })
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Create content JSON with URLs
    content = json.dumps([
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Property Category", "url": "/app/property-category", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Property Type", "url": "/app/property-type", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Restoration Category", "url": "/app/restoration-category", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Category", "url": "/app/material-category", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Condition", "url": "/app/material-condition", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Citizen", "url": "/app/citizen", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Contractor", "url": "/app/contractor", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Engineer", "url": "/app/engineer", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Inspector", "url": "/app/inspector", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Government Department", "url": "/app/government-department", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Reward Type", "url": "/app/reward-type", "col": 3}},
        {"id": generate_id(), "type": "spacer", "data": {"col": 12}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Abandoned Property", "url": "/app/abandoned-property", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Citizen Property Report", "url": "/app/citizen-property-report", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Property Inspection", "url": "/app/property-inspection", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Restoration Project", "url": "/app/restoration-project", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Salvage", "url": "/app/material-salvage", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Exchange", "url": "/app/material-exchange", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Sale", "url": "/app/material-sale", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Reward Claim", "url": "/app/reward-claim", "col": 3}},
        {"id": generate_id(), "type": "spacer", "data": {"col": 12}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} shortcuts with URLs!".format(len(shortcuts)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
