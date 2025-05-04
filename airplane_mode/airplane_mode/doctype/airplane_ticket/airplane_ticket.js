// Copyright (c) 2025, Aggrey Wafula and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		frm.add_custom_button(
			__("Assign Seat"),
			function () {
				let d = new frappe.ui.Dialog({
					title: "Select Seat",
					fields: [
						{
							label: "Seat Number",
							fieldname: "seat_number",
							fieldtype: "Data",
						},
					],
					size: "small",
					primary_action_label: "Assign",
					primary_action(values) {
						if (values) {
							frm.set_value("seat", values.seat_number);
							frm.save();
						}
						d.hide();
					},
				});

				d.show();
			},
			"Actions"
		);
	},
});
