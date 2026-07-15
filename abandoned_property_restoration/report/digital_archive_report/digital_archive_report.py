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
        {"label": _("Archive ID"), "fieldname": "name", "fieldtype": "Link", "options": "Digital Time Capsule", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Title"), "fieldname": "title", "fieldtype": "Data", "width": 200},
        {"label": _("Category"), "fieldname": "category", "fieldtype": "Link", "options": "Time Capsule Category", "width": 150},
        {"label": _("Archive Date"), "fieldname": "archive_date", "fieldtype": "Date", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            title,
            category,
            archive_date,
            status
        FROM `tabDigital Time Capsule`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("category"):
            query += " AND category = %(category)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
