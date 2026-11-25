import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from judgebench import datasets, private_setup, report, run

POSITIVE_CLASSES = {"ram", "free_disk", "local_tool_or_hook"}
NEGATIVE_GROUPS = {"neg_ordinary", "neg_vendor_figure", "neg_repro_line"}

FILE_SUFFIXES = {"toml", "yaml", "yml", "json", "sock", "md", "py", "lock", "txt", "cfg", "sh"}
DUMMY_TLDS = {"example", "test", "invalid"}
HOST_LIKE = re.compile(r"(?<![\w/$~.-])[A-Za-z0-9][\w-]*(?:\.[A-Za-z0-9][\w-]*)+(?![\w-])")
PATH_LIKE = re.compile(r"(?<![\w$])(?:/[\w.-]+){2,}|~/[\w.-]+|[A-Za-z]:\\\S+")
DUMMY_HOME = "/home/example-user/"


def non_dummy_tokens(text):
    """Every host-like or path-like token in `text` that is not in the dummy pools (case-insensitive)."""
    hosts = [t for t in HOST_LIKE.findall(text)
             if not t.rsplit(".", 1)[1].isdigit() and t.rsplit(".", 1)[1].lower() not in FILE_SUFFIXES | DUMMY_TLDS]
    paths = [t for t in PATH_LIKE.findall(text) if not t.lower().startswith(DUMMY_HOME)]
    return hosts + paths


