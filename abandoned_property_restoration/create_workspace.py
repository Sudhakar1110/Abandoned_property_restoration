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
    
    # Create workspace with content set directly
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
    
    # Create content JSON - using ERPNext format
    content = [
        {"id": "A1B2C3D4E5", "type": "card", "data": {"card_name": "Masters", "col": 4}},
        {"id": "F6G7H8I9J0", "type": "card", "data": {"card_name": "Transactions", "col": 4}},
        {"id": "K1L2M3N4O5", "type": "card", "data": {"card_name": "Reports", "col": 4}},
    ]
    
    # Set content as JSON string
    workspace.content = json.dumps(content)
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("Content:", workspace.content)
    print("Please hard refresh your browser (Ctrl+Shift+R)")
