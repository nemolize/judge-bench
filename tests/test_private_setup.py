import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from judgebench import datasets, private_setup, report, run

POSITIVE_CLASSES = {"ram", "free_disk", "local_tool_or_hook"}
NEGATIVE_GROUPS = {"neg_ordinary", "neg_vendor_figure", "neg_repro_line"}

NON_DUMMY_HOSTNAME = re.compile(r"(?<![\w/.-])[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|net|org|io|dev|app|local|lan|internal|home|corp)\b")
ANY_HOME_PATH = re.compile(r"(?:/home/|/Users/|[A-Z]:\\Users\\)([\w.-]+)")


class PrivateSetupDatasetTests(unittest.TestCase):
    items = private_setup.generate()

    def test_sizes_and_groups(self):
        self.assertEqual(len(self.items), 270)
        counts = {}
        for it in self.items:
            counts[it["cls"]] = counts.get(it["cls"], 0) + 1
        self.assertEqual(counts, {c: 45 for c in POSITIVE_CLASSES | NEGATIVE_GROUPS})
        self.assertTrue(all((it["label"] == 1) == (it["cls"] in POSITIVE_CLASSES) for it in self.items))

    def test_texts_are_unique_english_and_tagged(self):
        self.assertEqual(len({it["text"] for it in self.items}), len(self.items))
        self.assertTrue(all(it["meta"]["lang"] == "en" and it["meta"]["source_kind"] for it in self.items))

    def test_every_hostname_and_path_is_dummy(self):
        for it in self.items:
            self.assertIsNone(NON_DUMMY_HOSTNAME.search(it["text"]), it["text"])
            for user in ANY_HOME_PATH.findall(it["text"]):
                self.assertEqual(user, "example-user", it["text"])

    def test_pairs_share_the_disclosure_and_differ_in_label(self):
        pairs = {}
        for it in self.items:
            if it["meta"].get("pair_id"):
                pairs.setdefault(it["meta"]["pair_id"], []).append(it)
        self.assertEqual(len(pairs), 3 * private_setup.PAIRED)
        for pid, members in pairs.items():
            self.assertEqual(sorted(m["label"] for m in members), [0, 1], pid)
            pos, neg = sorted(members, key=lambda m: -m["label"])
            self.assertEqual(neg["cls"], "neg_repro_line")
            self.assertTrue(pos["text"].endswith(neg["text"].split(": ", 1)[1]), pid)

    def test_a_reproducibility_line_states_its_reason(self):
        for it in self.items:
            if it["cls"] == "neg_repro_line":
                self.assertTrue(any(it["text"].startswith(n) for needs in private_setup.NEEDS.values() for n in needs), it["text"])

    def test_registered_with_its_prompt(self):
        self.assertIn("private_setup", datasets.TASKS)
        prompt = datasets.prompt_for("private_setup", "Hello.")
        self.assertIn("Hello.", prompt)
        self.assertNotIn("{text}", prompt)


class PrivateSetupBaselineTests(unittest.TestCase):
    def flagged(self, text):
        from judgebench import baselines
        it = {"id": "x", "text": text}
        return baselines.run("private_setup", [it])[0]["x"]

    def test_flags_a_machine_size_a_free_disk_a_hook_and_a_home_path(self):
        for text in ["My laptop has 48 GB of RAM.", "I only have 35 GB free on my workstation.",
                     "I run fmtbot as a pre-push hook.", "A hook in /home/example-user/.config/git/hooks runs it."]:
            self.assertTrue(self.flagged(text), text)

    def test_passes_a_vendor_figure_and_an_ordinary_post(self):
        for text in ["The Aurora X2 supports up to 128 GB of unified memory.", "This PR fixes a broken link in the guide."]:
            self.assertFalse(self.flagged(text), text)


class NotMeasurableTests(unittest.TestCase):
    def test_floor_and_error_rate(self):
        ok = {"n": 45, "err": 0}
        self.assertTrue(report.measurable(ok, 0, 270))
        self.assertFalse(report.measurable({"n": 45, "err": 6}, 6, 270))
        self.assertFalse(report.measurable(ok, 14, 270))
        self.assertTrue(report.measurable(ok, 13, 270))

    def test_only_new_tasks_are_held_to_it(self):
        self.assertEqual(report.RULES_ENFORCED, {"private_setup"})


class LatencyProbeTests(unittest.TestCase):
    def test_probe_stores_per_task_latency(self):
        class Judge:
            name = "fake"
            hosted = True

            def ask(self, prompt):
                return {"verdict": "NO", "p_yes": None, "latency_s": 0.5}

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(run, "RESULTS", Path(tmp)), mock.patch.object(run.judges, "make", return_value=Judge()):
                run.run_latency_probe("fake", "private_setup")
            meta = json.loads((Path(tmp) / "fake__meta.json").read_text())
        self.assertEqual(len(meta["sequential_latency_by_task"]["private_setup"]), run.LATENCY_PROBE)
        self.assertNotIn("sequential_latency_s", meta)


if __name__ == "__main__":
    unittest.main()
