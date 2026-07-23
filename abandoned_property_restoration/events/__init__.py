import frappe


def client_property_report_on_update(doc, method):
    if doc.has_value_changed("status"):
        if doc.status == "Verified":
            send_notification(
                doc,
                "Property Verification Completed",
                "Property Manager",
                f"Property {doc.property_name} has been verified"
            )
        elif doc.status == "Inspection Scheduled":
            send_notification(
                doc,
                "Inspection Scheduled",
                "Field Agent",
                f"Inspection scheduled for {doc.property_name}"
            )


def client_property_report_after_insert(doc, method):
    send_notification(
        doc,
        "New Property Reported",
        "Property Manager",
        f"New property {doc.property_name} reported by {doc.client_name}"
    )


def property_inspection_on_update(doc, method):
    if doc.has_value_changed("inspection_status"):
        if doc.inspection_status == "Completed":
            send_notification(
                doc,
                "Inspection Completed",
                "Property Manager",
                f"Inspection completed for {doc.property}"
            )
        elif doc.inspection_status == "In Progress":
            send_notification(
                doc,
                "Inspection Started",
                "Property Manager",
                f"Inspection started for {doc.property}"
            )


def property_inspection_after_insert(doc, method):
    send_notification(
        doc,
        "Inspection Assigned",
        "Field Agent",
        f"New inspection assigned for {doc.property}"
    )


def restoration_project_on_update(doc, method):
    if doc.has_value_changed("project_status"):
        if doc.project_status == "In Progress":
            send_notification(
                doc,
                "Restoration Started",
                "Property Manager",
                f"Restoration project {doc.name} has started"
            )
        elif doc.project_status == "Completed":
            send_notification(
                doc,
                "Restoration Completed",
                "Property Manager",
                f"Restoration project {doc.name} has been completed"
            )
            update_abandoned_property_status(doc.property, "Restored")


def restoration_project_after_insert(doc, method):
    send_notification(
        doc,
        "Restoration Started",                "Property Manager",
                f"New restoration project {doc.name} created"
    )


def material_salvage_on_update(doc, method):
    if doc.has_value_changed("status"):
        if doc.status == "Available":
            send_notification(
                doc,
                "Material Added",
                "Restoration Manager",
                f"New material {doc.material_name} added to inventory"
            )


def material_salvage_after_insert(doc, method):
    pass


def material_exchange_on_update(doc, method):
    if doc.has_value_changed("exchange_status"):
        if doc.exchange_status == "Completed":
            send_notification(
                doc,
                "Material Exchanged",
                "Restoration Manager",
                f"Material exchange {doc.name} completed"
            )


def material_exchange_after_insert(doc, method):
    pass


def material_sale_on_update(doc, method):
    if doc.has_value_changed("sale_status"):
        if doc.sale_status == "Completed":
            send_notification(
                doc,
                "Material Sold",
                "Property Manager",
                f"Material sale {doc.name} completed"
            )


def material_sale_after_insert(doc, method):
    pass


def reward_claim_on_update(doc, method):
    if doc.has_value_changed("claim_status"):
        if doc.claim_status == "Approved":
            send_notification(
                doc,
                "Reward Approved",
                "Client",
                f"Your reward claim {doc.name} has been approved"
            )
        elif doc.claim_status == "Paid":
            send_notification(
                doc,
                "Reward Paid",
                "Client",
                f"Your reward for {doc.report_name} has been paid"
            )


def reward_claim_after_insert(doc, method):
    pass


def historical_record_on_update(doc, method):
    if doc.has_value_changed("record_status"):
        if doc.record_status == "Archived":
            send_notification(
                doc,
                "Historical Record Added",
                "Property Manager",
                f"New historical record {doc.record_title} archived"
            )


def historical_record_after_insert(doc, method):
    pass


def maintenance_schedule_on_update(doc, method):
    if doc.has_value_changed("maintenance_status"):
        if doc.maintenance_status == "Scheduled":
            send_notification(
                doc,
                "Maintenance Due",
                "Contractor",
                f"Maintenance scheduled for {doc.property}"
            )


def maintenance_schedule_after_insert(doc, method):
    pass


def abandoned_property_on_update(doc, method):
    if doc.has_value_changed("restoration_status"):
        if doc.restoration_status == "Restoration Started":
            send_notification(
                doc,
                "Restoration Started",
                "Property Manager",
                f"Restoration started for property {doc.property_name}"
            )
        elif doc.restoration_status == "Completed":
            send_notification(
                doc,
                "Restoration Completed",
                "Property Manager",
                f"Property {doc.property_name} restoration completed"
            )


def abandoned_property_after_insert(doc, method):
    pass


def send_notification(doc, subject, for_role, message):
    try:
        users = frappe.get_all(
            "Has Role",
            filters={"role": for_role},
            pluck="parent"
        )
        
        for user in users:
            notification = frappe.new_doc("Notification Log")
            notification.update({
                "type": "Alert",
                "document_type": doc.doctype,
                "document_name": doc.name,
                "subject": subject,
                "message": message,
                "for_user": user
            })
            notification.insert(ignore_permissions=True)
        
        frappe.publish_realtime("notification")
    except Exception as e:
        frappe.log_error(f"Error sending notification: {str(e)}", "Notification Error")


def update_abandoned_property_status(property_name, status):
    if frappe.db.exists("Abandoned Property", property_name):
        frappe.db.set_value(
            "Abandoned Property",
            property_name,
            "restoration_status",
            status,
            update_modified=False
        )
