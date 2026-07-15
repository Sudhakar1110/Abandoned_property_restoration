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
    
    # Add shortcuts to child table - this is what Frappe v15 uses
    shortcuts = [
        "Property Category", "Property Type", "Restoration Category", "Material Category",
        "Material Condition", "Citizen", "Contractor", "Engineer", "Inspector",
        "Government Department", "Reward Type", "Abandoned Property", "Citizen Property Report",
        "Property Inspection", "Restoration Project", "Material Salvage", "Material Exchange",
        "Material Sale", "Reward Claim"
    ]
    
    for sc_name in shortcuts:
        workspace.append("shortcuts", {
            "label": sc_name,
            "shortcut_name": sc_name,
            "col": 3
        })
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Create content JSON - matching ERPNext format exactly
    content = json.dumps([
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Property Category", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Property Type", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Restoration Category", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Category", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Condition", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Citizen", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Contractor", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Engineer", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Inspector", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Government Department", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Reward Type", "col": 3}},
        {"id": generate_id(), "type": "spacer", "data": {"col": 12}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Abandoned Property", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Citizen Property Report", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Property Inspection", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Restoration Project", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Salvage", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Exchange", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Material Sale", "col": 3}},
        {"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": "Reward Claim", "col": 3}},
        {"id": generate_id(), "type": "spacer", "data": {"col": 12}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} shortcuts!".format(len(shortcuts)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
