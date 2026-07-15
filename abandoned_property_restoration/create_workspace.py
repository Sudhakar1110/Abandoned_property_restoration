#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.create_workspace.create_abandoned_property_workspace
"""

import frappe
import json

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
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Update content JSON with shortcut blocks using URL format
    content = json.dumps([
        # Masters Section
        {"id": "H1", "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": "S1", "type": "shortcut", "data": {"shortcut_name": "Property Category", "url": "/app/property-category", "col": 3}},
        {"id": "S2", "type": "shortcut", "data": {"shortcut_name": "Property Type", "url": "/app/property-type", "col": 3}},
        {"id": "S3", "type": "shortcut", "data": {"shortcut_name": "Restoration Category", "url": "/app/restoration-category", "col": 3}},
        {"id": "S4", "type": "shortcut", "data": {"shortcut_name": "Material Category", "url": "/app/material-category", "col": 3}},
        {"id": "S5", "type": "shortcut", "data": {"shortcut_name": "Material Condition", "url": "/app/material-condition", "col": 3}},
        {"id": "S6", "type": "shortcut", "data": {"shortcut_name": "Citizen", "url": "/app/citizen", "col": 3}},
        {"id": "S7", "type": "shortcut", "data": {"shortcut_name": "Contractor", "url": "/app/contractor", "col": 3}},
        {"id": "S8", "type": "shortcut", "data": {"shortcut_name": "Engineer", "url": "/app/engineer", "col": 3}},
        {"id": "S9", "type": "shortcut", "data": {"shortcut_name": "Inspector", "url": "/app/inspector", "col": 3}},
        {"id": "S10", "type": "shortcut", "data": {"shortcut_name": "Government Department", "url": "/app/government-department", "col": 3}},
        {"id": "S11", "type": "shortcut", "data": {"shortcut_name": "Reward Type", "url": "/app/reward-type", "col": 3}},
        {"id": "SP1", "type": "spacer", "data": {"col": 12}},
        # Transactions Section
        {"id": "H2", "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": "S12", "type": "shortcut", "data": {"shortcut_name": "Abandoned Property", "url": "/app/abandoned-property", "col": 3}},
        {"id": "S13", "type": "shortcut", "data": {"shortcut_name": "Citizen Property Report", "url": "/app/citizen-property-report", "col": 3}},
        {"id": "S14", "type": "shortcut", "data": {"shortcut_name": "Property Inspection", "url": "/app/property-inspection", "col": 3}},
        {"id": "S15", "type": "shortcut", "data": {"shortcut_name": "Restoration Project", "url": "/app/restoration-project", "col": 3}},
        {"id": "S16", "type": "shortcut", "data": {"shortcut_name": "Material Salvage", "url": "/app/material-salvage", "col": 3}},
        {"id": "S17", "type": "shortcut", "data": {"shortcut_name": "Material Exchange", "url": "/app/material-exchange", "col": 3}},
        {"id": "S18", "type": "shortcut", "data": {"shortcut_name": "Material Sale", "url": "/app/material-sale", "col": 3}},
        {"id": "S19", "type": "shortcut", "data": {"shortcut_name": "Reward Claim", "url": "/app/reward-claim", "col": 3}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("Please hard refresh your browser (Ctrl+Shift+R)")
