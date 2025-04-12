# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import random


class AirplaneTicket(Document):

    def validate(self):
        self.calculate_total_amount()
        self.remove_duplicate_add_ons()

    def calculate_total_amount(self):

        total_amount = int(self.flight_price)
        if self.add_ons:

            for add_on in self.add_ons:
                total_amount += int(add_on.amount)

        self.total_amount = total_amount

    def remove_duplicate_add_ons(self):
        seen_add_ons = set()
        unique_add_ons = []

        if self.add_ons:
            for add_on in self.add_ons:
                if add_on.item not in seen_add_ons:
                    seen_add_ons.add(add_on.item)
                    unique_add_ons.append(add_on)
                else:
                    frappe.msgprint(
                        msg="Add On {} has been removed as it already exists".format(
                            add_on.item
                        ),
                        alert=True,
                    )

            self.add_ons = unique_add_ons

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Status has to be Boarded to submit the ticket")

    def before_insert(self):
        self.set_seat_number()

    def set_seat_number(self):
        ticket_letters = ["A", "B", "C", "D", "E"]
        seat_number = "{}{}".format(
            random.randint(1, 100), random.choice(ticket_letters).upper()
        )

        self.seat = seat_number
