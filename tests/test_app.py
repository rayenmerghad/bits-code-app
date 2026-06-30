import unittest

from app import app as flask_app


class DiscountedPriceTests(unittest.TestCase):
    def setUp(self):
        flask_app.config["TESTING"] = True
        self.client = flask_app.test_client()

    def test_discounted_price_casts_query_param_to_float(self):
        response = self.client.get("/products/1/discounted-price?discount=5")

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.get_json()["discounted_price"], 4.99, places=2)

    def test_discounted_price_returns_bad_request_for_non_numeric_discount(self):
        response = self.client.get("/products/1/discounted-price?discount=abc")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "invalid discount"})


if __name__ == "__main__":
    unittest.main()
