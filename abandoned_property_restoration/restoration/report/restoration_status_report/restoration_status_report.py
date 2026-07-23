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
        {"label": _("Expected End Date"), "fieldname": "expected_end_date", "fieldtype": "Date", "width": 100},
        {"label": _("Progress"), "fieldname": "progress_percentage", "fieldtype": "Percent", "width": 80},
        {"label": _("Estimated Cost"), "fieldname": "estimated_cost", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            project_status,
            start_date,
            expected_end_date,
            progress_percentage,
            estimated_cost
        FROM `tabRestoration Project`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("project_status"):
            query += " AND project_status = %(project_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