def reason_of(text):
    return next((n for needs in private_setup.NEEDS.values() for n in needs if text.startswith(n[1])), None)


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
            self.assertEqual(non_dummy_tokens(it["text"]), [], it["text"])

    def test_the_dummy_check_rejects_real_looking_hosts_and_paths(self):
        for text in ["on O2.local", "Devbox.Corp.COM", "host.example.jp", "build.mycorp.co", "/root/.cache", "/var/folders/x/y", "~/projects",
                     "/Users/someone/work", "C:\\Users\\x"]:
            self.assertTrue(non_dummy_tokens(text), text)
        for text in ["devbox-1.example", "api.example.test", "/home/example-user/.config/git", "see config.toml", "a.b.invalid"]:
            self.assertEqual(non_dummy_tokens(text), [], text)

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
            reason = reason_of(neg["text"])
            self.assertTrue(pos["text"].endswith(neg["text"][len(reason[1]) + 1:]), pid)

    def test_a_reproducibility_line_states_a_reason_that_fits_its_value(self):
        implicit = 0
        for it in self.items:
            if it["cls"] != "neg_repro_line":
                continue
            reason = reason_of(it["text"])
            self.assertIsNotNone(reason, it["text"])
            implicit += reason[0] == "implicit"
            lo, hi = reason[2]
            value = int(re.search(r"(\d+) GB", it["text"][len(reason[1]):]).group(1)) if lo or hi else None
            if value is not None:
                self.assertTrue((lo is None or value >= lo) and (hi is None or value <= hi), it["text"])
        self.assertEqual(implicit, 3 * (private_setup.PAIRED // 3))

    def test_a_tool_reason_fits_the_hook_and_tool_it_is_paired_with(self):
        for it in self.items:
            if it["cls"] != "neg_repro_line":
                continue
            reason = reason_of(it["text"])
            disclosure = it["text"][len(reason[1]) + 1:]
            if "push" in reason[1]:
                self.assertIn("pre-push", disclosure, it["text"])
            if "commit messages" in reason[1]:
                self.assertIn("commit-msg", disclosure, it["text"])
            if "watcher" in reason[1]:
                self.assertNotRegex(disclosure, r"tmux|direnv", it["text"])

    def test_a_scarcity_wording_never_carries_a_large_value(self):
        scarce = re.compile(r"only has|only have|down to|is at|nearly full|kept the examples small|trimmed the fixtures|did not clone")
        for it in self.items:
            if scarce.search(it["text"]):
                for number in re.findall(r"(\d+) GB", it["text"]):
                    self.assertLessEqual(int(number), 22, it["text"])

    def test_a_reproducibility_line_never_carries_a_hostname_or_home_path(self):
        for it in self.items:
            if it["cls"] == "neg_repro_line":
                self.assertNotRegex(it["text"], r"devbox-|/home/|\.example\b", it["text"])

    def test_formatter_and_commit_message_reasons_get_a_matching_tool(self):
        for it in self.items:
            if it["cls"] != "neg_repro_line":
                continue
            reason = reason_of(it["text"])[1]
            disclosure = it["text"][len(reason) + 1:]
            if "formatter" in reason or "commit messages" in reason or "formatter" in reason or "rewrites files" in reason:
                self.assertNotRegex(disclosure, r"tmux|direnv", it["text"])

    def test_ordinary_defaults_name_no_concrete_home_directory(self):
        for it in self.items:
            if it["cls"] == "neg_ordinary":
                self.assertNotIn("/home/", it["text"])

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

    def test_error_rate_counts_no_answers_and_errors_on_both_sides(self):
        items = [{"id": f"x{i}", "cls": "ram" if i < 45 else "neg", "label": int(i < 45)} for i in range(90)]
        res = {it["id"]: {"verdict": "YES", "error": None} for it in items}
        for i in (0, 1, 2, 50, 51):
            res[f"x{i}"] = {"verdict": None, "error": "boom"}
        for i in (3, 52):
            res[f"x{i}"] = {"verdict": None, "error": None}
        s = report.score(items, res)
        task_err = sum(c["err"] for c in s["pos"].values()) + s["neg"]["err"]
        task_items = sum(c["n"] for c in s["pos"].values()) + s["neg"]["n"] + s["neg"]["noans"] + s["neg"]["err"]
        self.assertEqual((task_err, task_items), (5, 90))

    def test_the_rules_apply_to_the_new_task_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            items = [{"id": f"t-{i}", "cls": "ram", "label": 1} for i in range(10)] + [{"id": f"t-n{i}", "cls": "neg", "label": 0} for i in range(10)]
            res = [{"id": it["id"], "verdict": "YES", "p_yes": None} for it in items]
            Path(tmp, "j__t.jsonl").write_text("\n".join(json.dumps(r) for r in res))
            Path(tmp, "baseline__t.jsonl").write_text("\n".join(json.dumps({**r, "verdict": "NO"}) for r in res))
            rows = {}
            for task in ("private_setup", "honorific"):
                with mock.patch.object(report, "RESULTS", Path(tmp)), mock.patch.object(report.datasets, "load", return_value=items), \
                        mock.patch.object(report, "JUDGES", ["baseline", "j"]), \
                        mock.patch.object(report, "load_results", lambda j, t: {r["id"]: r for r in map(json.loads, Path(tmp, f"{j}__t.jsonl").read_text().splitlines())}):
                    rows[task] = "\n".join(report.task_table(task, {}))
        self.assertIn("not measurable", rows["private_setup"])
        self.assertNotIn("not measurable", rows["honorific"])


class JudgeRunTests(unittest.TestCase):
    def test_probe_tasks_follow_the_tasks_asked(self):
        self.assertEqual(run.probe_tasks(["private_setup"]), ["private_setup"])
        self.assertEqual(run.probe_tasks(["honorific", "aitext"]), ["honorific"])
        self.assertEqual(run.probe_tasks([]), ["honorific", "private_setup"])
        self.assertEqual(run.probe_tasks(["secrets"]), [])

    def test_a_run_without_honorific_keeps_the_stored_loaded_size(self):
        class Local:
            name = "fake"

            def ask(self, prompt):
                return {"verdict": "NO", "p_yes": None, "latency_s": 0.1}

            def loaded_bytes(self):
                return 456

        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "fake__meta.json").write_text(json.dumps({"loaded_bytes": 123}))
            item = {"id": "t-1", "task": "private_setup", "cls": "ram", "label": 1, "text": "x", "meta": {}}
            with mock.patch.object(run, "RESULTS", Path(tmp)), mock.patch.object(run.judges, "make", return_value=Local()), \
                    mock.patch.object(run.datasets, "load", return_value=[item]):
                run.run_judge("fake", ["private_setup"])
            self.assertEqual(json.loads(Path(tmp, "fake__meta.json").read_text())["loaded_bytes"], 123)

    def test_an_unreachable_judge_stops_before_writing_anything(self):
        class Down:
            name = "down"

            def ask(self, prompt):
                raise OSError("connection refused")

            def loaded_bytes(self):
                return None

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(run, "RESULTS", Path(tmp)), mock.patch.object(run.judges, "make", return_value=Down()):
                with self.assertRaises(RuntimeError):
                    run.run_judge("down", ["private_setup"])
            self.assertEqual(list(Path(tmp).iterdir()), [])


class LatencyProbeTests(unittest.TestCase):
    def test_a_probe_with_no_successful_call_keeps_the_stored_latency(self):
        class Down:
            name = "fake"

            def ask(self, prompt):
                raise OSError("down")

        with tempfile.TemporaryDirectory() as tmp:
            stored = {"sequential_latency_by_task": {"private_setup": [0.5]}}
            Path(tmp, "fake__meta.json").write_text(json.dumps(stored))
            with mock.patch.object(run, "RESULTS", Path(tmp)), mock.patch.object(run.judges, "make", return_value=Down()):
                run.run_latency_probe("fake", "private_setup")
            self.assertEqual(json.loads(Path(tmp, "fake__meta.json").read_text()), stored)


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
