// Copyright (c) 2025, Aggrey Wafula and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rent Invoice", {
	refresh(frm) {},
	validate(frm) {
		if (frm.doc.due_date < frm.doc.date) {
			frappe.throw("Due Date cannot be earlier than the Date of the invoice");
		}
	},
});

frappe.ui.form.on("Rent Invoice Item", {
	rate: function (frm, cdt, cdn) {
		calculateAmount(frm, cdt, cdn);
		calculateTotalAmount(frm);
	},
	qty: function (frm, cdt, cdn) {
		calculateAmount(frm, cdt, cdn);
		calculateTotalAmount(frm);
	},
	items_remove: function (frm) {
		calculateTotalAmount(frm);
	},
});

function calculateAmount(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	if (row.qty && row.rate) {
		const amount = row.qty * row.rate;
		frappe.model.set_value(cdt, cdn, "amount", amount);
	}
	frm.refresh_fields();
}

function calculateTotalAmount(frm) {
	if (frm.doc.items) {
		let totalAmount = 0;
		frm.doc.items.forEach((item) => {
			totalAmount += item.amount;
		});

		frm.set_value("total_amount", totalAmount);
		frm.set_value("outstanding_amount", totalAmount);
	}
}
