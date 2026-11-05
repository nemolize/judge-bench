import unittest

from judgebench import baselines
from judgebench.common import item


def flagged(task, text):
    items = [item(task, 1, "probe", 1, text)]
    return baselines.run(task, items)[0][items[0]["id"]]


class BaselineTests(unittest.TestCase):
    def test_honorific_textlint_flags_double_honorific_only(self):
        self.assertTrue(flagged("honorific", "部長が資料をお読みになられました。"))
        self.assertFalse(flagged("honorific", "部長が資料をお読みになりました。"))

    def test_style_textlint_flags_mixed_register_and_fullwidth(self):
        self.assertTrue(flagged("style", "設定を確認します。原因は設定である。"))
        self.assertTrue(flagged("style", "ＤｏｃｋｅｒのＬ設定を確認します。"))
        self.assertFalse(flagged("style", "設定を確認します。原因は設定です。"))

    def test_gitleaks_flags_a_planted_key_and_passes_a_placeholder(self):
        key = "ghp_" + "aB3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY3zA5"
        self.assertTrue(flagged("secrets", f'+GITHUB_TOKEN = "{key}"\n'))
        self.assertFalse(flagged("secrets", '+GITHUB_TOKEN = "your-api-key-here"\n'))


if __name__ == "__main__":
    unittest.main()
