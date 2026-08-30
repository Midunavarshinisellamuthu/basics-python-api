import frappe
from frappe.tests.utils import FrappeTestCase


class TestArticle(FrappeTestCase):

    def test_article_creation(self):
        article = frappe.get_doc({
            "doctype": "Article",
            "data_elby": "My First Test",
            "status": "Available"
        }).insert()

        self.assertEqual(article.data_elby, "My First Test")
        self.assertTrue(
            frappe.db.exists("Article", article.name)
        )