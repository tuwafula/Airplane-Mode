// Copyright (c) 2025, Aggrey Wafula and contributors
// For license information, please see license.txt

frappe.query_reports["Shops By Airport"] = {
	filters: [
		{
			fieldname: "airport",
			label: __("Airport"),
			fieldtype: "Link",
			options: "Airport",
		},
	],
};
