from django.test import TestCase


class HealthCheckTests(TestCase):
    def test_health_check(self) -> None:
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
