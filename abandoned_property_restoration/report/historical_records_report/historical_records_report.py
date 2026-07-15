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
        {"label": _("Record ID"), "fieldname": "name", "fieldtype": "Link", "options": "Historical Record", "width": 150},
        {"label": _("Property"), "fieldname": "property", "fieldtype": "Link", "options": "Abandoned Property", "width": 150},
        {"label": _("Document Type"), "fieldname": "document_type", "fieldtype": "Link", "options": "Historical Document Type", "width": 150},
        {"label": _("Title"), "fieldname": "title", "fieldtype": "Data", "width": 200},
        {"label": _("Record Date"), "fieldname": "record_date", "fieldtype": "Date", "width": 120},
        {"label": _("Source"), "fieldname": "source", "fieldtype": "Data", "width": 150},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            property,
            document_type,
            title,
            record_date,
            source
        FROM `tabHistorical Record`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("document_type"):
            query += " AND document_type = %(document_type)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
