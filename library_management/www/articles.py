import frappe


def get_context(context):
    context.articles = frappe.get_all(
        "Article",
        filters={"status": "Issued"},
        fields=["data_elby","name"]
    )