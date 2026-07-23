import frappe
import importlib
import sys

def check_report(report_name):
    print(f"\n=== Checking report: {report_name} ===")
    try:
        report = frappe.get_doc("Report", report_name)
        print(f"  Report found: {report.name}")
        print(f"  Report type: {report.report_type}")
        print(f"  Module: {report.module}")
        print(f"  Ref DocType: {report.ref_doctype}")
        print(f"  is_standard: {report.is_standard}")
        
        # Check if there's a module def for this module
        module_def = frappe.db.exists("Module Def", report.module)
        print(f"  Module Def exists: {module_def}")
        if module_def:
            md = frappe.get_doc("Module Def", report.module)
            print(f"  App Name: {md.app_name}")
        
        # Try to import the report module
        module_path = f"abandoned_property_restoration.{frappe.scrub(report.module)}.report.{frappe.scrub(report.name)}.{frappe.scrub(report.name)}"
        print(f"  Expected module path: {module_path}")
        
        try:
            mod = importlib.import_module(module_path)
            print(f"  Module imported successfully!")
            if hasattr(mod, 'execute'):
                print(f"  execute() function found!")
            else:
                print(f"  WARNING: No execute() function found!")
        except ImportError as e:
            print(f"  ERROR: Could not import module: {e}")
            
    except frappe.DoesNotExistError:
        print(f"  Report '{report_name}' not found in database!")
    except Exception as e:
        print(f"  ERROR: {e}")

# Check all reports
reports = [
    "Abandoned Property Summary",
    "Citizen Reward Report", 
    "Digital Archive Report",
    "District Wise Restoration Report",
    "Historical Records Report",
    "Maintenance Report",
    "Material Exchange Report",
    "Material Salvage Report",
    "Project Progress Report",
    "Property Inspection Report",
    "Property Timeline Report",
    "Restoration Cost Report",
    "Restoration Status Report",
    "Top Contributors Report"
]

for report in reports:
    check_report(report)

print("\n=== Done ===")
