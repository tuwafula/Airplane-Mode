# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):

    def before_submit(self):
        """reconcile invoice with payment"""
        try:
            rent_invoice = frappe.get_doc("Rent Invoice", self.rent_invoice)
            total_due = rent_invoice.total_amount
            outstanding_amount = self.amount_paid - total_due

            frappe.db.set_value(
                "Rent Invoice",
                self.rent_invoice,
                {
                    "status": "Paid" if outstanding_amount <= 0 else "Partly Paid",
                    "outstanding_amount": (
                        0 if outstanding_amount <= 0 else outstanding_amount
                    ),
                    "amount_paid": self.amount_paid,
                },
                update_modified=True,
            )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                f"Something went wrong while reconciling the payment: {str(e)}",
            )
