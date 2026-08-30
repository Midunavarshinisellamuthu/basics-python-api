import frappe
from frappe.rate_limiter import rate_limit

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

@frappe.whitelist()
def get_recent_todos():
    todos = frappe.get_list(
        "ToDo",
        fields=["name", "description", "owner"],
        order_by="creation desc",
        limit_page_length=5
    )

    for todo in todos:
        todo["email"] = frappe.db.get_value(
            "User",
            todo["owner"],
            "email"
        )

    timestamp = frappe.utils.now()

    return {
        "timestamp": timestamp,
        "records": todos
    }

#Javascript API
@frappe.whitelist()
def create_task(task_subject):
    task = frappe.new_doc("Task")
    task.subject = task_subject
    task.save()

    return task.name

@frappe.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60)
def limited_greeting():
    logger = frappe.logger()
    logger.info("Endpoint called.")

    frappe.response["message"] = "Hello, Rate Limited World!"