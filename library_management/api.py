import frappe


def custom_logic(doc, method):
    frappe.msgprint("Hook executed!")


@frappe.whitelist()
def update_memberships():
    LibraryMembership = frappe.qb.DocType("Library Membership")
    LibraryMember = frappe.qb.DocType("Library Member")

    query = (
        frappe.qb.from_(LibraryMembership)
        .join(LibraryMember)
        .on(LibraryMembership.library_member == LibraryMember.name)
        .select(
            LibraryMembership.name,
            LibraryMembership.library_member,
            LibraryMembership.from_date,
            LibraryMembership.to_date,
            LibraryMembership.paid,
            LibraryMember.full_name,
        )
        .where(LibraryMembership.docstatus == 0)
        .limit(10)
    )

    records = query.run(as_dict=True)

    if not records:
        return []

    # Document API
    first_record = frappe.get_doc(
        "Library Membership",
        records[0]["name"]
    )

    first_record.paid = 1
    first_record.save()

    # Database API
    for record in records:
        frappe.db.set_value(
            "Library Membership",
            record["name"],
            "paid",
            1
        )

# Fetch updated results
    records = query.run(as_dict=True)

    return records