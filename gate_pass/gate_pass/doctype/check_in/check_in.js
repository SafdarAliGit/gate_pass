// Copyright (c) 2024, Tech Ventures and contributors
// For license information, please see license.txt

frappe.ui.form.on('Check In', {
    refresh: function (frm) {

        frm.set_query('employee', function () {
            return {
                filters: {
                    employee_group: 'Contractor Labour'
                }
            };
        });

        if (frm.is_new()) {
            frm.set_value('date', frappe.datetime.now_datetime());
        }
        employee_photo(frm);
    },
    // after_save: function (frm) {
    //     frappe.set_route("Form", "Check In", "new-check-in");
    // },
    employee_id: function (frm) {
        fetch_employee_info(frm, frm.doc.employee_id);
    },
    employee: function (frm) {
        employee_photo(frm);
    }
});


function fetch_employee_info(frm, attendance_device_id) {
    if (attendance_device_id) {
        // Clear existing data before adding new entries

        frappe.call({
            method: "gate_pass.gate_pass.doctype.utils.fetch_items.fetch_employee_info",
            args: {
                attendance_device_id: attendance_device_id
            },
            callback: function (response) {
                if (response.message.emp) {
                    frm.set_value('employee', response.message.emp[0].employee);
                    frm.set_value('employee_name', response.message.emp[0].employee_name);
                    frm.set_value('employee_id', response.message.emp[0].attendance_device_id);
                    frm.set_value('department', response.message.emp[0].department);
                    frm.set_value('division', response.message.emp[0].division);

                }
            }
        });
    }
}

function employee_photo(frm) {
    if (frm.doc.employee) {
        frappe.db.get_value('Employee', frm.doc.employee, 'image', (r) => {
            if (r && r.image) {
                // Display the image using HTML in the HTML field
                frm.fields_dict['employee_photo_html'].$wrapper.html(`<img src="${r.image}" width="150px">`);
            } else {
                // Clear the HTML field if no image is available
                frm.fields_dict['employee_photo_html'].$wrapper.html('');
            }
        });
    } else {
        frm.fields_dict['employee_photo_html'].$wrapper.html('');
    }

}