#!/bin/bash
python benchmark.py --sleep=0.033 --num_threads=1 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.033 --num_threads=2 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.033 --num_threads=4 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.033 --num_threads=8 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.005 --num_threads=1 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.005 --num_threads=2 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.005 --num_threads=4 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'
python benchmark.py --sleep=0.005 --num_threads=8 --metadata='{"server_workers":"'"$NUM_WORKERS"'", "framework":"'"$1"'"}'