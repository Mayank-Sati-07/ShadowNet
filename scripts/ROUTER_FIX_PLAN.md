Router fix plan

Goal: Remove temporary proxy endpoints in `src/api/main.py` and ensure all APIRouter instances defined under `src/api/routes/*` are properly mounted on the FastAPI app so runtime imports never require proxies.

Steps:

1. Reproduce the issue
   - Run `python -c "from importlib import import_module; m=import_module('src.api.main'); print([type(r).__name__+':'+str(getattr(r,'path',None)) for r in m.app.router.routes])"` to observe current router wrappers.

2. Identify root cause
   - Inspect each module under `src/api/routes/` for side-effects at import time (e.g., code that conditionally registers routes, imports heavy modules, or mutates app state).
   - Look for circular imports between `src/api/main.py` and route modules causing routers to be enclosed in `_IncludedRouter` wrappers.

3. Minimal safe fix
   - Ensure each `src/api/routes/*.py` only defines an `APIRouter` instance and route handlers, and does not import `src.api.main` or call `app.include_router` itself.
   - In `src/api/main.py`, import route modules (no side-effects) and call `app.include_router(router)` for each. Avoid pkg-level dynamic include logic.

4. Remove runtime flattening & proxies
   - After step 3 passes all tests, remove the `_flatten` implementation and the proxy endpoints from `src/api/main.py`.

5. Tests and validation
   - Re-run `pytest` to ensure tests still pass.
   - Start uvicorn and manually exercise the endpoints (e.g., `GET /api/persons`).

6. Optional cleanup
   - Replace remaining `print()` logging in routes/ingest code with `logging` and appropriate levels.
   - Add a small pre-commit hook or CI check that validates `app.include_router()` results in exposed `APIRoute` path entries (simple script that imports `src.api.main` and checks expected paths).

Notes:
- The plan emphasizes minimizing behavioural changes in the running app while fixing import semantics. If implementing the minimal fix reveals deeper circular import issues, we will refactor route modules into `routes/handlers.py` (definitions) and `routes/router.py` (router creation) to break cycles.
