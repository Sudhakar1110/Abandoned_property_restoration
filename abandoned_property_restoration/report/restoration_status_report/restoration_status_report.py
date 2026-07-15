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
        {"label": _("Project ID"), "fieldname": "name", "fieldtype": "Link", "options": "Restoration Project", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Project Status"), "fieldname": "project_status", "fieldtype": "Data", "width": 120},
        {"label": _("Start Date"), "fieldname": "start_date", "fieldtype": "Date", "width": 100},
        {"label": _("End Date"), "fieldname": "end_date", "fieldtype": "Date", "width": 100},
        {"label": _("Progress"), "fieldname": "progress", "fieldtype": "Percent", "width": 80},
        {"label": _("Budget"), "fieldname": "budget", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            project_status,
            start_date,
            end_date,
            progress,
            budget
        FROM `tabRestoration Project`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("project_status"):
            query += " AND project_status = %(project_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
