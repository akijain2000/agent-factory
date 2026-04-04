#!/usr/bin/env python3
"""
generate-charts.py — Generate visualization charts from autoresearch grading data.

Usage: python outputs/charts/generate-charts.py [--data-dir raw/datasets/] [--output-dir outputs/charts/]

Generates:
  1. Radar chart: 8 AGENT_SPEC dimensions for top/bottom/mean agents
  2. Bar chart: wave-by-wave score improvements (delta)
  3. Heatmap: agent x dimension scores
  4. Delta chart: before/after progression per agent

Requires: matplotlib, numpy (pip install matplotlib numpy)
"""

import json
import csv
import os
import sys
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import numpy as np
except ImportError:
    print("Error: matplotlib and numpy required. Install with:")
    print("  pip install matplotlib numpy")
    sys.exit(1)


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def load_csv(path: str) -> list[dict]:
    with open(path) as f:
        return list(csv.DictReader(f))


def chart_radar(data: dict, output_dir: str):
    """Radar chart: 8 AGENT_SPEC dimensions for best, worst, and mean agents."""
    dims = data["dimensions"]["agent_spec"]
    agents = data["agents"]

    scores = [a["agent_spec"] for a in agents]
    means = [sum(col) / len(col) for col in zip(*scores)]

    best = max(agents, key=lambda a: a["agent_spec_mean"])
    worst = min(agents, key=lambda a: a["agent_spec_mean"])

    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for label, values, color, ls in [
        (f"Best: {best['id']}", best["agent_spec"], "#2ecc71", "-"),
        (f"Worst: {worst['id']}", worst["agent_spec"], "#e74c3c", "--"),
        ("Mean (all 20)", means, "#3498db", "-."),
    ]:
        vals = values + values[:1]
        ax.plot(angles, vals, color=color, linewidth=2, linestyle=ls, label=label)
        ax.fill(angles, vals, color=color, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims, fontsize=10)
    ax.set_ylim(8, 10)
    ax.set_title("AGENT_SPEC Dimensions — Radar", fontsize=14, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "radar-agent-spec.png"), dpi=150)
    plt.close()
    print("  Generated: radar-agent-spec.png")


def chart_wave_bars(data: dict, output_dir: str):
    """Bar chart: wave-by-wave score improvements."""
    waves = data["wave_improvements"]

    dims = [w["dimension"] for w in waves]
    deltas = [w["delta"] for w in waves]
    befores = [w["before"] for w in waves]

    x = np.arange(len(dims))
    width = 0.6

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(x, deltas, width, bottom=befores, color="#2ecc71", label="Improvement")
    ax.bar(x, befores, width, color="#95a5a6", alpha=0.5, label="Before")

    for bar, delta in zip(bars, deltas):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_y() + bar.get_height() + 0.1,
            f"+{delta}",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10,
        )

    ax.set_ylabel("Score (0-10)")
    ax.set_title("Wave-by-Wave Score Improvements", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(dims, rotation=30, ha="right")
    ax.set_ylim(0, 10.5)
    ax.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "wave-improvements.png"), dpi=150)
    plt.close()
    print("  Generated: wave-improvements.png")


def chart_heatmap(data: dict, output_dir: str):
    """Heatmap: agent x dimension scores."""
    dims = data["dimensions"]["agent_spec"]
    agents = data["agents"]

    matrix = np.array([a["agent_spec"] for a in agents])
    labels = [a["id"].split("-", 1)[1] for a in agents]

    fig, ax = plt.subplots(figsize=(12, 10))
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#e74c3c", "#f39c12", "#2ecc71"])
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=8.5, vmax=10)

    ax.set_xticks(np.arange(len(dims)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(dims, fontsize=9)
    ax.set_yticklabels(labels, fontsize=8)

    for i in range(len(labels)):
        for j in range(len(dims)):
            ax.text(j, i, f"{matrix[i, j]:.1f}", ha="center", va="center", fontsize=8)

    ax.set_title("Agent x Dimension Heatmap", fontsize=14)
    fig.colorbar(im, ax=ax, shrink=0.6)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "heatmap-scores.png"), dpi=150)
    plt.close()
    print("  Generated: heatmap-scores.png")


def chart_delta(data: dict, output_dir: str):
    """Horizontal bar chart: before/after progression per agent."""
    progression = data["progression"]

    labels = [p["id"].split("-", 1)[1] for p in progression]
    cycle5 = [p["cycle5"] for p in progression]
    final = [p["final"] for p in progression]

    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(10, 12))
    ax.barh(y, cycle5, color="#95a5a6", alpha=0.7, label="Cycle 5")
    ax.barh(y, final, color="#2ecc71", alpha=0.5, label="Final")

    for i, (c5, fn) in enumerate(zip(cycle5, final)):
        ax.text(fn + 0.02, i, f"+{fn - c5:.1f}", va="center", fontsize=8, color="#27ae60")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("AGENT_SPEC Mean Score")
    ax.set_title("Agent Score Progression: Cycle 5 → Final", fontsize=14)
    ax.set_xlim(7, 10)
    ax.legend()
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "delta-progression.png"), dpi=150)
    plt.close()
    print("  Generated: delta-progression.png")


def main():
    data_dir = "raw/datasets"
    output_dir = "outputs/charts"

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--data-dir" and i < len(sys.argv) - 1:
            data_dir = sys.argv[i + 1]
        if arg == "--output-dir" and i < len(sys.argv) - 1:
            output_dir = sys.argv[i + 1]

    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(data_dir, "autoresearch-scores.json")
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        sys.exit(1)

    data = load_json(json_path)

    print(f"\nGenerating charts from {json_path}...\n")
    chart_radar(data, output_dir)
    chart_wave_bars(data, output_dir)
    chart_heatmap(data, output_dir)
    chart_delta(data, output_dir)
    print(f"\nAll charts saved to {output_dir}/\n")


if __name__ == "__main__":
    main()
