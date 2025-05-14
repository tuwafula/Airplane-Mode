# Copyright (c) 2025, Aggrey Wafula and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from frappe.model.document import Document


class RentInvoice(Document):
    def validate(self):
        if self.total_amount == 0:
            frappe.throw("Total Invoice amount cannot be zero")

        if getdate(self.due_date) < getdate(self.posting_date):
            frappe.throw("Due date cannot be before posting date")
            self.status = "Unpaid"
        elif getdate(self.due_date) == getdate(self.posting_date):
            self.status = "Overdue"
        else:
            self.status = "Unpaid"
