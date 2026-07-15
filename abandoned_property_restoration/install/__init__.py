import frappe


def after_install():
    create_custom_fields()
    create_property_doctypes()
    frappe.db.commit()
    frappe.publish_realtime("bench_event", {"message": "Abandoned Property Restoration installed successfully"})


def after_uninstall():
    pass


def create_custom_fields():
    pass


def create_property_doctypes():
    pass
