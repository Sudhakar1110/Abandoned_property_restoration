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
    
    # Create content JSON with links (not shortcuts) - ERPNext v15 format
    content = json.dumps([
        # Masters Section
        {"id": "H1", "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": "L1", "type": "link", "data": {"link_to": "Property Category", "col": 3}},
        {"id": "L2", "type": "link", "data": {"link_to": "Property Type", "col": 3}},
        {"id": "L3", "type": "link", "data": {"link_to": "Restoration Category", "col": 3}},
        {"id": "L4", "type": "link", "data": {"link_to": "Material Category", "col": 3}},
        {"id": "L5", "type": "link", "data": {"link_to": "Material Condition", "col": 3}},
        {"id": "L6", "type": "link", "data": {"link_to": "Citizen", "col": 3}},
        {"id": "L7", "type": "link", "data": {"link_to": "Contractor", "col": 3}},
        {"id": "L8", "type": "link", "data": {"link_to": "Engineer", "col": 3}},
        {"id": "L9", "type": "link", "data": {"link_to": "Inspector", "col": 3}},
        {"id": "L10", "type": "link", "data": {"link_to": "Government Department", "col": 3}},
        {"id": "L11", "type": "link", "data": {"link_to": "Reward Type", "col": 3}},
        {"id": "SP1", "type": "spacer", "data": {"col": 12}},
        # Transactions Section
        {"id": "H2", "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": "L12", "type": "link", "data": {"link_to": "Abandoned Property", "col": 3}},
        {"id": "L13", "type": "link", "data": {"link_to": "Citizen Property Report", "col": 3}},
        {"id": "L14", "type": "link", "data": {"link_to": "Property Inspection", "col": 3}},
        {"id": "L15", "type": "link", "data": {"link_to": "Restoration Project", "col": 3}},
        {"id": "L16", "type": "link", "data": {"link_to": "Material Salvage", "col": 3}},
        {"id": "L17", "type": "link", "data": {"link_to": "Material Exchange", "col": 3}},
        {"id": "L18", "type": "link", "data": {"link_to": "Material Sale", "col": 3}},
        {"id": "L19", "type": "link", "data": {"link_to": "Reward Claim", "col": 3}},
        {"id": "SP2", "type": "spacer", "data": {"col": 12}},
        # Reports Section
        {"id": "H3", "type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("Please hard refresh your browser (Ctrl+Shift+R)")
