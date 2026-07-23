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
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 150},
        {"label": _("Client Report"), "fieldname": "report_name", "fieldtype": "Link", "options": "Client Property Report", "width": 150},
        {"label": _("Reward Type"), "fieldname": "reward_type", "fieldtype": "Link", "options": "Reward Type", "width": 120},
        {"label": _("Reward Amount"), "fieldname": "reward_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Claim Status"), "fieldname": "claim_status", "fieldtype": "Data", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT 
            name,
            citizen,
            report_name,
            reward_type,
            reward_amount,
            claim_status
        FROM `tabReward Claim`
        WHERE docstatus < 2
    """
    
    if filters:
        if filters.get("claim_status"):
            query += " AND claim_status = %(claim_status)s"
    
    query += " ORDER BY modified DESC"
    
    return frappe.db.sql(query, filters, as_dict=1)
