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
        {"label": _("Timeline ID"), "fieldname": "name", "fieldtype": "Link", "options": "Property Timeline", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Event Type"), "fieldname": "event_type", "fieldtype": "Data", "width": 120},
        {"label": _("Event Title"), "fieldname": "event_title", "fieldtype": "Data", "width": 200},
        {"label": _("Event Date"), "fieldname": "event_date", "fieldtype": "Datetime", "width": 150},
        {"label": _("Created By"), "fieldname": "created_by", "fieldtype": "Data", "width": 150},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            event_type,
            event_title,
            event_date,
            created_by
        FROM `tabProperty Timeline`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("property"):
            query += " AND property = %(property)s"
        if filters.get("event_type"):
            query += " AND event_type = %(event_type)s"
    
    query += " ORDER BY event_date DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
