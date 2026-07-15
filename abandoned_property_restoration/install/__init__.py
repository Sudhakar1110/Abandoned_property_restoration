import frappe


def after_install():
    create_workspace()
    create_custom_fields()
    create_property_doctypes()
    frappe.db.commit()
    frappe.publish_realtime("bench_event", {"message": "Abandoned Property Restoration installed successfully"})


def after_uninstall():
    pass


def create_workspace():
    """Create the Abandoned Property Restoration workspace."""
    if not frappe.db.exists("Workspace", "Abandoned Property Restoration"):
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
        
        # Add content with card blocks
        workspace.content = frappe.json.dumps([
            {
                "id": "masters-header",
                "type": "header",
                "data": {"title": "Masters"}
            },
            {
                "id": "masters-card-1",
                "type": "card",
                "data": {
                    "label": "Property Masters",
                    "icon": "fa fa-building",
                    "items": [
                        {"label": "Property Category", "doc_type": "Property Category", "link": "/app/property-category"},
                        {"label": "Property Type", "doc_type": "Property Type", "link": "/app/property-type"},
                        {"label": "Restoration Category", "doc_type": "Restoration Category", "link": "/app/restoration-category"}
                    ]
                }
            },
            {
                "id": "masters-card-2",
                "type": "card",
                "data": {
                    "label": "Material Masters",
                    "icon": "fa fa-cubes",
                    "items": [
                        {"label": "Material Category", "doc_type": "Material Category", "link": "/app/material-category"},
                        {"label": "Material Condition", "doc_type": "Material Condition", "link": "/app/material-condition"}
                    ]
                }
            },
            {
                "id": "masters-card-3",
                "type": "card",
                "data": {
                    "label": "People",
                    "icon": "fa fa-users",
                    "items": [
                        {"label": "Citizen", "doc_type": "Citizen", "link": "/app/citizen"},
                        {"label": "Contractor", "doc_type": "Contractor", "link": "/app/contractor"},
                        {"label": "Engineer", "doc_type": "Engineer", "link": "/app/engineer"},
                        {"label": "Inspector", "doc_type": "Inspector", "link": "/app/inspector"}
                    ]
                }
            },
            {
                "id": "masters-card-4",
                "type": "card",
                "data": {
                    "label": "Organization",
                    "icon": "fa fa-institution",
                    "items": [
                        {"label": "Government Department", "doc_type": "Government Department", "link": "/app/government-department"},
                        {"label": "Reward Type", "doc_type": "Reward Type", "link": "/app/reward-type"}
                    ]
                }
            },
            {
                "id": "transactions-header",
                "type": "header",
                "data": {"title": "Transactions"}
            },
            {
                "id": "transactions-card-1",
                "type": "card",
                "data": {
                    "label": "Property Management",
                    "icon": "fa fa-home",
                    "items": [
                        {"label": "Abandoned Property", "doc_type": "Abandoned Property", "link": "/app/abandoned-property"},
                        {"label": "Citizen Property Report", "doc_type": "Citizen Property Report", "link": "/app/citizen-property-report"},
                        {"label": "Property Inspection", "doc_type": "Property Inspection", "link": "/app/property-inspection"}
                    ]
                }
            },
            {
                "id": "transactions-card-2",
                "type": "card",
                "data": {
                    "label": "Restoration",
                    "icon": "fa fa-refresh",
                    "items": [
                        {"label": "Restoration Project", "doc_type": "Restoration Project", "link": "/app/restoration-project"},
                        {"label": "Material Salvage", "doc_type": "Material Salvage", "link": "/app/material-salvage"},
                        {"label": "Material Exchange", "doc_type": "Material Exchange", "link": "/app/material-exchange"},
                        {"label": "Material Sale", "doc_type": "Material Sale", "link": "/app/material-sale"}
                    ]
                }
            },
            {
                "id": "transactions-card-3",
                "type": "card",
                "data": {
                    "label": "Rewards",
                    "icon": "fa fa-gift",
                    "items": [
                        {"label": "Reward Claim", "doc_type": "Reward Claim", "link": "/app/reward-claim"}
                    ]
                }
            },
            {
                "id": "reports-header",
                "type": "header",
                "data": {"title": "Reports"}
            },
            {
                "id": "reports-card-1",
                "type": "card",
                "data": {
                    "label": "Property Reports",
                    "icon": "fa fa-file-text",
                    "items": [
                        {"label": "Abandoned Property Summary", "link": "/app/query-report/Abandoned%20Property%20Summary"},
                        {"label": "Restoration Status Report", "link": "/app/query-report/Restoration%20Status%20Report"},
                        {"label": "Property Inspection Report", "link": "/app/query-report/Property%20Inspection%20Report"}
                    ]
                }
            },
            {
                "id": "reports-card-2",
                "type": "card",
                "data": {
                    "label": "Material Reports",
                    "icon": "fa fa-cubes",
                    "items": [
                        {"label": "Material Salvage Report", "link": "/app/query-report/Material%20Salvage%20Report"},
                        {"label": "Material Exchange Report", "link": "/app/query-report/Material%20Exchange%20Report"}
                    ]
                }
            },
            {
                "id": "reports-card-3",
                "type": "card",
                "data": {
                    "label": "Other Reports",
                    "icon": "fa fa-bar-chart",
                    "items": [
                        {"label": "Citizen Reward Report", "link": "/app/query-report/Citizen%20Reward%20Report"},
                        {"label": "Restoration Cost Report", "link": "/app/query-report/Restoration%20Cost%20Report"},
                        {"label": "Project Progress Report", "link": "/app/query-report/Project%20Progress%20Report"}
                    ]
                }
            }
        ])
        
        workspace.insert(ignore_permissions=True)


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
