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
        {"label": _("Client"), "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 200},
        {"label": _("Total Reports"), "fieldname": "total_reports", "fieldtype": "Int", "width": 120},
        {"label": _("Verified Reports"), "fieldname": "verified_reports", "fieldtype": "Int", "width": 130},
        {"label": _("Pending Reports"), "fieldname": "pending_reports", "fieldtype": "Int", "width": 130},
        {"label": _("Rejected Reports"), "fieldname": "rejected_reports", "fieldtype": "Int", "width": 130},
        {"label": _("Total Rewards"), "fieldname": "total_rewards", "fieldtype": "Currency", "width": 120},
    ]


def get_data(filters):
    query = """
        SELECT 
            citizen,
            COUNT(*) as total_reports,
            SUM(CASE WHEN status = 'Verified' THEN 1 ELSE 0 END) as verified_reports,
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_reports,
            SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) as rejected_reports,
            COALESCE(SUM(rc.reward_amount), 0) as total_rewards
        FROM `tabClient Property Report` cpr
        LEFT JOIN `tabReward Claim` rc ON rc.property_report = cpr.name AND rc.claim_status = 'Approved'
        WHERE cpr.docstatus < 2
        GROUP BY client
        ORDER BY total_reports DESC
    """
    
    return frappe.db.sql(query, filters, as_dict=1)
