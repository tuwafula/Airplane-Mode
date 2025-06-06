# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):

    def before_submit(self):
        self.status = "Completed"

    def on_update(self):
        frappe.enqueue(self.update_gate_number, queue="short")

    def on_update_after_submit(self):
        frappe.enqueue(self.update_gate_number, queue="short")

    def update_gate_number(self):
        tickets = frappe.get_all("Airplane Ticket", filters={"flight": self.name})
        for ticket in tickets:
            frappe.db.set_value(
                "Airplane Ticket", ticket.get("name"), "gate_number", self.gate_number
            )
