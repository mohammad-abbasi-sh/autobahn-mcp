"""Offline tests — parse real captured verkehr.autobahn.de responses, no network."""
import json
import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from autobahn_mcp import domain as dom
from autobahn_mcp import server as srv

FIX = pathlib.Path(__file__).resolve().parent / "fixtures"


def _read(name):
    return (FIX / name).read_text(encoding="utf-8")


class TestRoadValidation(unittest.TestCase):
    def test_valid_roads(self):
        self.assertEqual(dom.validate_road("A1"), "A1")
        self.assertEqual(dom.validate_road("a100"), "A100")
        self.assertEqual(dom.validate_road("  A7  "), "A7")

    def test_invalid_roads(self):
        for bad in ["", "A", "1", "AB1", "A1000", "Bundesstraße", "A-1"]:
            with self.assertRaises(ValueError, msg=bad):
                dom.validate_road(bad)

    def test_limit(self):
        self.assertEqual(dom.validate_limit(10), 10)
        with self.assertRaises(ValueError):
            dom.validate_limit(0)
        with self.assertRaises(ValueError):
            dom.validate_limit(51)


class TestFixtures(unittest.TestCase):
    def test_roadworks_a1(self):
        out = dom.parse_service(_read("roadworks-a1.json"), "roadworks")
        self.assertEqual(out["count"], 261)
        first = out["items"][0]
        self.assertTrue(first["identifier"] and first["title"])
        self.assertIn("lat", (first["coordinate"] or {}))

    def test_closures_a1(self):
        out = dom.parse_service(_read("closures-a1.json"), "closure")
        self.assertEqual(out["count"], 53)
        self.assertTrue(all(i["title"] for i in out["items"]))

    def test_warnings_a100(self):
        out = dom.parse_service(_read("warnings-a100.json"), "warning")
        self.assertEqual(out["count"], 4)
        self.assertTrue(all(i["headline"] if False else i["title"] for i in out["items"]))

    def test_parking_a1(self):
        out = dom.parse_service(_read("parking-a1.json"), "parking_lorry")
        self.assertEqual(out["count"], 133)
        first = out["items"][0]
        self.assertTrue(first["title"].startswith("A1"))
        self.assertIn("Stellplätze", first["description"])

    def test_ev_a1(self):
        out = dom.parse_service(_read("ev-a1.json"), "electric_charging_station")
        self.assertEqual(out["count"], 31)
        self.assertTrue(all("Ladepunkt" in i["description"] for i in out["items"]))

    def test_empty_service_is_valid(self):
        # The API returns [] when a road currently has no entries of a
        # kind (traffic fixture proves the empty shape parses).
        data = json.loads(_read("traffic-empty.json"))
        self.assertEqual(data["traffic"], [])
        out = dom.parse_service('{"roadworks": []}', "roadworks")
        self.assertEqual(out, {"count": 0, "items": []})

    def test_bad_json(self):
        with self.assertRaises(ValueError):
            dom.parse_service("<html>nope</html>", "roadworks")

    def test_missing_key(self):
        with self.assertRaises(ValueError):
            dom.parse_service('{"other": []}', "roadworks")


class TestServerOffline(unittest.TestCase):
    def test_tool_uses_fixture_via_mock(self):
        with mock.patch("autobahn_mcp.http.fetch_text",
                        return_value=_read("closures-a1.json")):
            out = json.loads(srv.autobahn_closures("A1", limit=3))
        self.assertEqual(out["road"], "A1")
        self.assertEqual(out["total_results"], 53)
        self.assertEqual(out["count"], 3)
        self.assertIn("fetched_at", out)
        self.assertEqual(out["source"], "verkehr.autobahn.de")

    def test_tool_bad_road(self):
        out = json.loads(srv.autobahn_roadworks("XX", limit=3))
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
