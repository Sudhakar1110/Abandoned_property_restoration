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
    
    # Update content using SQL - ERPNext format with headers for Masters, Transactions, Reports
    content = json.dumps([
        {"id": "H1", "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": "S1", "type": "shortcut", "data": {"shortcut_name": "Property Category", "col": 3}},
        {"id": "S2", "type": "shortcut", "data": {"shortcut_name": "Property Type", "col": 3}},
        {"id": "S3", "type": "shortcut", "data": {"shortcut_name": "Restoration Category", "col": 3}},
        {"id": "S4", "type": "shortcut", "data": {"shortcut_name": "Material Category", "col": 3}},
        {"id": "S5", "type": "shortcut", "data": {"shortcut_name": "Material Condition", "col": 3}},
        {"id": "S6", "type": "shortcut", "data": {"shortcut_name": "Citizen", "col": 3}},
        {"id": "S7", "type": "shortcut", "data": {"shortcut_name": "Contractor", "col": 3}},
        {"id": "S8", "type": "shortcut", "data": {"shortcut_name": "Engineer", "col": 3}},
        {"id": "S9", "type": "shortcut", "data": {"shortcut_name": "Inspector", "col": 3}},
        {"id": "S10", "type": "shortcut", "data": {"shortcut_name": "Government Department", "col": 3}},
        {"id": "S11", "type": "shortcut", "data": {"shortcut_name": "Reward Type", "col": 3}},
        {"id": "SP1", "type": "spacer", "data": {"col": 12}},
        {"id": "H2", "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": "S12", "type": "shortcut", "data": {"shortcut_name": "Abandoned Property", "col": 3}},
        {"id": "S13", "type": "shortcut", "data": {"shortcut_name": "Citizen Property Report", "col": 3}},
        {"id": "S14", "type": "shortcut", "data": {"shortcut_name": "Property Inspection", "col": 3}},
        {"id": "S15", "type": "shortcut", "data": {"shortcut_name": "Restoration Project", "col": 3}},
        {"id": "S16", "type": "shortcut", "data": {"shortcut_name": "Material Salvage", "col": 3}},
        {"id": "S17", "type": "shortcut", "data": {"shortcut_name": "Material Exchange", "col": 3}},
        {"id": "S18", "type": "shortcut", "data": {"shortcut_name": "Material Sale", "col": 3}},
        {"id": "S19", "type": "shortcut", "data": {"shortcut_name": "Reward Claim", "col": 3}},
        {"id": "SP2", "type": "spacer", "data": {"col": 12}},
        {"id": "H3", "type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with Masters, Transactions, Reports sections!")
    print("Please hard refresh your browser (Ctrl+Shift+R)")
