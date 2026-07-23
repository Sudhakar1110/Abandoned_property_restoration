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
        {"label": _("Exchange ID"), "fieldname": "name", "fieldtype": "Link", "options": "Material Exchange", "width": 150},
        {"label": _("Material"), "fieldname": "material_name", "fieldtype": "Data", "width": 150},
        {"label": _("Source Project"), "fieldname": "source_project", "fieldtype": "Link", "options": "Restoration Project", "width": 140},
        {"label": _("Destination Project"), "fieldname": "destination_project", "fieldtype": "Link", "options": "Restoration Project", "width": 140},
        {"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Float", "width": 80},
        {"label": _("Exchange Date"), "fieldname": "exchange_date", "fieldtype": "Date", "width": 100},
        {"label": _("Exchange Status"), "fieldname": "exchange_status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            material_name,
            source_project,
            destination_project,
            quantity,
            exchange_date,
            exchange_status
        FROM `tabMaterial Exchange`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("exchange_status"):
            query += " AND exchange_status = %(exchange_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
