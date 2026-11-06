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


class GeminiJudgeTests(unittest.TestCase):
    def ask(self, text):
        res = {"candidates": [{"content": {"parts": [{"text": text}]}}]}
        with mock.patch.object(judges, "_decide_request", return_value=res):
            return judges.make("gemini_flash").ask("q")

    def test_first_line_yes_or_no_is_the_verdict(self):
        self.assertEqual(self.ask("YES\nbecause")["verdict"], "YES")
        self.assertEqual(self.ask("NO")["verdict"], "NO")

    def test_anything_else_is_no_answer(self):
        self.assertIsNone(self.ask("Maybe")["verdict"])

    def test_empty_candidate_is_no_answer(self):
        with mock.patch.object(judges, "_decide_request", return_value={"candidates": [{"finishReason": "MAX_TOKENS"}]}):
            self.assertIsNone(judges.make("gemini_flash").ask("q")["verdict"])


class ClaudeApiJudgeTests(unittest.TestCase):
    def ask(self, name, blocks):
        client = mock.Mock()
        client.messages.create.return_value = mock.Mock(content=blocks, usage=mock.Mock(output_tokens=7))
        judge = judges.make(name)
        judge._client = client
        return judge.ask("q"), client.messages.create.call_args.kwargs

    def block(self, kind, text=""):
        return mock.Mock(type=kind, text=text)

    def test_text_block_after_thinking_is_the_verdict(self):
        out, _ = self.ask("claude_api_think", [self.block("thinking"), self.block("text", "YES")])
        self.assertEqual((out["verdict"], out["output_tokens"]), ("YES", 7))

    def test_no_text_block_is_no_answer(self):
        out, _ = self.ask("claude_api_think", [self.block("thinking")])
        self.assertIsNone(out["verdict"])

    def test_off_disables_thinking_and_think_leaves_the_default(self):
        _, off = self.ask("claude_api_off", [self.block("text", "NO")])
        _, think = self.ask("claude_api_think", [self.block("text", "NO")])
        self.assertEqual(off["thinking"], {"type": "disabled"})
        self.assertNotIn("thinking", think)


if __name__ == "__main__":
    unittest.main()
