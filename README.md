# Web HTTP frameworks benchmarks


## Getting started

Install:

- [**Rust**](https://www.rust-lang.org/tools/install)
- [**Python**](https://www.python.org/downloads/)

    Then:
    ```
    cd flask-http-server
    pip install -r requirements.txt
    ```


## Benchmarks!

### Setup

Each requests container an `base64` image, the server is expected to send it back to the client.


### Python
#### Run Flask Web Server

```
make rust-http num_workers=1

```

#### Run Actix Web Server
```
make python-http num_workers=1
```

#### Run Benchmarks

```
make benchmarks framework=flask
```

**Note** Remember to pass the framework you are using the run the server

After a while, you'll see your results in `benchmark.csv`

