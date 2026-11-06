import unittest
from unittest import mock

from judgebench import judges


class DecisionsJudgeTests(unittest.TestCase):
    def decide(self, name, response, text="部長がおっしゃられました。"):
        with mock.patch.object(judges, "_decide_request", return_value=response):
            return judges.make(name).decide("honorific", text)

    def test_noul_probability_at_or_above_half_is_yes(self):
        out = self.decide("jev", {"answers": {"q": {"type": "noul", "noul": 0.5}}})
        self.assertEqual((out["verdict"], out["p_yes"]), ("YES", 0.5))

    def test_predicate_probability_below_half_is_no(self):
        out = self.decide("gpt_6_luna", {"answers": [{"type": "predicate", "name": "q", "probability": 0.49}]})
        self.assertEqual(out["verdict"], "NO")

    def test_missing_probability_is_no_answer(self):
        out = self.decide("clef_flash", {"answers": {"q": {"type": "refusal"}}})
        self.assertIsNone(out["verdict"])

    def test_cloudflare_result_is_unwrapped(self):
        out = self.decide("clef", {"result": {"answers": {"q": {"type": "noul", "noul": 0.7}}}, "success": True})
        self.assertEqual((out["verdict"], out["p_yes"]), ("YES", 0.7))

    def test_cloudflare_body_has_no_model_field(self):
        self.assertNotIn("model", judges.make("clef")._payload(judges.QUESTIONS["honorific"], "x"))

    def test_payload_shapes(self):
        q = judges.QUESTIONS["honorific"]
        noul = judges.make("jev")._payload(q, "x")
        self.assertEqual(noul["questions"]["q"]["criteria"], {"true": q["true"], "false": q["false"]})
        predicate = judges.make("gpt_6_luna")._payload(q, "x")
        self.assertIn(q["false"], predicate["questions"][0]["instructions"])


if __name__ == "__main__":
    unittest.main()
