import frappe


def citizen_property_report_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Government Officer" in user_roles:
        return True
    
    if "Citizen" in user_roles:
        if doc.owner == user or doc.citizen == user:
            return True
    
    return False


def abandoned_property_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    if "Government Officer" in user_roles:
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
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Inspector" in user_roles:
        if doc.inspector == user or doc.owner == user:
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
    
    if "Property Administrator" in user_roles:
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
    
    if "Property Administrator" in user_roles:
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
    
    if "Property Administrator" in user_roles:
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
    
    if "Property Administrator" in user_roles:
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
    
    if "Property Administrator" in user_roles:
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
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Government Officer" in user_roles:
        return True
    
    if "Citizen" in user_roles:
        if doc.citizen == user:
            return True
    
    return False


def digital_time_capsule_has_permission(doc, ptype, user):
    if frappe.session.user == "Administrator":
        return True
    
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles:
        return True
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Government Officer" in user_roles:
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
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Government Officer" in user_roles:
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
    
    if "Property Administrator" in user_roles:
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
    
    if "Property Administrator" in user_roles:
        return True
    
    if "Restoration Manager" in user_roles:
        return True
    
    return False


def citizen_property_report_permission_query(user):
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles or "Property Administrator" in user_roles or "Government Officer" in user_roles:
        return None
    
    if "Citizen" in user_roles:
        return f"`tabCitizen Property Report`.citizen = '{user}'"
    
    return "1=0"


def abandoned_property_permission_query(user):
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles or "Property Administrator" in user_roles or "Restoration Manager" in user_roles or "Government Officer" in user_roles:
        return None
    
    if "View Only User" in user_roles:
        return None
    
    return "1=0"


def property_inspection_permission_query(user):
    user_roles = frappe.get_roles(user)
    
    if "System Manager" in user_roles or "Property Administrator" in user_roles or "Engineer" in user_roles:
        return None
    
    if "Inspector" in user_roles:
        return f"`tabProperty Inspection`.inspector = '{user}'"
    
    if "View Only User" in user_roles:
        return None
    
    return "1=0"
