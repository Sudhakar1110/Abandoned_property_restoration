import frappe


def get_employee_query(keyword, filters):
    return frappe.db.sql(
        """
        SELECT name, employee_name, designation, department
        FROM tabEmployee
        WHERE docstatus < 2
        AND (employee_name LIKE %(keyword)s
            OR name LIKE %(keyword)s
            OR designation LIKE %(keyword)s)
        {conditions}
        ORDER BY employee_name ASC
        LIMIT 20
        """.format(
            conditions=get_conditions(filters)
        ),
        {"keyword": "%" + keyword + "%"},
    )


def get_conditions(filters):
    conditions = []
    if filters:
        for key, value in filters.items():
            if value:
                conditions.append(f"AND {key} = '{value}'")
    return " ".join(conditions)


def validate_naming_series(doc, method):
    if doc.naming_series:
        if not frappe.db.exists("Naming Series", doc.naming_series):
            frappe.throw(f"Naming Series {doc.naming_series} does not exist")


def send_notification(doc, event, notification_type, message):
    notification = frappe.new_doc("Notification Log")
    notification.update(
        {
            "type": notification_type,
            "document_type": doc.doctype,
            "document_name": doc.name,
            "subject": f"{doc.doctype}: {message}",
            "message": message,
            "for_user": doc.owner if hasattr(doc, "assigned_to") else None,
        }
    )
    notification.insert(ignore_permissions=True)
    frappe.publish_realtime("notification")


def update_property_status(property_name, status):
    if frappe.db.exists("Abandoned Property", property_name):
        frappe.db.set_value(
            "Abandoned Property",
            property_name,
            "restoration_status",
            status,
            update_modified=False
        )


def calculate_project_cost(project_name):
    total_cost = 0.0
    expenses = frappe.get_all(
        "Expense Entry",
        filters={"parent_project": project_name},
        fields=["SUM(total_amount) as total"]
    )
    if expenses and expenses[0].total:
        total_cost = expenses[0].total
    frappe.db.set_value(
        "Restoration Project",
        project_name,
        "total_cost",
        total_cost,
        update_modified=False
    )
    return total_cost


def get_available_materials(material_type=None):
    filters = {"status": "Available"}
    if material_type:
        filters["material_type"] = material_type
    
    materials = frappe.get_all(
        "Material Salvage",
        filters=filters,
        fields=["name", "material_name", "quantity", "condition", "location"]
    )
    return materials


def create_time_capsule_entry(property_name, record_type, data):
    time_capsule = frappe.new_doc("Digital Time Capsule")
    time_capsule.property = property_name
    time_capsule.capsule_category = record_type
    time_capsule.title = data.get("title", "Historical Record")
    time_capsule.description = data.get("description", "")
    time_capsule.record_date = data.get("record_date", frappe.utils.today())
    time_capsule.insert(ignore_permissions=True)
    return time_capsule.name
