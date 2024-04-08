// Copyright (c) 2024, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Inward Pass', {
	refresh: function(frm) {
     if (frm.is_new()) {
            frm.set_value('date', frappe.datetime.now_datetime());
        }
      frm.set_value('entry_no',frm.doc.name);
	}

});
