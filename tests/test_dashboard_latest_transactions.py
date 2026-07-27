import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app
import database


class DashboardLatestTransactionsTest(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()
        self.email = "latestorder@example.com"
        self.password = "secret123"
        try:
            self.client.post(
                "/register",
                data={"name": "Latest Order", "email": self.email, "password": self.password},
            )
        except Exception:
            pass
        self.client.post(
            "/login",
            data={"email": self.email, "password": self.password},
        )

        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE user_id IN (SELECT id FROM users WHERE email=?)", (self.email,))
        conn.commit()
        conn.close()

    def test_dashboard_shows_newest_transactions_first(self):
        self.client.post(
            "/add",
            data={"date": "2026-07-27", "category": "Groceries", "type": "Expense", "amount": "120"},
        )
        self.client.post(
            "/add",
            data={"date": "2026-07-27", "category": "Taxi", "type": "Expense", "amount": "90"},
        )

        response = self.client.get("/dashboard")

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        first_idx = html.index("Taxi")
        second_idx = html.index("Groceries")
        self.assertLess(first_idx, second_idx)


if __name__ == "__main__":
    unittest.main()
