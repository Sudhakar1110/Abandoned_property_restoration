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
    
    # Add links to the links child table
    links = [
        {"name": "Property Category", "doctype": "Property Category"},
        {"name": "Property Type", "doctype": "Property Type"},
        {"name": "Restoration Category", "doctype": "Restoration Category"},
        {"name": "Material Category", "doctype": "Material Category"},
        {"name": "Material Condition", "doctype": "Material Condition"},
        {"name": "Citizen", "doctype": "Citizen"},
        {"name": "Contractor", "doctype": "Contractor"},
        {"name": "Engineer", "doctype": "Engineer"},
        {"name": "Inspector", "doctype": "Inspector"},
        {"name": "Government Department", "doctype": "Government Department"},
        {"name": "Reward Type", "doctype": "Reward Type"},
        {"name": "Abandoned Property", "doctype": "Abandoned Property"},
        {"name": "Citizen Property Report", "doctype": "Citizen Property Report"},
        {"name": "Property Inspection", "doctype": "Property Inspection"},
        {"name": "Restoration Project", "doctype": "Restoration Project"},
        {"name": "Material Salvage", "doctype": "Material Salvage"},
        {"name": "Material Exchange", "doctype": "Material Exchange"},
        {"name": "Material Sale", "doctype": "Material Sale"},
        {"name": "Reward Claim", "doctype": "Reward Claim"},
    ]
    
    for link in links:
        workspace.append("links", {
            "label": link["name"],
            "link_type": "DocType",
            "link_to": link["doctype"],
            "col": 3
        })
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Create content JSON with links
    content = json.dumps([
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Property Category", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Property Type", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Restoration Category", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Material Category", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Material Condition", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Citizen", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Contractor", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Engineer", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Inspector", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Government Department", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Reward Type", "col": 3}},
        {"id": generate_id(), "type": "spacer", "data": {"col": 12}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Abandoned Property", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Citizen Property Report", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Property Inspection", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Restoration Project", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Material Salvage", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Material Exchange", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Material Sale", "col": 3}},
        {"id": generate_id(), "type": "link", "data": {"link_to": "Reward Claim", "col": 3}},
        {"id": generate_id(), "type": "spacer", "data": {"col": 12}},
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
    ])
    
    frappe.db.sql("UPDATE `tabWorkspace` SET content = %s WHERE name = %s", (content, "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created with {0} links!".format(len(links)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
