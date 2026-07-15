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
    
    # Update content with card blocks that contain links
    content = json.dumps([
        {"id": "C1", "type": "card", "data": {"card_name": "Masters", "col": 4}},
        {"id": "C2", "type": "card", "data": {"card_name": "Transactions", "col": 4}},
        {"id": "C3", "type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    # Add links to child table (these will appear in the card)
    links = [
        # Masters - using internal_label to group
        {"label": "Property Category", "link_type": "DocType", "link_to": "Property Category", "internal": 1},
        {"label": "Property Type", "link_type": "DocType", "link_to": "Property Type", "internal": 1},
        {"label": "Restoration Category", "link_type": "DocType", "link_to": "Restoration Category", "internal": 1},
        {"label": "Material Category", "link_type": "DocType", "link_to": "Material Category", "internal": 1},
        {"label": "Material Condition", "link_type": "DocType", "link_to": "Material Condition", "internal": 1},
        {"label": "Citizen", "link_type": "DocType", "link_to": "Citizen", "internal": 1},
        {"label": "Contractor", "link_type": "DocType", "link_to": "Contractor", "internal": 1},
        {"label": "Engineer", "link_type": "DocType", "link_to": "Engineer", "internal": 1},
        {"label": "Inspector", "link_type": "DocType", "link_to": "Inspector", "internal": 1},
        {"label": "Government Department", "link_type": "DocType", "link_to": "Government Department", "internal": 1},
        {"label": "Reward Type", "link_type": "DocType", "link_to": "Reward Type", "internal": 1},
        # Transactions
        {"label": "Abandoned Property", "link_type": "DocType", "link_to": "Abandoned Property", "internal": 1},
        {"label": "Citizen Property Report", "link_type": "DocType", "link_to": "Citizen Property Report", "internal": 1},
        {"label": "Property Inspection", "link_type": "DocType", "link_to": "Property Inspection", "internal": 1},
        {"label": "Restoration Project", "link_type": "DocType", "link_to": "Restoration Project", "internal": 1},
        {"label": "Material Salvage", "link_type": "DocType", "link_to": "Material Salvage", "internal": 1},
        {"label": "Material Exchange", "link_type": "DocType", "link_to": "Material Exchange", "internal": 1},
        {"label": "Material Sale", "link_type": "DocType", "link_to": "Material Sale", "internal": 1},
        {"label": "Reward Claim", "link_type": "DocType", "link_to": "Reward Claim", "internal": 1},
    ]
    
    for link in links:
        ws_link = frappe.new_doc("Workspace Link")
        ws_link.parent = "Abandoned Property Restoration"
        ws_link.parentfield = "links"
        ws_link.parenttype = "Workspace"
        ws_link.label = link["label"]
        ws_link.link_type = link["link_type"]
        ws_link.link_to = link["link_to"]
        ws_link.internal = link.get("internal", 0)
        ws_link.insert(ignore_permissions=True)
    
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with cards and {0} links!".format(len(links)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
