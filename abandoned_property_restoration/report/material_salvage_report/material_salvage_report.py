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
        {"label": _("Material ID"), "fieldname": "name", "fieldtype": "Link", "options": "Material Salvage", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Material Name"), "fieldname": "material_name", "fieldtype": "Data", "width": 150},
        {"label": _("Category"), "fieldname": "material_category", "fieldtype": "Link", "options": "Material Category", "width": 120},
        {"label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Float", "width": 80},
        {"label": _("Condition"), "fieldname": "material_condition", "fieldtype": "Link", "options": "Material Condition", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            material_name,
            material_category,
            quantity,
            material_condition,
            status
        FROM `tabMaterial Salvage`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("material_category"):
            query += " AND material_category = %(material_category)s"
        if filters.get("status"):
            query += " AND status = %(status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
