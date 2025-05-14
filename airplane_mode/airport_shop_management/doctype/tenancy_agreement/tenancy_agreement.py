# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TenancyAgreement(Document):

    def before_save(self):
        shop_doc = frappe.get_doc("Airport Shop", self.shop_number)
        if shop_doc.occupancy_status == "Available For Lease":
            self.update_occupancy_status("Occupied")

    def on_cancel(self):
        shop_doc = frappe.get_doc("Airport Shop", self.shop_number)
        if shop_doc.occupancy_status == "Occupied":
            self.update_occupancy_status("Available For Lease")

    def on_trash(self):
        shop_doc = frappe.get_doc("Airport Shop", self.shop_number)
        if shop_doc.occupancy_status == "Occupied":
            self.update_occupancy_status("Available For Lease")

    def update_occupancy_status(self, occupancy_status):
        frappe.db.set_value(
            "Airport Shop", self.shop_number, "occupancy_status", occupancy_status
        )
