# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):
    pass


@frappe.whitelist()
def get_default_rent():
    rent = frappe.get_doc("Airport Shop Settings").default_rent_amount
    return rent
