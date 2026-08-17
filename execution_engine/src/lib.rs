//! Simulated order-matching core.
//!
//! Compiles two ways from the same source:
//!   - `cdylib` + wasm-bindgen -> the browser WASM demo (the actual
//!     "browser-independent execution" artifact — self-contained,
//!     doesn't need the Python side running at all)
//!   - `rlib` -> linked into a native binary that the Python pipeline
//!     talks to over a small subprocess/JSON protocol
//!
//! This is the natural extension of the EigenVM work — same
//! Rust-to-WASM shape, different domain.
//!
//! Deliberately scoped to *simulated* matching, not a production
//! settlement system. See docs/future-work.md for why that framing
//! matters.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Side {
    Buy,
    Sell,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Order {
    pub ticker: String,
    pub side: Side,
    pub quantity: f64,
    pub limit_price: Option<f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Fill {
    pub ticker: String,
    pub quantity: f64,
    pub price: f64,
    pub timestamp_ms: u64,
}

/// TODO: the actual matching logic. Start with a simple price-time
/// priority book against simulated market data before adding anything
/// fancier — the point of this module is demonstrating fast, correct
/// matching, not sophistication.
pub fn match_order(_order: Order) -> Option<Fill> {
    todo!("order-matching logic")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn order_constructs() {
        let o = Order { ticker: "TEST".into(), side: Side::Buy, quantity: 10.0, limit_price: Some(100.0) };
        assert_eq!(o.ticker, "TEST");
    }
}
