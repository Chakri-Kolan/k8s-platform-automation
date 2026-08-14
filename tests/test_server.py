import json
import unittest

from app.server import payload


class PayloadTests(unittest.TestCase):
    def test_health_and_readiness(self) -> None:
        for path, expected in (("/health", "healthy"), ("/ready", "ready")):
            status, content_type, body = payload(path)
            self.assertEqual(200, status)
            self.assertEqual("application/json", content_type)
            self.assertEqual(expected, json.loads(body)["status"])

    def test_metrics_are_prometheus_compatible(self) -> None:
        status, content_type, body = payload("/metrics")
        self.assertEqual(200, status)
        self.assertIn("text/plain", content_type)
        self.assertIn(b"platform_app_requests_total", body)

    def test_unknown_route(self) -> None:
        status, _, body = payload("/missing")
        self.assertEqual(404, status)
        self.assertEqual("not_found", json.loads(body)["error"])


if __name__ == "__main__":
    unittest.main()
