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
        {"label": _("Cost ID"), "fieldname": "name", "fieldtype": "Link", "options": "Project Cost", "width": 150},
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Restoration Project", "width": 150},
        {"label": _("Cost Type"), "fieldname": "cost_type", "fieldtype": "Data", "width": 120},
        {"label": _("Amount"), "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Cost Date"), "fieldname": "cost_date", "fieldtype": "Date", "width": 100},
        {"label": _("Vendor"), "fieldname": "vendor", "fieldtype": "Data", "width": 150},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            project,
            cost_type,
            amount,
            cost_date,
            vendor,
            status
        FROM `tabProject Cost`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("project"):
            query += " AND project = %(project)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
