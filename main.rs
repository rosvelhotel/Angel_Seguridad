// Cambia esta línea:
let listener = tokio::net::TcpListener::bind("127.0.0.1:8080").await.unwrap();

// Por esto:
let port = std::env::var("PORT").unwrap_or_else(|_| "8080".to_string());
let addr = format!("0.0.0.0:{}", port);
println!("Servidor en: http://{}", addr);
let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
