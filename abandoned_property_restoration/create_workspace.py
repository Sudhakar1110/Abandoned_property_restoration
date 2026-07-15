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
    
    # Add links to the links child table
    links = [
        {"label": "Property Category", "link_type": "DocType", "link_to": "Property Category"},
        {"label": "Property Type", "link_type": "DocType", "link_to": "Property Type"},
        {"label": "Restoration Category", "link_type": "DocType", "link_to": "Restoration Category"},
        {"label": "Material Category", "link_type": "DocType", "link_to": "Material Category"},
        {"label": "Material Condition", "link_type": "DocType", "link_to": "Material Condition"},
        {"label": "Citizen", "link_type": "DocType", "link_to": "Citizen"},
        {"label": "Contractor", "link_type": "DocType", "link_to": "Contractor"},
        {"label": "Engineer", "link_type": "DocType", "link_to": "Engineer"},
        {"label": "Inspector", "link_type": "DocType", "link_to": "Inspector"},
        {"label": "Government Department", "link_type": "DocType", "link_to": "Government Department"},
        {"label": "Reward Type", "link_type": "DocType", "link_to": "Reward Type"},
        {"label": "Abandoned Property", "link_type": "DocType", "link_to": "Abandoned Property"},
        {"label": "Citizen Property Report", "link_type": "DocType", "link_to": "Citizen Property Report"},
        {"label": "Property Inspection", "link_type": "DocType", "link_to": "Property Inspection"},
        {"label": "Restoration Project", "link_type": "DocType", "link_to": "Restoration Project"},
        {"label": "Material Salvage", "link_type": "DocType", "link_to": "Material Salvage"},
        {"label": "Material Exchange", "link_type": "DocType", "link_to": "Material Exchange"},
        {"label": "Material Sale", "link_type": "DocType", "link_to": "Material Sale"},
        {"label": "Reward Claim", "link_type": "DocType", "link_to": "Reward Claim"},
    ]
    
    for link in links:
        workspace.append("links", {
            "label": link["label"],
            "link_type": link["link_type"],
            "link_to": link["link_to"],
            "col": 3
        })
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} links!".format(len(links)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
