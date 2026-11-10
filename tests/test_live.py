"""Live tests — hit the real verkehr.autobahn.de API. Cautious: few requests.

Run:  pytest tests/test_live.py -v
Skip: pytest -m "not live"  (or set AUTOBAHN_SKIP_LIVE=1)
"""
import json
import os
import pathlib
import sys
import unittest

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from autobahn_mcp import server as srv

pytestmark = pytest.mark.live
SKIP = os.environ.get("AUTOBAHN_SKIP_LIVE") == "1"


@pytest.mark.skipif(SKIP, reason="AUTOBAHN_SKIP_LIVE=1")
class TestLive(unittest.TestCase):
    def test_roadworks_live(self):
        out = json.loads(srv.autobahn_roadworks("A100", limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["count"], 0)
        print(f"\nLIVE roadworks A100: {out['total_results']} total")

    def test_closures_live(self):
        out = json.loads(srv.autobahn_closures("A1", limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)
        print(f"\nLIVE closures A1: {out['total_results']} total")

    def test_warnings_live(self):
        out = json.loads(srv.autobahn_warnings("A100", limit=3))
        self.assertNotIn("error", out)
        print(f"\nLIVE warnings A100: {out['total_results']} total")

    def test_parking_live(self):
        out = json.loads(srv.autobahn_parking("A1", limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)
        print(f"\nLIVE parking A1: {out['total_results']} total")

    def test_ev_live(self):
        out = json.loads(srv.autobahn_ev_charging("A1", limit=3))
        self.assertNotIn("error", out)
        self.assertGreaterEqual(out["total_results"], 1)
        print(f"\nLIVE EV A1: {out['total_results']} total")

    def test_health_live(self):
        out = json.loads(srv.autobahn_health())
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["http_status"], 200)
