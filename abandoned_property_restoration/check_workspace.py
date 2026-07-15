#!/usr/bin/env python3
"""
Script to check workspace structure in Frappe v15.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.check_workspace.check_format
"""

import frappe

def check_format():
    """Check workspace structure."""
    
    # Check workspace doctype fields
    meta = frappe.get_meta("Workspace")
    print("=== Workspace Doctype Fields ===")
    for field in meta.fields:
        print(f"{field.fieldname}: {field.fieldtype}")
        
    # Check if blocks child table exists
    print("\n=== Child Tables ===")
    for field in meta.fields:
        if field.fieldtype in ["Table", "Small Text"]:
            print(f"Child table: {field.options}")
            
    # Check ERPNext workspace
    if frappe.db.exists("Workspace", "Selling"):
        ws = frappe.get_doc("Workspace", "Selling")
        print("\n=== ERPNext Selling Workspace ===")
        print("Has blocks:", hasattr(ws, 'blocks'))
        print("Blocks count:", len(ws.blocks) if hasattr(ws, 'blocks') else 0)
        print("Content:", ws.content[:500] if ws.content else "Empty")
        
    # Check our workspace
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        ws = frappe.get_doc("Workspace", "Abandoned Property Restoration")
        print("\n=== Our Workspace ===")
        print("Has blocks:", hasattr(ws, 'blocks'))
        print("Blocks count:", len(ws.blocks) if hasattr(ws, 'blocks') else 0)
        print("Content:", ws.content[:500] if ws.content else "Empty")
