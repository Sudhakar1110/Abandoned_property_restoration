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
        {"label": _("Inspection ID"), "fieldname": "name", "fieldtype": "Link", "options": "Property Inspection", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Inspector"), "fieldname": "inspector", "fieldtype": "Link", "options": "Inspector", "width": 140},
        {"label": _("Inspection Date"), "fieldname": "inspection_date", "fieldtype": "Date", "width": 120},
        {"label": _("Condition"), "fieldname": "overall_condition", "fieldtype": "Data", "width": 120},
        {"label": _("Risk Level"), "fieldname": "risk_level", "fieldtype": "Data", "width": 100},
        {"label": _("Status"), "fieldname": "inspection_status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            inspector,
            inspection_date,
            overall_condition,
            risk_level,
            inspection_status
        FROM `tabProperty Inspection`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("inspection_status"):
            query += " AND inspection_status = %(inspection_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
