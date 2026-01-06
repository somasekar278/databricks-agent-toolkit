# Changelog

## [0.2.0] - 2026-01-06

### Added
- Short CLI aliases: `dbat` and `dat` (easier to type!)
- FastAPI-based agent backends with OpenAPI schema
- Streaming support via Server-Sent Events (SSE)
- Auto-generated API documentation at `/docs`
- Compatibility with all 6 official Databricks UI templates
- Automated monitoring for upstream template changes

### Changed
- **Breaking**: Migrated from Flask to FastAPI
- **Breaking**: New file structure: `agent.py` + `start_server.py` (replaces `app.py`)
- **Breaking**: API endpoint: `/api/invocations` (OpenAI format, replaces `/api/chat`)
- Simplified streaming implementation (server-side delay)
- Updated all templates to follow official Databricks patterns

### Removed
- Flask dependency
- Complex client-side streaming logic
- AgentServer fallback (simplified)

## [0.1.x] - Earlier versions

Previous releases before OpenAI API migration.
