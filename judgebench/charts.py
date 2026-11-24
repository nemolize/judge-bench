"""Draw the three charts of the article from results/: detection rate, false-alarm rate, flip rate under an added instruction.

The rows are the judges the article shows; `gemma4_26b`, `gemma4_26b_think` and `claude_haiku` are in the report but not charted.

  pip install matplotlib
  python3 -m judgebench.charts <output dir>
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from . import datasets
from .report import MEASURABLE_FLIPS, injection_flips, load_results, score

matplotlib.rcParams["font.family"] = ["Hiragino Sans", "Noto Sans CJK JP", "sans-serif"]

GROUPS = [
    [("baseline", "機械的判定")],
    [("claude_api_think", "claude-haiku（thinking あり）"), ("claude_api_off", "claude-haiku（thinking なし）"),
     ("gemini_flash", "gemini-3.7-flash（thinking あり）")],
    [("gemma4_12b", "gemma4:12b"), ("gemma4_12b_think", "gemma4:12b（thinking あり）"), ("gemma4_31b", "gemma4:31b"),
     ("qwen3.5_27b", "qwen3.5:27b"), ("sync_m_think", "Qwen3.8 Sync-M（thinking あり）"), ("qwen3.8_iq3_s", "Qwen3.8 IQ3_S"),
     ("qwen3.8_iq3_s_think", "Qwen3.8 IQ3_S（thinking あり）")],
    [("jev", "jev"), ("gpt_6_luna", "gpt-6-luna"), ("gemini_decision", "gemini-decision-1"), ("clef", "clef（27B）"),
     ("clef_flash", "clef-flash")],
]
DETECT_COLUMNS = [("二重敬語", "honorific", "double_honorific"), ("謙譲→相手", "honorific", "humble_for_other"),
                  ("尊敬→自分", "honorific", "honorific_for_self"), ("です・ます", "style", "mixed_register"),
                  ("全角混在", "style", "width"), ("用語不統一", "style", "term_variant"), ("秘密情報", "secrets", None),
                  ("AI 文", "aitext", None)]
FALSE_ALARM_COLUMNS = [("敬語", "honorific"), ("文体", "style"), ("秘密情報", "secrets"), ("AI 文", "aitext")]
INJECTION_COLUMNS = [(f"{tl}・{al}", task, attack) for tl, task in (("敬語", "honorific"), ("秘密", "secrets"))
                     for al, attack in (("直接", "direct"), ("権威", "authority"), ("偽の正解", "fake_answer"))]
UNJUDGEABLE_SHARE = 0.5  # a cell is "－" when at least this share of its items got no answer
BLUE, ORANGE, RED = (0x1F, 0x5B, 0xB5), (0xD6, 0x7A, 0x45), (0xC4, 0x28, 0x1F)


def mix(color, share):
    return tuple((255 - (255 - c) * (0.08 + 0.92 * share)) / 255 for c in color)


def detect_cell(judge, task, cls):
    res = load_results(judge, task)
    if res is None:
        return None, ""
    s = score(datasets.load(task), res)
    pos = list(s["pos"].values()) if cls is None else [s["pos"][cls]]
    n, caught, noans = (sum(c[k] for c in pos) for k in ("n", "caught", "noans"))
    return (None if n == 0 or noans / n >= UNJUDGEABLE_SHARE else caught / n), ""


def false_alarm_cell(judge, task):
    res = load_results(judge, task)
    if res is None or detect_cell(judge, task, None)[0] is None:
        return None, ""
    neg = score(datasets.load(task), res)["neg"]
    answered, noans = neg["n"], neg["noans"]
    if answered == 0 or noans / (answered + noans) >= UNJUDGEABLE_SHARE:
        return None, ""
    return neg["flagged"] / answered, ""


def injection_cell(judge, task, attack):
    base, res = load_results(judge, task), load_results(judge, "injection_" + task)
    if base is None or res is None:
        return None, ""
    flips, n = injection_flips(datasets.load("injection_" + task), base, res, attack)
    if n <= 1:
        return None, ""
    return flips / n, "*" if n < MEASURABLE_FLIPS else ""


def draw(path, title, columns, cell, color, note, col_width):
    rows = [(label, g, judge) for g, group in enumerate(GROUPS) for judge, label in group]
    cw, ch, gap, left, top = col_width, 0.58, 0.05, 4.7, 1.25
    gap_group = 0.22
    ys, y, prev = [], top, 0
    for _, g, _ in rows:
        y += gap_group if g != prev else 0
        prev = g
        ys.append(y)
        y += ch + gap
    width, height = left + cw * len(columns) + 0.4, y + 0.9
    fig = plt.figure(figsize=(width, height), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.axis("off")
    ax.text(0.4, 0.55, title, fontsize=17, fontweight="bold", va="center", color="#222222")
    for j, (label, *_) in enumerate(columns):
        ax.text(left + cw * j + cw / 2, top - 0.3, label, ha="center", va="center", fontsize=13, color="#222222")
    for (label, _, judge), y in zip(rows, ys):
        ax.text(left - 0.15, y + ch / 2, label, ha="right", va="center", fontsize=13, color="#222222")
        for j, spec in enumerate(columns):
            value, star = cell(judge, *spec[1:])
            x = left + cw * j
            if value is None:
                ax.add_patch(Rectangle((x + gap / 2, y), cw - gap, ch, color="#eeeeee", lw=0))
                ax.text(x + cw / 2, y + ch / 2, "－", ha="center", va="center", fontsize=13, color="#777777")
                continue
            ax.add_patch(Rectangle((x + gap / 2, y), cw - gap, ch, color=mix(color, value), lw=0))
            ax.text(x + cw / 2, y + ch / 2, f"{value:.0%}" + star, ha="center", va="center", fontsize=13,
                    color="white" if value >= 0.5 else "#222222")
    ax.text(0.4, height - 0.4, note, fontsize=10.5, va="center", color="#666666")
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    note_missing = "― は未測定、または答えが出ない件が多く評価できないもの。"
    draw(out / "detect-heatmap.png", "検出率（誤りを含む文に YES を返した割合）", DETECT_COLUMNS,
         lambda j, t, c: detect_cell(j, t, c), BLUE, "高いほど良い。AI 文の「機械的判定」は定型句リスト。" + note_missing, 1.42)
    draw(out / "false-alarm-heatmap.png", "誤警報率（正しい文に YES を返した割合）", FALSE_ALARM_COLUMNS,
         lambda j, t: false_alarm_cell(j, t), ORANGE, "低いほど良い。AI 文の「機械的判定」は定型句リスト。" + note_missing, 2.3)
    draw(out / "injection.png", "指示を足すと判定が YES から変わった割合", INJECTION_COLUMNS,
         lambda j, t, a: injection_cell(j, t, a), RED,
         f"低いほど耐性がある。* は元が YES の項目が {MEASURABLE_FLIPS} 件未満の参考値。― は元が YES の項目が 0〜1 件で比較できない。", 1.95)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
