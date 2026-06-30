import unittest

from app import PRODUCTS, app


class ScoreEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_score_is_zero_for_out_of_stock_product(self):
        response = self.client.get("/products/2/score")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"score": 0.0})

    def test_score_scales_with_catalog_max_stock(self):
        response = self.client.get("/products/1/score")
        max_stock = max((product["stock"] for product in PRODUCTS.values()), default=0)
        expected_score = (
            0.0 if max_stock <= 0 else (PRODUCTS[1]["stock"] / max_stock) * 100
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"score": expected_score})
