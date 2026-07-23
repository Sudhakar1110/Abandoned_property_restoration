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
        {"label": _("Property ID"), "fieldname": "name", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Property Name"), "fieldname": "property_name", "fieldtype": "Data", "width": 150},
        {"label": _("Address"), "fieldname": "address", "fieldtype": "Data", "width": 200},
        {"label": _("Property Status"), "fieldname": "property_status", "fieldtype": "Data", "width": 120},
        {"label": _("Risk Level"), "fieldname": "risk_level", "fieldtype": "Data", "width": 100},
        {"label": _("Property Type"), "fieldname": "property_type", "fieldtype": "Link", "options": "Property Type", "width": 120},
        {"label": _("Owner Name"), "fieldname": "owner_name", "fieldtype": "Data", "width": 150},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property_name,
            address,
            property_status,
            risk_level,
            property_type,
            owner_name
        FROM `tabAbandoned Property`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("property_status"):
            query += " AND property_status = %(property_status)s"
        if filters.get("risk_level"):
            query += " AND risk_level = %(risk_level)s"
        if filters.get("property_type"):
            query += " AND property_type = %(property_type)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
