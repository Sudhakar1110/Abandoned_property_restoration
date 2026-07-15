#!/usr/bin/env python3
"""
Script to check ERPNext workspace format and structure.
Run with: bench --site abp.bizaxl.local execute abandoned_property_restoration.check_workspace.check_format
"""

import frappe

def check_format():
    """Check ERPNext workspace format."""
    
    # Get ERPNext workspace content
    if frappe.db.exists("Workspace", "Selling"):
        ws = frappe.get_doc("Workspace", "Selling")
        print("=== ERPNext Selling Workspace ===")
        print("Content length:", len(ws.content) if ws.content else 0)
        print()
        print("Full Content:")
        print(ws.content if ws.content else "No content")
        print()
        
    # Check our workspace
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        ws = frappe.get_doc("Workspace", "Abandoned Property Restoration")
        print("=== Our Workspace ===")
        print("Content length:", len(ws.content) if ws.content else 0)
        print()
        print("Full Content:")
        print(ws.content if ws.content else "No content")
        
    # Check what doctypes exist
    print("\n=== Checking Doctypes ===")
    doctypes = frappe.get_all("DocType", filters=[["name", "like", "%Property%"]], fields=["name"])
    for d in doctypes:
        print(d.get("name"))
        
    # Check workspace pages table
    print("\n=== Checking Workspace Pages ===")
    pages = frappe.get_all("Workspace Page", fields=["name", "page_name"])
    for p in pages[:20]:
        print(p)
