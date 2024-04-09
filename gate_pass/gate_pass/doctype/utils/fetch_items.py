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
            poi.uom
        ).where((poi.parent == po_no))
    )
    poi_result = parent_query.run(as_dict=True)

    return {
        "poi": poi_result,
    }

@frappe.whitelist()
def fetch_gop_items(**args):
    dn_no = args.get('dn_no')
    dni = frappe.qb.DocType("Delivery Note Item")
    parent_query = (
        frappe.qb.from_(dni)
        .select(
            dni.item_code,
            dni.qty,
            dni.uom
        ).where((dni.parent == dn_no))
    )
    dni_result = parent_query.run(as_dict=True)

    return {
        "dni": dni_result,
    }
