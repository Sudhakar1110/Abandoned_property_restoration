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
    roles = ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]
    for role in roles:
        workspace.append("roles", {"role": role})
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Define shortcuts - these will be in content JSON with headers
    content_blocks = []
    
    # Masters Section Header
    content_blocks.append({
        "id": generate_id(),
        "type": "header", 
        "data": {"text": "<span class=\"h4\"><b>Masters</b></span>", "col": 12}
    })
    
    # Masters Shortcuts
    masters = [
        ("Property Category", "Property Category"),
        ("Property Type", "Property Type"),
        ("Restoration Category", "Restoration Category"),
        ("Material Category", "Material Category"),
        ("Material Condition", "Material Condition"),
        ("Citizen", "Citizen"),
        ("Contractor", "Contractor"),
        ("Engineer", "Engineer"),
        ("Inspector", "Inspector"),
        ("Government Department", "Government Department"),
        ("Reward Type", "Reward Type"),
    ]
    
    for label, shortcut_name in masters:
        content_blocks.append({
            "id": generate_id(),
            "type": "shortcut",
            "data": {"shortcut_name": shortcut_name, "col": 3}
        })
    
    # Spacer
    content_blocks.append({"id": generate_id(), "type": "spacer", "data": {"col": 12}})
    
    # Transactions Section Header
    content_blocks.append({
        "id": generate_id(),
        "type": "header", 
        "data": {"text": "<span class=\"h4\"><b>Transactions</b></span>", "col": 12}
    })
    
    # Transactions Shortcuts
    transactions = [
        ("Abandoned Property", "Abandoned Property"),
        ("Citizen Property Report", "Citizen Property Report"),
        ("Property Inspection", "Property Inspection"),
        ("Restoration Project", "Restoration Project"),
        ("Material Salvage", "Material Salvage"),
        ("Material Exchange", "Material Exchange"),
        ("Material Sale", "Material Sale"),
        ("Reward Claim", "Reward Claim"),
    ]
    
    for label, shortcut_name in transactions:
        content_blocks.append({
            "id": generate_id(),
            "type": "shortcut",
            "data": {"shortcut_name": shortcut_name, "col": 3}
        })
    
    # Update content via SQL
    frappe.db.sql("""
        UPDATE `tabWorkspace` 
        SET content = %s 
        WHERE name = %s
    """, (frappe.json.dumps(content_blocks), "Abandoned Property Restoration"))
    frappe.db.commit()
    
    print("SUCCESS: Workspace created!")
    print("- Masters: {0} shortcuts".format(len(masters)))
    print("- Transactions: {0} shortcuts".format(len(transactions)))
    print("Please hard refresh your browser (Ctrl+Shift+R)")
