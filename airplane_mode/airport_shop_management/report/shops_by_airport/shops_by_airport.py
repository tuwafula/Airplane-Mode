# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from collections import defaultdict


def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns() -> list[dict]:
    """Return columns for the report.

    One field definition per column, just like a DocType field definition.
    """
    return [
        {
            "label": _("Airport"),
            "fieldname": "airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 150,
        },
        {
            "label": _("Shops Count"),
            "fieldname": "shops_count",
            "fieldtype": "Int",
            "width": 150,
        },
        {
            "label": _("Occupied Shops"),
            "fieldname": "occupied_shops",
            "fieldtype": "Int",
            "width": 150,
        },
        {
            "label": _("Shops Available For Lease"),
            "fieldname": "shops_available_for_lease",
            "fieldtype": "Int",
            "width": 150,
        },
    ]


def get_data(filters) -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    shop_filters = {}

    if filters.get("airport"):
        shop_filters["airport"] = filters.get("airport")

    shops = frappe.get_all(
        "Airport Shop",
        filters=shop_filters,
        fields=["airport", "occupancy_status"],
    )

    airport_data = defaultdict(
        lambda: {
            "airport": "",
            "shops_count": 0.0,
            "occupied_shops": 0.0,
            "shops_available_for_lease": 0.0,
        }
    )

    for shop in shops:
        key = shop.get("airport")
        airport_data[key]["airport"] = key
        airport_data[key]["shops_count"] += 1
        if shop.get("occupancy_status") == "Occupied":
            airport_data[key]["occupied_shops"] += 1
        else:
            airport_data[key]["shops_available_for_lease"] += 1

    if airport_data:
        return list(airport_data.values())

    return list
