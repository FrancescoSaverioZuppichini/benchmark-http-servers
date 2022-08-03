use actix_web::{get, post, web, App, Error, HttpRequest, HttpResponse, HttpServer, Responder};
use std::{
    fs::OpenOptions,
    io::{self, Write}, env,
};
#[get("/hello/{name}")]
async fn greet(name: web::Path<String>) -> impl Responder {
    format!("Hello {name}!")
}

#[get("/ping")]
async fn pong() -> impl Responder {
    HttpResponse::Ok().body("pong")
}

#[post("/infer")]
async fn infer(body: web::Bytes) -> Result<HttpResponse, Error> {
    Ok(HttpResponse::Ok().body(body))
}

#[actix_web::main] // or #[tokio::main]
async fn main() -> std::io::Result<()> {
    let num_workers: usize = env::var("NUM_WORKERS").unwrap_or(String::from("1")).parse::<usize>().unwrap();
    println!("Starting server with {} workers 🚀", num_workers);
    HttpServer::new(|| App::new().service(greet).service(pong).service(infer))
        .workers(num_workers)
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}
