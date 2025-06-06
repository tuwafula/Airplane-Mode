// Copyright (c) 2025, Aggrey Wafula and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
	refresh(frm) {
		frm.set_query("shop_type", () => {
			return {
				filters: {
					enabled: true,
				},
			};
		});

		if (frm.is_new()) {
			frappe.call({
				method: "airplane_mode.airport_shop_management.doctype.airport_shop.airport_shop.get_default_rent",
				callback: (response) => {
					if (response && response.message) {
						frm.set_value("shop_rent", response.message);
					}
				},
			});
		}
	},
});
