import unittest

from judgebench import datasets
from judgebench.common import digest, positives_per_class

FLOOR = 40


class DatasetTests(unittest.TestCase):
    def test_deterministic_for_fixed_seed(self):
        for task, build in datasets.TASKS.items():
            self.assertEqual(digest(build()), digest(build()), task)

    def test_positive_floor_per_class(self):
        for task, build in datasets.TASKS.items():
            counts = positives_per_class(build())
            self.assertTrue(counts, task)
            for cls, n in counts.items():
                self.assertGreaterEqual(n, FLOOR, f"{task}/{cls}")

    def test_ids_unique_and_labels_binary(self):
        for task, build in datasets.TASKS.items():
            items = build()
            self.assertEqual(len({i["id"] for i in items}), len(items), task)
            self.assertTrue(all(i["label"] in (0, 1) for i in items), task)

    def test_injection_items_keep_the_base_text(self):
        items = datasets.TASKS["injection_honorific"]()
        base = {i["id"]: i for i in datasets.TASKS["honorific"]()}
        for it in items:
            self.assertTrue(it["text"].startswith(base[it["meta"]["base_id"]]["text"]))


if __name__ == "__main__":
    unittest.main()
