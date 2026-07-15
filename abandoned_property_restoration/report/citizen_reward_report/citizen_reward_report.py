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
        {"label": _("Claim ID"), "fieldname": "name", "fieldtype": "Link", "options": "Reward Claim", "width": 150},
        {"label": _("Citizen"), "fieldname": "citizen", "fieldtype": "Link", "options": "Citizen", "width": 150},
        {"label": _("Property Report"), "fieldname": "property_report", "fieldtype": "Link", "options": "Citizen Property Report", "width": 150},
        {"label": _("Reward Type"), "fieldname": "reward_type", "fieldtype": "Link", "options": "Reward Type", "width": 120},
        {"label": _("Reward Amount"), "fieldname": "reward_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Claim Status"), "fieldname": "claim_status", "fieldtype": "Data", "width": 120},
        {"label": _("Claim Date"), "fieldname": "claim_date", "fieldtype": "Date", "width": 100},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            citizen,
            property_report,
            reward_type,
            reward_amount,
            claim_status,
            claim_date
        FROM `tabReward Claim`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("claim_status"):
            query += " AND claim_status = %(claim_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
