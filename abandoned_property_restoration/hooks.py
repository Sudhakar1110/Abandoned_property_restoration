from . import __version__ as app_version

app_name = "abandoned_property_restoration"
app_title = "Abandoned Property Restoration"
app_publisher = "Abandoned Property Restoration Team"
app_description = "Application for identifying, restoring, preserving, and managing abandoned properties"
app_email = "support@abandonedpropertyrestoration.com"
app_license = "MIT"
app_version = "1.0.0"
required_apps = ["erpnext"]

doc_events = {
    "Citizen Property Report": {
        "on_update": "abandoned_property_restoration.events.citizen_property_report_on_update",
        "after_insert": "abandoned_property_restoration.events.citizen_property_report_after_insert",
    },
    "Property Inspection": {
        "on_update": "abandoned_property_restoration.events.property_inspection_on_update",
        "after_insert": "abandoned_property_restoration.events.property_inspection_after_insert",
    },
    "Restoration Project": {
        "on_update": "abandoned_property_restoration.events.restoration_project_on_update",
        "after_insert": "abandoned_property_restoration.events.restoration_project_after_insert",
    },
    "Material Salvage": {
        "on_update": "abandoned_property_restoration.events.material_salvage_on_update",
        "after_insert": "abandoned_property_restoration.events.material_salvage_after_insert",
    },
    "Material Exchange": {
        "on_update": "abandoned_property_restoration.events.material_exchange_on_update",
        "after_insert": "abandoned_property_restoration.events.material_exchange_after_insert",
    },
    "Material Sale": {
        "on_update": "abandoned_property_restoration.events.material_sale_on_update",
        "after_insert": "abandoned_property_restoration.events.material_sale_after_insert",
    },
    "Reward Claim": {
        "on_update": "abandoned_property_restoration.events.reward_claim_on_update",
        "after_insert": "abandoned_property_restoration.events.reward_claim_after_insert",
    },
    "Historical Record": {
        "on_update": "abandoned_property_restoration.events.historical_record_on_update",
        "after_insert": "abandoned_property_restoration.events.historical_record_after_insert",
    },
    "Maintenance Schedule": {
        "on_update": "abandoned_property_restoration.events.maintenance_schedule_on_update",
        "after_insert": "abandoned_property_restoration.events.maintenance_schedule_after_insert",
    },
    "Abandoned Property": {
        "on_update": "abandoned_property_restoration.events.abandoned_property_on_update",
        "after_insert": "abandoned_property_restoration.events.abandoned_property_after_insert",
    },
}

scheduler_events = {
    "all": [
        "abandoned_property_restoration.tasks.all",
    ],
    "daily": [
        "abandoned_property_restoration.scheduler.maintenance_due_check",
        "abandoned_property_restoration.scheduler.project_delayed_check",
        "abandoned_property_restoration.tasks.daily",
    ],
    "hourly": [
        "abandoned_property_restoration.scheduler.status_check",
        "abandoned_property_restoration.tasks.hourly",
    ],
    "weekly": [
        "abandoned_property_restoration.tasks.weekly",
    ],
    "monthly": [
        "abandoned_property_restoration.tasks.monthly",
    ],
    "yearly": [
        "abandoned_property_restoration.tasks.yearly",
    ],
}

after_install = "abandoned_property_restoration.install.after_install"
after_uninstall = "abandoned_property_restoration.install.after_uninstall"

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "restoration"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "restoration"]]},
    {"dt": "Custom Script", "filters": [["dt", "like", "%"]]},
    {"dt": "Print Format", "filters": [["module", "=", "restoration"]]},
    {"dt": "Report", "filters": [["module", "=", "restoration"]]},
    {"dt": "Workspace", "filters": [["name", "=", "Abandoned Property Restoration"]]},
]

override_whitelisted_methods = {}

has_permission = {
    "Citizen Property Report": "abandoned_property_restoration.permissions.citizen_property_report_has_permission",
    "Abandoned Property": "abandoned_property_restoration.permissions.abandoned_property_has_permission",
    "Property Inspection": "abandoned_property_restoration.permissions.property_inspection_has_permission",
    "Restoration Project": "abandoned_property_restoration.permissions.restoration_project_has_permission",
    "Before After Visualization": "abandoned_property_restoration.permissions.before_after_visualization_has_permission",
    "Material Salvage": "abandoned_property_restoration.permissions.material_salvage_has_permission",
    "Material Exchange": "abandoned_property_restoration.permissions.material_exchange_has_permission",
    "Material Sale": "abandoned_property_restoration.permissions.material_sale_has_permission",
    "Reward Claim": "abandoned_property_restoration.permissions.reward_claim_has_permission",
    "Digital Time Capsule": "abandoned_property_restoration.permissions.digital_time_capsule_has_permission",
    "Historical Record": "abandoned_property_restoration.permissions.historical_record_has_permission",
    "Maintenance Schedule": "abandoned_property_restoration.permissions.maintenance_schedule_has_permission",
    "Project Assignment": "abandoned_property_restoration.permissions.project_assignment_has_permission",
}

permission_query_conditions = {
    "Citizen Property Report": "abandoned_property_restoration.permissions.citizen_property_report_permission_query",
    "Abandoned Property": "abandoned_property_restoration.permissions.abandoned_property_permission_query",
    "Property Inspection": "abandoned_property_restoration.permissions.property_inspection_permission_query",
}

standard_queries = {
    "Employee": "abandoned_property_restoration.utils.get_employee_query",
}
