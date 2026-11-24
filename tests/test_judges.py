import io
import json
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
        gemini = judges.make("gemini_decision")._payload(q, "x")
        self.assertEqual(gemini["questions"]["q"]["criteria"],
                         {"true_description": q["true"], "false_description": q["false"]})

    def test_key_header_only_for_gemini(self):
        self.assertEqual(judges.make("gemini_decision").key_header, "x-goog-api-key")
        for name in ("jev", "clef", "clef_flash", "gpt_6_luna"):
            self.assertIsNone(judges.make(name).key_header)


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


class OllamaThinkJudgeTests(unittest.TestCase):
    def ask(self, content):
        with mock.patch.object(judges, "_post", return_value={"message": {"content": content}, "eval_count": 9}) as post:
            return judges.make("gemma4:26b+think").ask("q"), post.call_args.args[1]

    def test_first_word_is_the_verdict(self):
        self.assertEqual(self.ask("YES")[0]["verdict"], "YES")
        self.assertEqual(self.ask("No.\nbecause")[0]["verdict"], "NO")

    def test_anything_else_is_no_answer(self):
        self.assertIsNone(self.ask("Maybe")[0]["verdict"])

    def test_thinking_is_on_and_the_name_marks_it(self):
        out, request = self.ask("YES")
        self.assertTrue(request["think"])
        self.assertEqual(judges.make("gemma4:26b+think").name, "gemma4_26b_think")


class SyncStrataJudgeTests(unittest.TestCase):
    def ask(self, content):
        seen = {}

        def fake_urlopen(req, timeout):
            seen["body"] = json.loads(req.data)
            seen["url"] = req.full_url
            payload = {"choices": [{"message": {"content": content}}], "timings": {"prompt_ms": 300.0, "predicted_ms": 20.0}}
            return io.BytesIO(json.dumps(payload).encode())

        with mock.patch.object(judges.urllib.request, "urlopen", fake_urlopen):
            return judges.make("sync_m").ask("p"), seen

    def test_thinking_is_off_and_the_request_is_greedy(self):
        _, seen = self.ask("YES")
        self.assertEqual(seen["body"]["reasoning_effort"], "none")
        self.assertEqual(seen["body"]["temperature"], 0)
        self.assertTrue(seen["url"].endswith("/v1/chat/completions"))

    def test_each_engine_sends_its_own_model_id(self):
        _, seen = self.ask("YES")
        self.assertEqual(seen["body"]["model"], "qwen3.8-flash-next-sync-m")
        with mock.patch.object(judges.urllib.request, "urlopen") as urlopen:
            urlopen.return_value = io.BytesIO(json.dumps({"choices": [{"message": {"content": "NO"}}]}).encode())
            judge = judges.make("inkling_2_mini")
            judge.ask("p")
            body = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual((judge.name, body["model"]), ("inkling_2_mini", "inkling-2-mini-sq-20"))

    def test_logprob_engine_is_judged_by_probability_like_ollama(self):
        reply = {"choices": [{"logprobs": {"content": [{"token": "NO", "top_logprobs": [
            {"token": "NO", "logprob": -0.9}, {"token": "YES", "logprob": -0.5}]}]}}]}
        with mock.patch.object(judges.urllib.request, "urlopen") as urlopen:
            urlopen.return_value = io.BytesIO(json.dumps(reply).encode())
            out = judges.make("qwen3.8_iq3_s").ask("p")
            body = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual(out["verdict"], "YES")
        self.assertGreater(out["p_yes"], 0.5)
        self.assertEqual((body["max_tokens"], body["reasoning_effort"], len(body["messages"])), (1, "none", 1))

    def test_think_variant_turns_reasoning_on_and_has_its_own_name(self):
        with mock.patch.object(judges.urllib.request, "urlopen") as urlopen:
            urlopen.return_value = io.BytesIO(json.dumps({"choices": [{"message": {"content": "YES"}}], "usage": {"completion_tokens": 300}}).encode())
            judge = judges.make("sync_m+think")
            out = judge.ask("p")
            body = json.loads(urlopen.call_args.args[0].data)
        self.assertEqual((judge.name, judges.make("sync_m").name), ("sync_m_think", "sync_m"))
        self.assertEqual(body["reasoning_effort"], "low")
        self.assertGreater(body["max_tokens"], 1000)
        self.assertEqual(out["output_tokens"], 300)

    def test_first_line_must_be_exactly_yes_or_no(self):
        self.assertEqual(self.ask("YES")[0]["verdict"], "YES")
        self.assertEqual(self.ask("NO\nbecause")[0]["verdict"], "NO")
        self.assertIsNone(self.ask("Yes, it is")[0]["verdict"])
        self.assertIsNone(self.ask(None)[0]["verdict"])

    def test_no_probability_and_server_time_is_kept(self):
        out, _ = self.ask("NO")
        self.assertIsNone(out["p_yes"])
        self.assertEqual(out["server_ms"], 320.0)


if __name__ == "__main__":
    unittest.main()
