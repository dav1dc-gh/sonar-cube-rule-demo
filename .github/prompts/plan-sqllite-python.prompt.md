# Plan: SQLite Persistence for SonarQube Rules

## TL;DR
Replace on-disk JSON rule files with a SQLite database, using Python + SQLAlchemy for the schema definition and a migration script to load existing JSON rules into the DB. Docker Compose provides a reproducible environment.

## Steps

### Phase 1: Project Setup
1. Create `requirements.txt` with `sqlalchemy>=2.0` and `pydantic>=2.0` (for input validation)
2. Create `Dockerfile` for the Python environment (non-root user, minimal image)
3. Create `docker-compose.yml` with a service that mounts the workspace and persists the SQLite DB via a volume

### Phase 2: Database Schema (SQLAlchemy Models)
4. Create `db/models.py` — define the following tables with CHECK constraints on all enum columns, NOT NULL on required fields, and FOREIGN KEY with ON DELETE CASCADE:
   - **`rules`** — main table: `id` (PK, auto), `key` (unique, indexed, NOT NULL), `name` (NOT NULL), `description` (NOT NULL), `severity` (CHECK IN CRITICAL/MAJOR/MINOR/INFO), `type` (CHECK IN VULNERABILITY/BUG/CODE_SMELL), `default_severity`, `status` (CHECK IN READY/LEGACY/DEPRECATED), `category` (CHECK IN security/code-smells/maintainability/performance)
   - **`rule_tags`** — join table: `id`, `rule_id` (FK → rules, CASCADE), `tag` (NOT NULL)
   - **`rule_remediation`** — `id`, `rule_id` (FK → rules, CASCADE, unique), `constant_cost` (NOT NULL)
   - **`rule_remediation_examples`** — `id`, `remediation_id` (FK → rule_remediation, CASCADE), `before_code` (text, NOT NULL), `after_code` (text, NOT NULL)
   - **`rule_impacts`** — `id`, `rule_id` (FK → rules, CASCADE), `software_quality` (CHECK IN SECURITY/MAINTAINABILITY/RELIABILITY/PERFORMANCE), `severity` (CHECK IN LOW/MEDIUM/HIGH)
   - **`rule_params`** — `id`, `rule_id` (FK → rules, CASCADE), `key` (NOT NULL), `name`, `description`, `default_value`, `type` (CHECK IN INTEGER/STRING/FLOAT)
   - **`rule_debt`** — `id`, `rule_id` (FK → rules, CASCADE, unique), `function` (CHECK IN LINEAR/CONSTANT_ISSUE), `coefficient` (nullable), `offset`
5. Create `db/database.py` — SQLAlchemy engine + session factory, pointing at `sonarqube_rules.db`

### Phase 3: Input Validation
6. Create `db/validators.py` — Pydantic models mirroring the JSON schema:
   - Validate required fields (`key`, `name`, `description`, `severity`, `type`)
   - Validate enum values against strict allowed sets
   - Validate string length limits on `key` (max 100), `name` (max 200)
   - Reject unexpected/extra fields

### Phase 4: Migration Script
7. Create `db/migrate.py` — script that:
   - Walks `rules/` directory recursively
   - **Path safety**: resolves each file path and verifies it stays within the `rules/` root; skips symlinks
   - Only processes files ending in `.json`
   - Validates each JSON file through Pydantic models before insert (rejects invalid files with clear error messages)
   - Extracts category from the parent folder name
   - Uses ORM methods only — **no raw SQL string construction**
   - Handles the optional `params` field gracefully
   - Is idempotent: drops and recreates tables on each run
   - Sets SQLite file permissions to 0600 after creation
   - Prints a summary: number of rules loaded per category, and any rejected files

