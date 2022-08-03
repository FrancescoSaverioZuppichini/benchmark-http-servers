import time
from dataclasses import dataclass
import pandas as pd
import requests
from multiprocessing.pool import ThreadPool
from pathlib import Path
from logger import logger
from typing import Callable, List
import numpy as np
import base64
import io
from PIL import Image
import os

API_URL = os.getenv("BENCHMARK_API_URL", "http://localhost:8080/infer")

# Load Image with PIL
image = Image.open("./images/blood.jpg").convert("RGB")

# Convert to JPEG Buffer
buffered = io.BytesIO()
image.save(buffered, format="JPEG")

# Base 64 Encode
img_str = base64.b64encode(buffered.getvalue())
img_str = img_str.decode("ascii")


@dataclass
class Report:
    tot_time: float
    means: List[int]
    tot_requests: int
    num_threads: int
    sleep_between_requests: float
    misses: int

    def __post_init__(self):
        means = np.array(self.means)
        self.stats = means.mean(), means.std()

    def print(self):
        mean, std = self.stats
        print("🗒️ Report:")
        print(f"\tRun {self.tot_requests} in {self.tot_time:.4f}s.")
        print(f"\t{mean:.4f}s/req (+-{std:.4f}s).")
        print(f"\t{self.misses /(self.tot_requests + 1e-5) * 100 :.2f}% misses.")

    def to_df(self, **kwargs) -> pd.DataFrame:
        mean, std = self.stats
        df = pd.DataFrame(
            data={
                "num_threads": [self.num_threads],
                "tot_requests": [self.tot_requests],
                "sleep_between": [self.sleep_between_requests],
                "tot_time(s)": [self.tot_time],
                "mean (s)": [mean],
                "std (s)": [std],
                "misses": [self.misses / self.tot_requests * 100],
                **kwargs,
            }
        )

        return df

    def to_csv(self, filepath: Path, **kwargs):
        df = self.to_df(**kwargs)
        if filepath.exists():
            old_df = pd.read_csv(filepath)
            df = pd.concat([old_df, df])
            # df = df.reset_index()
        df.to_csv(filepath, index=False)


class Benchmark:
    def __init__(
        self,
        strategy: Callable[[int], requests.Response],
        num_requests: int = 100,
        num_threads: int = 8,
        sleep_between_requests: float = 0.05,
    ):
        self.strategy = strategy
        self.num_requests = num_requests
        self.num_threads = num_threads
        self.sleep_between_requests = sleep_between_requests
        self.means = []
        self.misses = 0

    def test(self, req_id):
        time.sleep(self.sleep_between_requests)
        start = time.time()
        logger.info(f"➡️ Sending request with uid = {req_id}")
        res = self.strategy(req_id)
        try:
            elapsed = time.time() - start
            logger.info(f"⬅️ Received reply after {elapsed:.4f}s")
            self.means.append(elapsed)
        except requests.exceptions.JSONDecodeError:
            self.misses += 1
            time.sleep(5)
            logger.error("💣 Invalid answer from the server")

    def __call__(self):
        logger.info("Warmup ... ")
        for i in range(8):
            self.test(i)
            time.sleep(0.2)
        logger.info("Done ... ")
        self.means = []
        self.misses = 0
        with ThreadPool(self.num_threads) as p:
            p.map(self.test, [i for i in range(self.num_requests)])

    def make_report(self) -> Report:
        tot_time = sum(self.means)

        return Report(
            num_threads=self.num_threads,
            means=self.means,
            tot_time=tot_time,
            tot_requests=len(self.means),
            sleep_between_requests=self.sleep_between_requests,
            misses=self.misses,
        )


def send_image_strategy(req_id: int):
    res = requests.post(
        API_URL,
        data=img_str,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    print(res.status_code)


if __name__ == "__main__":
    from argparse import ArgumentParser
    import json

    parser = ArgumentParser()
    parser.add_argument("--num_requests", default=512, type=int)
    parser.add_argument("--num_threads", default=1, type=int)
    parser.add_argument("--sleep", default=0.05, type=float)
    parser.add_argument("--metadata", default="{}", type=str)

    args = parser.parse_args()

    num_requests, num_threads, sleep, metadata = (
        args.num_requests,
        args.num_threads,
        args.sleep,
        json.loads(args.metadata),
    )

    num_requests *= num_threads
    logger.info(
        f"Starting benchmark with {num_requests=}, {num_threads=}, {sleep=}, {metadata=}"
    )
    metadata = {k: [v] for k, v in metadata.items()}

    try:
        bm = Benchmark(
            send_image_strategy, num_requests, num_threads, sleep_between_requests=sleep
        )
        bm()
        report = bm.make_report()
        report.print()
        print(report.to_csv(Path("./benchmark.csv"), **metadata))
    except KeyboardInterrupt:
        bm.make_report().print()
