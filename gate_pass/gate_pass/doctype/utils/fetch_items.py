import frappe


@frappe.whitelist()
def fetch_gip_items(**args):
    po_no = args.get('po_no')
    poi = frappe.qb.DocType("Purchase Order Item")
    parent_query = (
        frappe.qb.from_(poi)
        .select(
            poi.item_code,
            poi.qty,
            poi.uom,
            poi.rate
        ).where((poi.parent == po_no))
    )
    poi_result = parent_query.run(as_dict=True)

    return {
        "poi": poi_result,
    }
@frappe.whitelist()
def fetch_so_items(**args):
    so_no = args.get('so_no')
    soi = frappe.qb.DocType("Sales Order Item")
    parent_query = (
        frappe.qb.from_(soi)
        .select(
            soi.finish_item,
            soi.qty,
            soi.uom,
            soi.rate,
            soi.description

        ).where((soi.parent == so_no))
    )
    soi_result = parent_query.run(as_dict=True)

    return {
        "soi": soi_result,
    }
@frappe.whitelist()
def fetch_mr_items(**args):
    mr_no = args.get('mr_no')
    mri = frappe.qb.DocType("Material Request Item")
    parent_query = (
        frappe.qb.from_(mri)
        .select(
            mri.item_code,
            mri.qty,
            mri.uom
        ).where((mri.parent == mr_no))
    )
    mri_result = parent_query.run(as_dict=True)

    return {
        "mri": mri_result,
    }
@frappe.whitelist()
def fetch_outward_items(**args):
    outward_no = args.get('outward_no')
    gopi = frappe.qb.DocType("Gate Outward Pass Items")
    parent_query = (
        frappe.qb.from_(gopi)
        .select(
            gopi.item_code,
            gopi.qty,
            gopi.uom,
            gopi.description
        ).where((gopi.parent == outward_no))
    )
    gopi_result = parent_query.run(as_dict=True)

    return {
        "gopi": gopi_result,
    }
@frappe.whitelist()
def fetch_gop_items(**args):
    is_return = False
    no = args.get('no')
    source = args.get('source')
    child = ""
    if(source == "PRR"):
        is_return = True
    if(source == "DN"):
            child = "Delivery Note Item"
    elif(source == "PO"):
            child = "Purchase Order Item"
    elif(source == "PRR"):
            child = "Purchase Receipt Item"

    dni = frappe.qb.DocType(child)
    parent_query = (
        frappe.qb.from_(dni)
        .select(
            dni.item_code,
            dni.qty,
            dni.uom,
            dni.description
        ).where((dni.parent == no)
        
        )
    )
    if is_return:
        parent_query = parent_query.where(dni.is_return == 1)
    dni_result = parent_query.run(as_dict=True)

    return {
        "dni": dni_result,
    }

@frappe.whitelist()
def fetch_employee_info(**args):
    attendance_device_id = args.get('attendance_device_id')
    emp = frappe.qb.DocType("Employee")
    parent_query = (
        frappe.qb.from_(emp)
        .select(
            emp.employee,
            emp.employee_name,
            emp.attendance_device_id,
            emp.department,
            emp.division
        ).where((emp.attendance_device_id == attendance_device_id))
    )
    emp_result = parent_query.run(as_dict=True)

    return {
        "emp": emp_result,
    }