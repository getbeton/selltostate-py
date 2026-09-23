import json
import unittest
from selltostate import SellToState, AuthError, PaymentError, RateLimitError, DEFAULT_BASE_URL

class ClientTest(unittest.TestCase):
    def test_whoami_header(self):
        seen = {}
        def transport(url, method, headers, data):
            seen["url"] = url
            seen["headers"] = headers
            seen["calls"] = seen.get("calls", 0) + 1
            return 200, "{}"
        sts = SellToState(api_key="sts_test", client_id="nope", transport=transport)
        sts.whoami()
        self.assertEqual(seen["calls"], 1)
        self.assertEqual(seen["url"], DEFAULT_BASE_URL + "/api/v1/whoami")
        self.assertEqual(seen["headers"]["x-api-key"], "sts_test")
        self.assertNotIn("authorization", seen["headers"])

    def test_401(self):
        calls = {"n": 0}
        def transport(url, method, headers, data):
            calls["n"] += 1
            return 401, json.dumps({"error": "unauthorized"})
        with self.assertRaises(AuthError):
            SellToState(api_key="sts_test", transport=transport).whoami()
        self.assertEqual(calls["n"], 1)

    def test_402(self):
        calls = {"n": 0}
        body = {"payment_link": "https://pay.example", "plan": "data-monthly", "machine_payment": {"endpoint": "https://app.selltostate.com/api/v1/pay"}}
        def transport(url, method, headers, data):
            calls["n"] += 1
            return 402, json.dumps(body)
        with self.assertRaises(PaymentError) as ctx:
            SellToState(api_key="sts_test", transport=transport).searchAwards()
        self.assertEqual(ctx.exception.payment_link, body["payment_link"])
        self.assertEqual(ctx.exception.plan, body["plan"])
        self.assertEqual(ctx.exception.machine_payment, body["machine_payment"])
        self.assertEqual(calls["n"], 1)

    def test_429(self):
        calls = {"n": 0}
        def transport(url, method, headers, data):
            calls["n"] += 1
            return 429, "{}"
        with self.assertRaises(RateLimitError):
            SellToState(api_key="sts_test", transport=transport).whoami()
        self.assertEqual(calls["n"], 1)

if __name__ == "__main__":
    unittest.main()