### Phase 5: Docker Hardening
8. Create `Dockerfile` — Python 3.12 slim image, installs deps, copies source, runs as non-root user via `USER` directive
9. Create `docker-compose.yml`:
   - Single service `db-migrate`
   - Mounts `./rules` as **read-only**
   - Persists `sonarqube_rules.db` to a named volume
   - `read_only: true` on container filesystem (except DB volume)
   - `security_opt: [no-new-privileges:true]`
   - `cap_drop: [ALL]`
   - Runs `python db/migrate.py` as entrypoint

## Relevant files

- `rules/**/*.json` — source data (52 JSON files across 4 categories) — read-only input
- `db/models.py` (new) — SQLAlchemy ORM models for all tables described above, with CHECK constraints and NOT NULL enforcement
- `db/database.py` (new) — engine/session setup targeting `sonarqube_rules.db`
- `db/validators.py` (new) — Pydantic validation models for JSON input sanitization
- `db/migrate.py` (new) — JSON-to-SQLite migration script, walks `rules/` tree with path safety checks
- `requirements.txt` (new) — `sqlalchemy>=2.0`, `pydantic>=2.0`
- `Dockerfile` (new) — Python 3.12-slim, non-root user, pip install, copy source
- `docker-compose.yml` (new) — hardened service definition with read-only mounts, dropped capabilities, no-new-privileges

## Schema Design Rationale

The JSON is semi-structured with nested objects and arrays. A normalized relational schema is used instead of storing raw JSON blobs because:
- Enables querying rules by tag, severity, impact, category, etc.
- `rule_tags`, `rule_impacts`, and `rule_params` are one-to-many relationships (separate tables)
- `rule_debt` and `rule_remediation` are one-to-one (separate tables to keep `rules` table clean)
- `rule_remediation_examples` belongs to the remediation relationship (one-to-many)
- `category` is derived from the filesystem folder name and stored as a column on `rules`

## Verification
1. Run `docker compose up --build` — should complete without errors
2. After migration, open the SQLite DB and verify: `SELECT COUNT(*) FROM rules;` returns 52
3. Spot-check: `SELECT * FROM rules WHERE key = 'sql-injection';` — verify all fields match `rules/security/sql-injection.json`
4. Verify relationships: `SELECT r.key, t.tag FROM rules r JOIN rule_tags t ON r.id = t.rule_id WHERE r.key = 'sql-injection';`
5. Verify optional fields: confirm rules without `params` have no rows in `rule_params`
6. **Validation test**: create a malformed JSON file (e.g., missing `key`, invalid `severity` value) — migration should reject it with a clear error and continue loading valid files
7. **Path traversal test**: create a symlink inside `rules/` pointing outside the directory — migration should skip it
8. **DB permissions test**: after migration, verify file permissions on `sonarqube_rules.db` are `0600`
9. **CHECK constraint test**: attempt a direct `INSERT` with an invalid enum value — should be rejected by the DB
10. **Docker hardening test**: verify container runs as non-root (`docker compose exec db-migrate whoami`)

## Decisions
- **SQLAlchemy 2.0+** mapped-column style for modern, type-annotated models
- **Pydantic 2.0+** for input validation before any data touches the database
- **Normalized schema** over JSON blob storage — enables structured queries
- **Defence in depth** — validation in Python (Pydantic) AND in the DB (CHECK constraints)
- **Idempotent migration** — safe to re-run; drops/recreates tables each time
- **No REST API** — out of scope per user decision; can be added later with FastAPI
- **No Alembic migrations** — unnecessary for initial load; can be added if schema evolves
- **SQLite file** persisted via Docker volume at `data/sonarqube_rules.db`
- **No raw SQL** — all database operations via SQLAlchemy ORM to prevent injection

## Further Considerations
1. **Query helper**: Should the plan include a small `db/query.py` utility with common lookups (by category, severity, tag) for convenience? Recommendation: skip for now, add when needed.
2. **Alembic**: If the schema is expected to evolve, Alembic migration tracking can be added in a follow-up. Recommendation: defer.
