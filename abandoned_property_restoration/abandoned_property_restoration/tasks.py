import frappe


def all():
    pass


def daily():
    frappe.publish_realtime("bench_event", {"message": "Daily tasks completed"})
    pass


def hourly():
    pass


def weekly():
    pass


def monthly():
    pass


def yearly():
    pass
