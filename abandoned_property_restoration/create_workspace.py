#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.create_workspace.create_abandoned_property_workspace
"""

import frappe
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
    
    # First create the workspace
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
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Masters links - only DocTypes
    masters_links = [
        {"label": "Property Category", "link_type": "DocType", "link_to": "Property Category", "icon": "fa fa-th"},
        {"label": "Property Type", "link_type": "DocType", "link_to": "Property Type", "icon": "fa fa-building"},
        {"label": "Restoration Category", "link_type": "DocType", "link_to": "Restoration Category", "icon": "fa fa-refresh"},
        {"label": "Material Category", "link_type": "DocType", "link_to": "Material Category", "icon": "fa fa-cubes"},
        {"label": "Material Condition", "link_type": "DocType", "link_to": "Material Condition", "icon": "fa fa-check-circle"},
        {"label": "Citizen", "link_type": "DocType", "link_to": "Citizen", "icon": "fa fa-user"},
        {"label": "Contractor", "link_type": "DocType", "link_to": "Contractor", "icon": "fa fa-briefcase"},
        {"label": "Engineer", "link_type": "DocType", "link_to": "Engineer", "icon": "fa fa-wrench"},
        {"label": "Inspector", "link_type": "DocType", "link_to": "Inspector", "icon": "fa fa-search"},
        {"label": "Government Department", "link_type": "DocType", "link_to": "Government Department", "icon": "fa fa-institution"},
        {"label": "Reward Type", "link_type": "DocType", "link_to": "Reward Type", "icon": "fa fa-gift"},
    ]
    
    transactions_links = [
        {"label": "Abandoned Property", "link_type": "DocType", "link_to": "Abandoned Property", "icon": "fa fa-home"},
        {"label": "Citizen Property Report", "link_type": "DocType", "link_to": "Citizen Property Report", "icon": "fa fa-flag"},
        {"label": "Property Inspection", "link_type": "DocType", "link_to": "Property Inspection", "icon": "fa fa-clipboard"},
        {"label": "Restoration Project", "link_type": "DocType", "link_to": "Restoration Project", "icon": "fa fa-tasks"},
        {"label": "Material Salvage", "link_type": "DocType", "link_to": "Material Salvage", "icon": "fa fa-recycle"},
        {"label": "Material Exchange", "link_type": "DocType", "link_to": "Material Exchange", "icon": "fa fa-exchange"},
        {"label": "Material Sale", "link_type": "DocType", "link_to": "Material Sale", "icon": "fa fa-shopping-cart"},
        {"label": "Reward Claim", "link_type": "DocType", "link_to": "Reward Claim", "icon": "fa fa-money"},
    ]
    
    # Add Masters links
    for link in masters_links:
        ws_link = frappe.new_doc("Workspace Link")
        ws_link.parent = "Abandoned Property Restoration"
        ws_link.parentfield = "links"
        ws_link.parenttype = "Workspace"
        ws_link.label = link["label"]
        ws_link.link_type = link["link_type"]
        ws_link.link_to = link["link_to"]
        ws_link.icon = link["icon"]
        ws_link.insert(ignore_permissions=True)
    
    # Add Transactions links
    for link in transactions_links:
        ws_link = frappe.new_doc("Workspace Link")
        ws_link.parent = "Abandoned Property Restoration"
        ws_link.parentfield = "links"
        ws_link.parenttype = "Workspace"
        ws_link.label = link["label"]
        ws_link.link_type = link["link_type"]
        ws_link.link_to = link["link_to"]
        ws_link.icon = link["icon"]
        ws_link.insert(ignore_permissions=True)
    
    frappe.db.commit()
    
    # Create content JSON with headers for each section
    content_blocks = [
        # Masters Section
        {"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}},
    ]
    for link in masters_links:
        content_blocks.append({"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": link["link_to"], "col": 3}})
    
    content_blocks.append({"id": generate_id(), "type": "spacer", "data": {"col": 12}})
    
    # Transactions Section
    content_blocks.append({"id": generate_id(), "type": "header", "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}})
    for link in transactions_links:
        content_blocks.append({"id": generate_id(), "type": "shortcut", "data": {"shortcut_name": link["link_to"], "col": 3}})
    
    # Update content via SQL
    frappe.db.sql("""
        UPDATE `tabWorkspace` 
        SET content = %s 
        WHERE name = %s
    """, (frappe.json.dumps(content_blocks), "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("- Masters: {0} links".format(len(masters_links)))
    print("- Transactions: {0} links".format(len(transactions_links)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
