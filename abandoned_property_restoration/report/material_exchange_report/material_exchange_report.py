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
        {"label": _("From Project"), "fieldname": "from_project", "fieldtype": "Link", "options": "Restoration Project", "width": 140},
        {"label": _("To Project"), "fieldname": "to_project", "fieldtype": "Link", "options": "Restoration Project", "width": 140},
        {"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Float", "width": 80},
        {"label": _("Exchange Date"), "fieldname": "exchange_date", "fieldtype": "Date", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            material_name,
            from_project,
            to_project,
            quantity,
            exchange_date,
            status
        FROM `tabMaterial Exchange`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("status"):
            query += " AND status = %(status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
