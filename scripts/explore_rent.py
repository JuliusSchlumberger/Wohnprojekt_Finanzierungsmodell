"""Sample the required rent over model.exploration.PARAMETERS and write the page data.

Usage: python scripts/explore_rent.py [--n 1000000] [--seed 7] [--workers 0] [--out PATH]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from model.exploration import explore, latin_hypercube, summarize  # noqa: E402
from model.presets import ProjectInputs  # noqa: E402

DEFAULT_OUT = ROOT / "app" / "data" / "exploration.json"
CHUNK = 5_000

log = logging.getLogger("explore_rent")


def _explore_chunk(draws: pd.DataFrame) -> pd.DataFrame:
    return explore(ProjectInputs(), draws)


def _json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"not JSON serialisable: {type(value).__name__}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=1_000_000, help="number of sampled variants")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--workers", type=int, default=0, help="processes; 0 = all cores")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    draws = latin_hypercube(args.n, args.seed)
    chunks = [draws.iloc[i : i + CHUNK] for i in range(0, args.n, CHUNK)]
    workers = args.workers or os.cpu_count() or 1
    start = time.perf_counter()
    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for i, result in enumerate(pool.map(_explore_chunk, chunks), start=1):
            results.append(result)
            if i % 20 == 0 or i == len(chunks):
                log.info("%d/%d chunks, %.0f s", i, len(chunks), time.perf_counter() - start)
    samples = pd.concat(results)
    summary = summarize(ProjectInputs(), samples, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(summary, default=_json_default, separators=(",", ":")), encoding="utf-8"
    )
    log.info("wrote %s (%.0f kB)", args.out, args.out.stat().st_size / 1e3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
