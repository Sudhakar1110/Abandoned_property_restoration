#!/usr/bin/env python3
"""
Script to create the Abandoned Property Restoration workspace.
Run this after the app is installed.
"""
import frappe


def create_abandoned_property_workspace():
    """Create the Abandoned Property Restoration workspace with proper cards."""
    
    workspace_content = [
        {
            "type": "header",
            "name": "masters",
            "hidden": False
        },
        {
            "type": "card",
            "name": "masters-property",
            "hidden": False,
            "data": {
                "label": "Property Masters",
                "icon": "fa fa-building",
                "items": [
                    {
                        "type": "link",
                        "name": "property-category",
                        "label": "Property Category",
                        "doc_type": "Property Category",
                        "icon": "fa fa-th",
                        "link": "/app/property-category"
                    },
                    {
                        "type": "link",
                        "name": "property-type",
                        "label": "Property Type",
                        "doc_type": "Property Type",
                        "icon": "fa fa-building",
                        "link": "/app/property-type"
                    },
                    {
                        "type": "link",
                        "name": "restoration-category",
                        "label": "Restoration Category",
                        "doc_type": "Restoration Category",
                        "icon": "fa fa-refresh",
                        "link": "/app/restoration-category"
                    }
                ]
            }
        },
        {
            "type": "card",
            "name": "masters-material",
            "hidden": False,
            "data": {
                "label": "Material Masters",
                "icon": "fa fa-cubes",
                "items": [
                    {
                        "type": "link",
                        "name": "material-category",
                        "label": "Material Category",
                        "doc_type": "Material Category",
                        "icon": "fa fa-cubes",
                        "link": "/app/material-category"
                    },
                    {
                        "type": "link",
                        "name": "material-condition",
                        "label": "Material Condition",
                        "doc_type": "Material Condition",
                        "icon": "fa fa-check-circle",
                        "link": "/app/material-condition"
                    }
                ]
            }
        },
        {
            "type": "card",
            "name": "masters-people",
            "hidden": False,
            "data": {
                "label": "People",
                "icon": "fa fa-users",
                "items": [
                    {
                        "type": "link",
                        "name": "citizen",
                        "label": "Citizen",
                        "doc_type": "Citizen",
                        "icon": "fa fa-user",
                        "link": "/app/citizen"
                    },
                    {
                        "type": "link",
                        "name": "contractor",
                        "label": "Contractor",
                        "doc_type": "Contractor",
                        "icon": "fa fa-briefcase",
                        "link": "/app/contractor"
                    },
                    {
                        "type": "link",
                        "name": "engineer",
                        "label": "Engineer",
                        "doc_type": "Engineer",
                        "icon": "fa fa-wrench",
                        "link": "/app/engineer"
                    },
                    {
                        "type": "link",
                        "name": "inspector",
                        "label": "Inspector",
                        "doc_type": "Inspector",
                        "icon": "fa fa-search",
                        "link": "/app/inspector"
                    }
                ]
            }
        },
        {
            "type": "card",
            "name": "masters-organization",
            "hidden": False,
            "data": {
                "label": "Organization",
                "icon": "fa fa-institution",
                "items": [
                    {
                        "type": "link",
                        "name": "government-department",
                        "label": "Government Department",
                        "doc_type": "Government Department",
                        "icon": "fa fa-institution",
                        "link": "/app/government-department"
                    },
                    {
                        "type": "link",
                        "name": "reward-type",
                        "label": "Reward Type",
                        "doc_type": "Reward Type",
                        "icon": "fa fa-gift",
                        "link": "/app/reward-type"
                    }
                ]
            }
        },
        {
            "type": "header",
            "name": "transactions",
            "hidden": False
        },
        {
            "type": "card",
            "name": "transactions-property",
            "hidden": False,
            "data": {
                "label": "Property Management",
                "icon": "fa fa-home",
                "items": [
                    {
                        "type": "link",
                        "name": "abandoned-property",
                        "label": "Abandoned Property",
                        "doc_type": "Abandoned Property",
                        "icon": "fa fa-home",
                        "link": "/app/abandoned-property"
                    },
                    {
                        "type": "link",
                        "name": "citizen-property-report",
                        "label": "Citizen Property Report",
                        "doc_type": "Citizen Property Report",
                        "icon": "fa fa-flag",
                        "link": "/app/citizen-property-report"
                    },
                    {
                        "type": "link",
                        "name": "property-inspection",
                        "label": "Property Inspection",
                        "doc_type": "Property Inspection",
                        "icon": "fa fa-clipboard",
                        "link": "/app/property-inspection"
                    }
                ]
            }
        },
        {
            "type": "card",
            "name": "transactions-restoration",
            "hidden": False,
            "data": {
                "label": "Restoration",
                "icon": "fa fa-refresh",
                "items": [
                    {
                        "type": "link",
                        "name": "restoration-project",
                        "label": "Restoration Project",
                        "doc_type": "Restoration Project",
                        "icon": "fa fa-tasks",
                        "link": "/app/restoration-project"
                    },
                    {
                        "type": "link",
                        "name": "material-salvage",
                        "label": "Material Salvage",
                        "doc_type": "Material Salvage",
                        "icon": "fa fa-recycle",
                        "link": "/app/material-salvage"
                    },
                    {
                        "type": "link",
                        "name": "material-exchange",
                        "label": "Material Exchange",
                        "doc_type": "Material Exchange",
                        "icon": "fa fa-exchange",
                        "link": "/app/material-exchange"
                    },
                    {
                        "type": "link",
                        "name": "material-sale",
                        "label": "Material Sale",
                        "doc_type": "Material Sale",
                        "icon": "fa fa-shopping-cart",
                        "link": "/app/material-sale"
                    }
                ]
            }
        },
        {
            "type": "card",
            "name": "transactions-rewards",
            "hidden": False,
            "data": {
                "label": "Rewards",
                "icon": "fa fa-gift",
                "items": [
                    {
                        "type": "link",
                        "name": "reward-claim",
                        "label": "Reward Claim",
                        "doc_type": "Reward Claim",
                        "icon": "fa fa-money",
                        "link": "/app/reward-claim"
                    }
                ]
            }
        }
    ]
    
    # Delete existing workspace if it exists
    if frappe.db.exists("Workspace", "Abandoned Property Restoration"):
        frappe.delete_doc("Workspace", "Abandoned Property Restoration", force=True)
        print("Deleted existing workspace")
    
    # Create new workspace
    workspace = frappe.new_doc("Workspace")
    workspace.name = "Abandoned Property Restoration"
    workspace.title = "Abandoned Property Restoration"
    workspace.label = "Abandoned Property Restoration"
    workspace.icon = "fa fa-home"
    workspace.module = "restoration"
    workspace.public = 1
    workspace.sequence_id = 1
    workspace.is_standard = 1
    workspace.content = frappe.json.dumps(workspace_content)
    
    # Add roles
    roles = ["System Manager", "Property Administrator", "Restoration Manager", "Government Officer", "View Only User"]
    for role in roles:
        workspace.append("roles", {"role": role})
    
    workspace.insert(ignore_permissions=True)
    frappe.db.commit()
    
    print("Workspace 'Abandoned Property Restoration' created successfully!")
    print(f"Total blocks: {len(workspace_content)}")


if __name__ == "__main__":
    frappe.init(site="abp.bizaxl.local")
    frappe.connect()
    create_abandoned_property_workspace()
