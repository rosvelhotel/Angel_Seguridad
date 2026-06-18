use std::sync::Arc;
use tokio::sync::Mutex;
use chrono::Local;
use axum::{
    Router,
    routing::get,
    routing::post,
    Json,
    extract::State,
    response::Html,
};
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Log {
    pub id: u64,
    pub timestamp: String,
    pub ip: String,
    pub mensaje: String,
    pub categoria: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct Stats {
    pub total_logs: usize,
    pub criticos: usize,
    pub sospechosos: usize,
    pub seguros: usize,
}

pub struct MotorOnion {
    logs: Vec<Log>,
}

impl MotorOnion {
    pub fn new() -> Self {
        Self { logs: Vec::new() }
    }

    pub fn agregar_log(&mut self, ip: &str, mensaje: &str, categoria: &str) {
        let id = self.logs.len() as u64;
        let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
        self.logs.push(Log {
            id,
            timestamp,
            ip: ip.to_string(),
            mensaje: mensaje.to_string(),
            categoria: categoria.to_string(),
        });
        println!("[LOG] Recibido: {} - {}", ip, mensaje);
    }

    pub fn obtener_logs(&self, limit: usize) -> Vec<Log> {
        self.logs.iter().rev().take(limit).cloned().collect()
    }

    pub fn obtener_stats(&self) -> Stats {
        let mut criticos = 0;
        let mut sospechosos = 0;
        let mut seguros = 0;
        
        for log in &self.logs {
            match log.categoria.as_str() {
                "CRITICO" => criticos += 1,
                "SOSPECHOSO" => sospechosos += 1,
                _ => seguros += 1,
            }
        }
        
        Stats {
            total_logs: self.logs.len(),
            criticos,
            sospechosos,
            seguros,
        }
    }
}

type SharedMotor = Arc<Mutex<MotorOnion>>;

async fn handler_index() -> Html<String> {
    match std::fs::read_to_string("web/index.html") {
        Ok(content) => {
            println!("[OK] Dashboard cargado");
            Html(content)
        }
        Err(e) => {
            println!("[ERROR] No se pudo cargar web/index.html: {}", e);
            Html(format!("<h1>Error</h1><p>web/index.html no encontrado</p><p>Ruta actual: {:?}</p>", std::env::current_dir()))
        }
    }
}

async fn handler_logs(State(motor): State<SharedMotor>) -> Json<Vec<Log>> {
    let motor = motor.lock().await;
    Json(motor.obtener_logs(100))
}

async fn handler_stats(State(motor): State<SharedMotor>) -> Json<Stats> {
    let motor = motor.lock().await;
    Json(motor.obtener_stats())
}

async fn handler_post_log(
    State(motor): State<SharedMotor>,
    Json(payload): Json<serde_json::Value>,
) -> &'static str {
    let ip = payload.get("ip").and_then(|v| v.as_str()).unwrap_or("SISTEMA");
    let mensaje = payload.get("mensaje").and_then(|v| v.as_str()).unwrap_or("");
    let categoria = payload.get("categoria").and_then(|v| v.as_str()).unwrap_or("INFO");
    
    let mut motor = motor.lock().await;
    motor.agregar_log(ip, mensaje, categoria);
    "ok"
}

#[tokio::main]
async fn main() {
    println!("
============================================================
   ANGEL GUARDIAN - MOTOR ONION EN RUST
   Servidor web + Dashboard
============================================================
");

    let motor = Arc::new(Mutex::new(MotorOnion::new()));

    let app = Router::new()
        .route("/", get(handler_index))
        .route("/api/logs", get(handler_logs))
        .route("/api/logs", post(handler_post_log))
        .route("/api/stats", get(handler_stats))
        .with_state(motor.clone());

    // 🟢 CAMBIO AQUÍ - Usar puerto de Render
    let port = std::env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let addr = format!("0.0.0.0:{}", port);
    println!("Servidor en: http://{}", addr);
    println!("Dashboard: http://{}/", addr);
    println!("");

    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
