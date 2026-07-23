import frappe


def client_property_report_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Approver" in user_roles:
        return True
    
    if "Client" in user_roles:
        if doc.owner == user or doc.client == user:
            return True
    
    return False


def abandoned_property_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Approver" in user_roles:
        return True
    
    if "View Only User" in user_roles:
        if ptype == "read":
            return True
    
    return False


def property_inspection_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Field Agent" in user_roles:
        if doc.field_agent == user or doc.owner == user:
            return True
    
    if "Engineer" in user_roles:
        return True
    
    if "View Only User" in user_roles:
        if ptype == "read":
            return True
    
    return False


def restoration_project_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Engineer" in user_roles:
        if doc.engineer == user:
            return True
    
    if "Contractor" in user_roles:
        return True
    
    if "View Only User" in user_roles:
        if ptype == "read":
            return True
    
    return False


def before_after_visualization_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Engineer" in user_roles:
        return True
    
    if "Contractor" in user_roles:
        return True
    
    return False


def material_salvage_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Contractor" in user_roles:
        return True
    
    return False


def material_exchange_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Contractor" in user_roles:
        return True
    
    return False


def material_sale_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    return False


def reward_claim_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Approver" in user_roles:
        return True
    
    if "Client" in user_roles:
        if doc.client == user:
            return True
    
    return False


def digital_time_capsule_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Approver" in user_roles:
        return True
    
    if "View Only User" in user_roles:
        if ptype == "read":
            return True
    
    return False


def historical_record_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Approver" in user_roles:
        return True
    
    if "View Only User" in user_roles:
        if ptype == "read":
            return True
    
    return False


def maintenance_schedule_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Engineer" in user_roles:
        return True
    
    if "Contractor" in user_roles:
        return True
    
    return False


def project_assignment_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Manager" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    return False


def client_property_report_permission_query(user):
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles or "Property Manager" in user_roles or "Approver" in user_roles:
        return None
    
    if "Client" in user_roles:
        return f"`tabClient Property Report`.client = '{user}'"
    
    return "1=0"


def abandoned_property_permission_query(user):
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles or "Property Manager" in user_roles or "Restoration Manager" in user_roles or "Approver" in user_roles:
        return None
    
    if "View Only User" in user_roles:
        return None
    
    return "1=0"


def property_inspection_permission_query(user):
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles or "Property Manager" in user_roles or "Engineer" in user_roles:
        return None
    
    if "Field Agent" in user_roles:
        return f"`tabProperty Inspection`.field_agent = '{user}'"
    
    if "View Only User" in user_roles:
        return None
    
    return "1=0"
