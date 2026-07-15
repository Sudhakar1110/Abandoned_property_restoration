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
        {"label": _("District"), "fieldname": "district", "fieldtype": "Link", "options": "District", "width": 150},
        {"label": _("City"), "fieldname": "city", "fieldtype": "Link", "options": "City", "width": 150},
        {"label": _("Total Properties"), "fieldname": "total_properties", "fieldtype": "Int", "width": 130},
        {"label": _("Reported"), "fieldname": "reported", "fieldtype": "Int", "width": 100},
        {"label": _("Under Inspection"), "fieldname": "under_inspection", "fieldtype": "Int", "width": 130},
        {"label": _("In Restoration"), "fieldname": "in_restoration", "fieldtype": "Int", "width": 120},
        {"label": _("Restored"), "fieldname": "restored", "fieldtype": "Int", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            COALESCE(ap.district, 'Unknown') as district,
            COALESCE(ap.city, 'Unknown') as city,
            COUNT(*) as total_properties,
            SUM(CASE WHEN ap.status = 'Reported' THEN 1 ELSE 0 END) as reported,
            SUM(CASE WHEN ap.status = 'Under Inspection' THEN 1 ELSE 0 END) as under_inspection,
            SUM(CASE WHEN ap.status = 'In Restoration' THEN 1 ELSE 0 END) as in_restoration,
            SUM(CASE WHEN ap.status = 'Restored' THEN 1 ELSE 0 END) as restored
        FROM `tabAbandoned Property` ap
        WHERE ap.docstatus < 2
        GROUP BY ap.district, ap.city
        ORDER BY total_properties DESC
    """
    
    return frappe.db.sql(query, filters, as_dict=1)
