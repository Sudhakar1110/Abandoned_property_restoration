#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.create_workspace.create_abandoned_property_workspace
"""

import frappe

def create_abandoned_property_workspace():
    """Create the Abandoned Property Restoration workspace with child tables."""
    
    # Delete existing workspace if it exists
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        frappe.delete_doc("Workspace", "Abandoned Property Restoration", force=True)
        print("Deleted existing workspace")
    
    # Create new workspace with child tables
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
    
    # Add blocks as child table - using the blocks child table
    blocks = [
        # Masters section
        {"type": "header", "name": "Masters", "label": "Masters", "hidden": 0},
        {"type": "shortcut", "name": "Property Category", "label": "Property Category", "url": "/app/property-category", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Property Type", "label": "Property Type", "url": "/app/property-type", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Restoration Category", "label": "Restoration Category", "url": "/app/restoration-category", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Material Category", "label": "Material Category", "url": "/app/material-category", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Material Condition", "label": "Material Condition", "url": "/app/material-condition", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Citizen", "label": "Citizen", "url": "/app/citizen", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Contractor", "label": "Contractor", "url": "/app/contractor", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Engineer", "label": "Engineer", "url": "/app/engineer", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Inspector", "label": "Inspector", "url": "/app/inspector", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Government Department", "label": "Government Department", "url": "/app/government-department", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Reward Type", "label": "Reward Type", "url": "/app/reward-type", "hidden": 0, "col": 3},
        # Transactions section
        {"type": "header", "name": "Transactions", "label": "Transactions", "hidden": 0},
        {"type": "shortcut", "name": "Abandoned Property", "label": "Abandoned Property", "url": "/app/abandoned-property", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Citizen Property Report", "label": "Citizen Property Report", "url": "/app/citizen-property-report", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Property Inspection", "label": "Property Inspection", "url": "/app/property-inspection", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Restoration Project", "label": "Restoration Project", "url": "/app/restoration-project", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Material Salvage", "label": "Material Salvage", "url": "/app/material-salvage", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Material Exchange", "label": "Material Exchange", "url": "/app/material-exchange", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Material Sale", "label": "Material Sale", "url": "/app/material-sale", "hidden": 0, "col": 3},
        {"type": "shortcut", "name": "Reward Claim", "label": "Reward Claim", "url": "/app/reward-claim", "hidden": 0, "col": 3},
    ]
    
    # Try to add blocks using the workspace's child table
    for block in blocks:
        workspace.append("blocks", block)
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} blocks!".format(len(blocks)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
