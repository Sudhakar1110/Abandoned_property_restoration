#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.create_workspace.create_abandoned_property_workspace
"""

import frappe
import json
import os

def create_abandoned_property_workspace():
    """Create the Abandoned Property Restoration workspace."""
    
    # Delete existing workspace if it exists
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        frappe.delete_doc("Workspace", "Abandoned Property Restoration", force=True)
        print("Deleted existing workspace")
    
    # Delete any existing links
    frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = 'Abandoned Property Restoration'")
    
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
    links_data = [
        # Masters
        {"label": "Property Category", "link_type": "DocType", "link_to": "Property Category", "icon": "fa fa-th", "col": 3},
        {"label": "Property Type", "link_type": "DocType", "link_to": "Property Type", "icon": "fa fa-building", "col": 3},
        {"label": "Restoration Category", "link_type": "DocType", "link_to": "Restoration Category", "icon": "fa fa-refresh", "col": 3},
        {"label": "Material Category", "link_type": "DocType", "link_to": "Material Category", "icon": "fa fa-cubes", "col": 3},
        {"label": "Material Condition", "link_type": "DocType", "link_to": "Material Condition", "icon": "fa fa-check-circle", "col": 3},
        {"label": "Citizen", "link_type": "DocType", "link_to": "Citizen", "icon": "fa fa-user", "col": 3},
        {"label": "Contractor", "link_type": "DocType", "link_to": "Contractor", "icon": "fa fa-briefcase", "col": 3},
        {"label": "Engineer", "link_type": "DocType", "link_to": "Engineer", "icon": "fa fa-wrench", "col": 3},
        {"label": "Inspector", "link_type": "DocType", "link_to": "Inspector", "icon": "fa fa-search", "col": 3},
        {"label": "Government Department", "link_type": "DocType", "link_to": "Government Department", "icon": "fa fa-institution", "col": 3},
        {"label": "Reward Type", "link_type": "DocType", "link_to": "Reward Type", "icon": "fa fa-gift", "col": 3},
        # Transactions
        {"label": "Abandoned Property", "link_type": "DocType", "link_to": "Abandoned Property", "icon": "fa fa-home", "col": 3},
        {"label": "Citizen Property Report", "link_type": "DocType", "link_to": "Citizen Property Report", "icon": "fa fa-flag", "col": 3},
        {"label": "Property Inspection", "link_type": "DocType", "link_to": "Property Inspection", "icon": "fa fa-clipboard", "col": 3},
        {"label": "Restoration Project", "link_type": "DocType", "link_to": "Restoration Project", "icon": "fa fa-tasks", "col": 3},
        {"label": "Material Salvage", "link_type": "DocType", "link_to": "Material Salvage", "icon": "fa fa-recycle", "col": 3},
        {"label": "Material Exchange", "link_type": "DocType", "link_to": "Material Exchange", "icon": "fa fa-exchange", "col": 3},
        {"label": "Material Sale", "link_type": "DocType", "link_to": "Material Sale", "icon": "fa fa-shopping-cart", "col": 3},
        {"label": "Reward Claim", "link_type": "DocType", "link_to": "Reward Claim", "icon": "fa fa-money", "col": 3},
    ]
    
    for link in links_data:
        workspace.append("links", link)
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} links!".format(len(links_data)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
