import frappe


def get_data():
    return [
        {
            "label": frappe._("Abandoned Property Restoration"),
            "items": [
                {
                    "label": frappe._("Masters"),
                    "items": get_master_items()
                },
                {
                    "label": frappe._("Transactions"),
                    "items": get_transaction_items()
                },
                {
                    "label": frappe._("Reports"),
                    "items": get_report_items()
                }
            ]
        }
    ]


def get_master_items():
    return [
        "Property Category",
        "Property Type",
        "Restoration Category",
        "Material Category",
        "Material Condition",
        "Reward Type",
        "Client",
        "Contractor",
        "Engineer",
        "Field Agent",
        "Department",
        "District",
        "City",
        "State",
        "Country",
        "Ownership Type",
        "Risk Level",
        "Restoration Status",
        "Project Priority",
        "Historical Document Type",
        "Time Capsule Category",
        "Location"
    ]


def get_transaction_items():
    return [
        "Abandoned Property",
        "Property Inspection",
        "Restoration Project",
        "Before After Visualization",
        "Property Images",
        "Property Documents",
        "Material Salvage",
        "Material Exchange",
        "Material Sale",
        "Client Property Report",
        "Reward Claim",
        "Project Assignment",
        "Inspection Report",
        "Restoration Progress",
        "Property Ownership Record",
        "Digital Time Capsule",
        "Historical Record",
        "Maintenance Schedule",
        "Maintenance Visit",
        "Project Cost",
        "Expense Entry",
        "Property Timeline"
    ]


def get_report_items():
    return [
        "Abandoned Property Summary",
        "Restoration Status Report",
        "Material Salvage Report",
        "Material Exchange Report",
        "Citizen Reward Report",
        "Property Inspection Report",
        "Restoration Cost Report",
        "Digital Archive Report",
        "Property Timeline Report",
        "Historical Records Report",
        "Maintenance Report",
        "Project Progress Report",
        "Top Contributors Report",
        "District-wise Restoration Report"
    ]
