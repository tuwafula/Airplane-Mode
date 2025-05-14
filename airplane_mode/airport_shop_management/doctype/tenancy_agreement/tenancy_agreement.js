// Copyright (c) 2025, Aggrey Wafula and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenancy Agreement", {
	refresh(frm) {
		frm.set_query("shop_number", () => {
			return {
				filters: {
					occupancy_status: "Available For Lease",
				},
			};
		});
	},
});
