# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import functions as fn


def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data()

    report_summary = get_report_summary(data)
    chart = {
        "type": "donut",
        "data": {
            "labels": [row["airline"] for row in data],
            "datasets": [{"values": [row["revenue"] for row in data]}],
        },
    }

    return columns, data, [], chart, report_summary


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "label": _("Airline"),
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200,
        },
        {
            "label": _("Revenue"),
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 200,
        },
    ]


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """

    airline_doc = frappe.qb.DocType("Airline")
    ticket_doc = frappe.qb.DocType("Airplane Ticket")
    flight_doc = frappe.qb.DocType("Airplane Flight")
    airplane_doc = frappe.qb.DocType("Airplane")

    query = (
        frappe.qb.from_(airline_doc)
        .left_join(airplane_doc)
        .on(airplane_doc.airline == airline_doc.name)
        .left_join(flight_doc)
        .on(flight_doc.airplane == airplane_doc.name)
        .left_join(ticket_doc)
        .on(ticket_doc.flight == flight_doc.name)
        .select(
            airline_doc.name.as_("airline"),
            fn.Coalesce(fn.Sum(ticket_doc.total_amount), 0).as_("revenue"),
        )
        .groupby(airplane_doc.airline)
        .orderby(ticket_doc.total_amount, order=frappe.qb.desc)
    )

    return query.run(as_dict=True)


def get_report_summary(data):
    total_revenue = 0
    if data:
        for row in data:
            total_revenue += row.get("revenue")
    return [
        {
            "value": total_revenue,
            "indicator": "Green" if total_revenue > 0 else "Red",
            "label": _("Total Revenue"),
            "datatype": "Currency",
            "currency": "KES",
        },
    ]
