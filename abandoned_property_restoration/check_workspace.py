#!/usr/bin/env python3
"""
Script to check workspace structure in Frappe v15.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.check_workspace.check_format
"""

import frappe

def check_format():
    """Check workspace structure."""
    
    # Get ERPNext workspace content
    if frappe.db.exists("Workspace", "Selling"):
        ws = frappe.get_doc("Workspace", "Selling")
        print("=== ERPNext Selling Workspace ===")
        print("Name:", ws.name)
        print("Fields:", [d.fieldname for d in ws.meta.fields])
        print()
        
    # Check our workspace
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        ws = frappe.get_doc("Workspace", "Abandoned Property Restoration")
        print("=== Our Workspace ===")
        print("Name:", ws.name)
        print("Content length:", len(ws.content) if ws.content else 0)
        
    # Check all workspace-related tables
    print("\n=== Checking Workspace Shortcuts ===")
    shortcuts = frappe.get_all("Workspace Shortcut", fields=["name", "shortcut_name", "url"])
    for s in shortcuts[:20]:
        print(s)
        
    # Check what doctypes exist
    print("\n=== All Custom Doctypes ===")
    doctypes = frappe.get_all("DocType", 
        filters=[["module", "=", "restoration"]], 
        fields=["name"])
    for d in doctypes:
        print(d.get("name"))
