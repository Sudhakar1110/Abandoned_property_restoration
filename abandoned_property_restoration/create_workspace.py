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
    
    # Add number cards - need number_card_name field
    number_cards = [
        {"number_card_name": "Masters", "label": "Masters", "color": "#4CAF50"},
        {"number_card_name": "Transactions", "label": "Transactions", "color": "#2196F3"},
        {"number_card_name": "Reports", "label": "Reports", "color": "#FF9800"},
    ]
    
    for card in number_cards:
        workspace.append("number_cards", {
            "number_card_name": card["number_card_name"],
            "label": card["label"],
            "color": card["color"],
        })
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("Number cards:", len(number_cards))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
