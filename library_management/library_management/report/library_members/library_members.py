import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Member ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 150,
        },
        {
            "label": "First Name",
            "fieldname": "first_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Last Name",
            "fieldname": "last_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Full Name",
            "fieldname": "full_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Email Address",
            "fieldname": "email_address",
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "label": "Phone",
            "fieldname": "phone",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Date",
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120,
        },
    ]

    data = frappe.get_all(
        "Library Member",
        fields=[
            "name",
            "first_name",
            "last_name",
            "full_name",
            "email_address",
            "phone",
            "date",
        ],
        limit_page_length=10,
    )

    return columns, data