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
    
    # Add shortcuts to the shortcuts child table
    shortcuts = [
        {"label": "Property Category", "shortcut_name": "Property Category", "url": "/app/property-category"},
        {"label": "Property Type", "shortcut_name": "Property Type", "url": "/app/property-type"},
        {"label": "Restoration Category", "shortcut_name": "Restoration Category", "url": "/app/restoration-category"},
        {"label": "Material Category", "shortcut_name": "Material Category", "url": "/app/material-category"},
        {"label": "Material Condition", "shortcut_name": "Material Condition", "url": "/app/material-condition"},
        {"label": "Citizen", "shortcut_name": "Citizen", "url": "/app/citizen"},
        {"label": "Contractor", "shortcut_name": "Contractor", "url": "/app/contractor"},
        {"label": "Engineer", "shortcut_name": "Engineer", "url": "/app/engineer"},
        {"label": "Inspector", "shortcut_name": "Inspector", "url": "/app/inspector"},
        {"label": "Government Department", "shortcut_name": "Government Department", "url": "/app/government-department"},
        {"label": "Reward Type", "shortcut_name": "Reward Type", "url": "/app/reward-type"},
        {"label": "Abandoned Property", "shortcut_name": "Abandoned Property", "url": "/app/abandoned-property"},
        {"label": "Citizen Property Report", "shortcut_name": "Citizen Property Report", "url": "/app/citizen-property-report"},
        {"label": "Property Inspection", "shortcut_name": "Property Inspection", "url": "/app/property-inspection"},
        {"label": "Restoration Project", "shortcut_name": "Restoration Project", "url": "/app/restoration-project"},
        {"label": "Material Salvage", "shortcut_name": "Material Salvage", "url": "/app/material-salvage"},
        {"label": "Material Exchange", "shortcut_name": "Material Exchange", "url": "/app/material-exchange"},
        {"label": "Material Sale", "shortcut_name": "Material Sale", "url": "/app/material-sale"},
        {"label": "Reward Claim", "shortcut_name": "Reward Claim", "url": "/app/reward-claim"},
    ]
    
    for sc in shortcuts:
        workspace.append("shortcuts", {
            "label": sc["label"],
            "shortcut_name": sc["shortcut_name"],
            "url": sc["url"],
            "col": 3
        })
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} shortcuts!".format(len(shortcuts)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
