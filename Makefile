export NUM_WORKERS=$(num_workers)

rust-http:
	cd actix-http-server && cargo run --release

python-http:
	cd flask-http-server && gunicorn --bind 0.0.0.0:8080 --workers=${NUM_WORKERS} app:app	

benchmarks:
	./run_benchmarks.sh ${framework}