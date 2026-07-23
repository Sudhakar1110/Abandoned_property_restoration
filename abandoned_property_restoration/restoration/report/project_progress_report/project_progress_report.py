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
        {"label": _("Progress ID"), "fieldname": "name", "fieldtype": "Link", "options": "Restoration Progress", "width": 150},
        {"label": _("Project"), "fieldname": "restoration_project", "fieldtype": "Link", "options": "Restoration Project", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Update Date"), "fieldname": "update_date", "fieldtype": "Date", "width": 120},
        {"label": _("Progress Percentage"), "fieldname": "progress_percentage", "fieldtype": "Percent", "width": 130},
        {"label": _("Work Completed"), "fieldname": "work_completed", "fieldtype": "Data", "width": 250},
        {"label": _("Current Phase"), "fieldname": "current_phase", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            restoration_project,
            property,
            update_date,
            progress_percentage,
            work_completed,
            current_phase
        FROM `tabRestoration Progress`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("restoration_project"):
            query += " AND restoration_project = %(restoration_project)s"
    
    query += " ORDER BY update_date DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
