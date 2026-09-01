// Copyright (c) 2026, Deepak Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
	refresh(frm) {
		const full_name = frm.get_field("full_name");
		const light_green = "var(--green-100)";

		full_name?.$input?.css("background-color", light_green);
		full_name?.$wrapper.find(".control-value").css("background-color", light_green);
	},
});
