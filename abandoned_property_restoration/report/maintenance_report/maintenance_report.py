# Copyright (c) 2024 - Abandoned Property Restoration
# For license information, please see the LICENSE file

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": _("Schedule ID"), "fieldname": "name", "fieldtype": "Link", "options": "Maintenance Schedule", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Maintenance Type"), "fieldname": "maintenance_type", "fieldtype": "Data", "width": 150},
        {"label": _("Scheduled Date"), "fieldname": "scheduled_date", "fieldtype": "Date", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": _("Assigned To"), "fieldname": "assigned_to", "fieldtype": "Data", "width": 150},
        {"label": _("Estimated Cost"), "fieldname": "estimated_cost", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            maintenance_type,
            scheduled_date,
            status,
            assigned_to,
            estimated_cost
        FROM `tabMaintenance Schedule`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("status"):
            query += " AND status = %(status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
