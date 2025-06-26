---
title: "Structure errors for safety"
description: "Create specific error types with appropriate status codes while ensuring sensitive details are logged but not exposed to clients. Follow guidelines for defining specific error types, implementing proper status codes, logging detailed errors internally, and returning sanitized error messages to clients."
repository: "tokio-rs/axum"
label: "Error Handling"
language: "Rust"
comments_count: 4
repository_stars: 22100
---

Create specific error types with appropriate status codes while ensuring sensitive details are logged but not exposed to clients. Follow these guidelines:

1. Define specific error types instead of using generic ones
2. Implement proper status codes for each error variant
3. Log detailed errors internally
4. Return sanitized error messages to clients

Example:
```rust
#[derive(Debug, Error)]
pub enum ApiError {
    #[error("Invalid input provided")]
    ValidationError(#[from] JsonRejection),
    #[error("Internal server error")]
    InternalError(#[source] anyhow::Error),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let status = match &self {
            Self::ValidationError(_) => StatusCode::UNPROCESSABLE_ENTITY,
            Self::InternalError(_) => StatusCode::INTERNAL_SERVER_ERROR,
        };
        
        // Log detailed error internally
        tracing::error!("{:#}", self);
        
        // Return sanitized response to client
        let body = Json(json!({
            "error": self.to_string()  // Uses the #[error] messages
        }));
        
        (status, body).into_response()
    }
}
```