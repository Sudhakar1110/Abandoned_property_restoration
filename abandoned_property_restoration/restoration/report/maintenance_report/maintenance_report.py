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
        {"label": _("Schedule Type"), "fieldname": "schedule_type", "fieldtype": "Data", "width": 150},
        {"label": _("Schedule Date"), "fieldname": "schedule_date", "fieldtype": "Date", "width": 120},
        {"label": _("Status"), "fieldname": "schedule_status", "fieldtype": "Data", "width": 120},
        {"label": _("Contractor"), "fieldname": "contractor", "fieldtype": "Link", "options": "Contractor", "width": 150},
        {"label": _("Estimated Cost"), "fieldname": "estimated_cost", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            schedule_type,
            schedule_date,
            schedule_status,
            contractor,
            estimated_cost
        FROM `tabMaintenance Schedule`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("schedule_status"):
            query += " AND schedule_status = %(schedule_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
