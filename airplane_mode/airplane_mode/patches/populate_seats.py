import frappe
import random


def execute():
    tickets = frappe.db.get_all(
        "Airplane Ticket", filters={"seat": ["is", "not set"]}, pluck="name"
    )

    if tickets:
        for t in tickets:
            seat_number = "{}{}".format(random.randint(1, 100), random.choice("ABCDE"))

            frappe.db.set_value("Airplane Ticket", t, "seat", seat_number)

        frappe.db.commit()
