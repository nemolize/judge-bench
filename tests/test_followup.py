import datetime
import unittest

from judgebench import baselines, calendar_task, datasets, followup_report, langid, personal_data


class LangidTests(unittest.TestCase):
    def setUp(self):
        self.items = datasets.TASKS["langid"]()

    def test_mixed_items_follow_the_main_language_rule(self):
        for it in self.items:
            if it["cls"].startswith("mixed_"):
                self.assertEqual(langid.main_language(it["text"]), "ja" if it["label"] == 0 else "en", it["id"])

    def test_appended_items_keep_the_control_text_and_label(self):
        by_id = {i["id"]: i for i in self.items}
        appended = [i for i in self.items if i["cls"].startswith("appended_")]
        self.assertEqual(len(appended), 80)
        for it in appended:
            base = by_id[it["meta"]["base_id"]]
            self.assertTrue(it["text"].startswith(base["text"]), it["id"])
            self.assertEqual(it["label"], base["label"], it["id"])

    def test_no_sentence_is_shared_between_unrelated_classes(self):
        seen = {}
        for it in self.items:
            if it["cls"].startswith("appended_"):
                continue
            for sid in it["meta"].get("tatoeba_ids", [it["meta"].get("tatoeba_id")]):
                self.assertNotIn(sid, seen, f"{it['id']} reuses {sid} from {seen.get(sid)}")
                seen[sid] = it["id"]

    def test_baseline_marks_a_text_without_kana(self):
        flagged, _ = baselines.kana_absent([{"id": "a", "text": "Hello"}, {"id": "b", "text": "こんにちは"}])
        self.assertEqual(flagged, {"a": True, "b": False})


class FlipDirectionTests(unittest.TestCase):
    def test_flips_count_each_direction_apart(self):
        items = [{"id": "c1", "cls": "control_ja", "meta": {}}, {"id": "a1", "cls": "appended_ja", "meta": {"base_id": "c1"}},
                 {"id": "c2", "cls": "control_ja", "meta": {}}, {"id": "a2", "cls": "appended_ja", "meta": {"base_id": "c2"}}]
        res = {"c1": {"verdict": "NO"}, "a1": {"verdict": "YES"}, "c2": {"verdict": "YES"}, "a2": {"verdict": "NO"}}
        self.assertEqual(followup_report.flips(items, res, "appended_ja"), {"n": 2, "to_yes": 1, "to_no": 1})


class PersonalDataTests(unittest.TestCase):
    def test_my_number_check_digit_matches_a_published_sample(self):
        self.assertTrue(personal_data.valid_my_number("123456789018"))
        self.assertFalse(personal_data.valid_my_number("123456789019"))

    def test_labels_agree_with_the_check_digit_rule(self):
        for it in datasets.TASKS["personal_data"]():
            if it["cls"] == "my_number_valid":
                self.assertTrue(personal_data.valid_my_number(it["meta"]["value"].replace(" ", "")))
            if it["cls"] == "neg_my_number_invalid":
                self.assertFalse(personal_data.valid_my_number(it["meta"]["value"].replace(" ", "")))

    def test_values_are_unique_and_use_reserved_shapes(self):
        items = datasets.TASKS["personal_data"]()
        values = [it["meta"]["value"] for it in items]
        self.assertEqual(len(values), len(set(values)))
        for it in items:
            if "@" in it["meta"]["value"]:
                self.assertRegex(it["meta"]["value"], r"@example\.(com|org|net)$")
            if it["cls"] == "mobile_number":
                self.assertRegex(it["meta"]["value"], r"^0[789]0-0000-\d{4}$")


class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.items = datasets.TASKS["calendar"]()

    def test_truth_is_recomputed_from_the_text(self):
        for it in self.items:
            self.assertEqual(calendar_task.consistent(it["text"]), it["label"] == 0, it["id"])

    def test_every_inconsistent_item_has_a_consistent_twin(self):
        pairs = {}
        for it in self.items:
            pairs.setdefault(it["meta"]["pair_id"], set()).add(it["label"])
        self.assertTrue(all(v == {0, 1} for v in pairs.values()))

    def test_era_table_and_weekdays_against_known_dates(self):
        self.assertEqual(calendar_task.era_to_year("令和", 7), 2025)
        self.assertEqual(calendar_task.era_to_year("昭和", 50), 1975)
        self.assertEqual(calendar_task.weekday_name(2026, 11, 28), "土")
        self.assertEqual(datetime.date(2026, 11, 28).strftime("%A"), "Saturday")

    def test_tax_is_rounded_down(self):
        self.assertEqual(calendar_task.invoice_consistent([(1255, 1)]), (1255, 125, 1380))

    def test_no_dated_statement_precedes_the_gregorian_calendar(self):
        for it in self.items:
            if it["cls"] in ("era_year", "neg_era_year"):
                self.assertGreaterEqual(calendar_task.era_to_year(it["meta"]["era"], it["meta"]["era_year"]), calendar_task.GREGORIAN_FROM, it["id"])

    def test_no_era_year_sits_in_a_changeover_year(self):
        last = {e: n for e, _, n in calendar_task.ERAS}
        for it in self.items:
            if it["cls"] in ("era_year", "neg_era_year"):
                self.assertNotIn(it["meta"]["era_year"], (1, last[it["meta"]["era"]]), it["id"])


if __name__ == "__main__":
    unittest.main()
