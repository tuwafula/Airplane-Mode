import frappe


def send_rent_reminder():
    disable_rent_reminders = frappe.get_doc(
        "Airport Shop Settings"
    ).disable_rent_reminders
    if disable_rent_reminders:
        return

    overdue_invoices = frappe.get_all(
        "Rent Invoice",
        ["name", "tenant"],
        filters={"docstatus": 1, "status": "Overdue"},
    )

    if overdue_invoices:
        try:
            for invoice in overdue_invoices:
                tenant_email = frappe.db.get_value(
                    "Tenant", invoice.get("tenant"), "email"
                )
                subject = f"Please settle your due Invoice: {invoice.get("name")}"
                message = "Dear Tenant\nYour rent invoice is due. Kindly settle it to avoid penalties"
                frappe.sendmail(
                    recipients=[tenant_email], subject=subject, message=message
                )
        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(), f"Error while sending reminder email {str(e)}"
            )
