cd C:\IA_angel

# Crear el archivo lib.rs (biblioteca principal)
@'
// ============================================
// ÁNGEL GUARDIAN - LIBRERÍA PRINCIPAL
// ============================================

pub mod core;
pub mod engine;
pub mod web;
pub mod adapters;

pub use core::*;
pub use engine::*;
pub use web::*;
pub use adapters::*;
'@ | Out-File -FilePath "src\lib.rs" -Encoding utf8