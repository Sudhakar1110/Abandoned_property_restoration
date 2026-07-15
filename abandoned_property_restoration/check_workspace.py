#!/usr/bin/env python3
"""
Script to check ERPNext workspace format.
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
        
    # Check workspace charts/cards
    print("=== Checking Workspace Charts ===")
    charts = frappe.get_all("Workspace Chart", fields=["name", "item", "label", "doctype"])
    for c in charts[:10]:
        print(c)
