from datetime import date
from dateutil.relativedelta import relativedelta


import frappe
import frappe.query_builder
import frappe.query_builder.functions
from frappe.utils import add_days


def generate_rent_invoice():
    today = date.today()
    current_month_end = today + relativedelta(day=31)
    days = frappe.get_doc("Airport Shop Settings").invoice_due_days
    due_date = add_days(today, days=days)

    # Get all tenancy agreements
    tenancy_agreements = frappe.get_all(
        "Tenancy Agreement",
        ["tenant", "shop_number", "rent_amount"],
        [["date_of_expiry", ">", current_month_end]],
    )

    tenants = list(set([x.get("tenant") for x in tenancy_agreements]))

    try:
        # Create Rent Invoice
        for tenant in tenants:
            rent_invoice = frappe.new_doc("Rent Invoice")
            rent_invoice.tenant = tenant
            rent_invoice.posting_date = today
            rent_invoice.due_date = due_date

            total_amount = 0

            for agreement in tenancy_agreements:
                if agreement.get("tenant") == tenant:
                    rent_invoice.append(
                        "items",
                        {
                            "shop": agreement.get("shop_number"),
                            "qty": 1,
                            "rate": agreement.get("rent_amount"),
                            "amount": agreement.get("rent_amount"),
                        },
                    )

                    total_amount += agreement.get("rent_amount")

            rent_invoice.total_amount = total_amount
            rent_invoice.outstanding_amount = total_amount
            rent_invoice.save()
            rent_invoice.submit()
    except Exception as e:
        frappe.msgprint(
            frappe.get_traceback(),
            f"Something went wrong while creating invoice {str(e)}",
        )
