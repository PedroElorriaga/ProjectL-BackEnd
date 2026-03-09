## Plan: Login Module Checklist

Actionable checklist focused on MVP priorities: security hardening, core auth features, and strong tests.

## Current Status Snapshot (2026-03-09)
- Implemented: `POST /login` rate limiting (`5/min` per IP)
- Implemented: clearer invalid-credential response (`401` with generic message)
- Implemented: tests for login success, wrong password, invalid email, and rate limit (`429`)
- Pending in login DTO: stricter password strength validation rules

**Phase 1 - Security Hardening**
- [X] Create `PasswordValidator` at `src/services/security/password/password_validator.py`
- [X] Enforce password strength (min 8, upper, lower, digit, special)
- [X] Add rate limiting to `POST /login/` in `src/modules/login/routes/login.py` (`5/min` per IP)
- [X] Add clearer auth error handling in `src/modules/login/controllers/login_controller.py`

**Phase 2 - Core Auth Features**
- [ ] Create session/refresh token model `src/modules/users/models/session_token.py`
- [ ] Extend `JwtHandle` in `src/services/security/jwt/jwt_handle.py` for refresh tokens
- [ ] Add `DELETE /login/logout` endpoint in `src/modules/login/routes/login.py`
- [ ] Add `POST /login/refresh` endpoint for access-token renewal
- [ ] Add `POST /login/password-reset` endpoint (request reset)
- [ ] Add `POST /login/password-reset/confirm` endpoint (apply new password)
- [ ] Add repository methods in `src/modules/users/repositories/user_repository.py`:
- [ ] `get_item_by_reset_token()`
- [ ] `update_password()`
- [ ] `revoke_refresh_tokens()`
- [ ] Update `LoginResponseDTO` to optionally return `refresh_token`

**Phase 3 - Email Verification**
- [ ] Add email verification service under `src/services/email/`
- [ ] Add `GET /login/verify-email/{token}` endpoint
- [ ] Update user creation flow to send verification email and mark account unverified
- [ ] Add `POST /usuario/resend-verification` endpoint (with rate limit)
- [ ] Optionally enforce verified-email check in protected routes

**Phase 4 - Tests and Quality**
- [ ] Add tests for rate-limiting behavior (expect `429` on excess)
- [ ] Add tests for refresh token flow (valid, expired, revoked)
- [ ] Add tests for logout invalidation
- [ ] Add tests for password reset lifecycle (valid token, expired token, invalid token)
- [ ] Add tests for email verification/resend flow
- [ ] Add tests for malformed headers/tokens and missing fields
- [ ] Run full regression test suite in `tests/test_api.py`
- [ ] Update `docs/LOGIN_MODULE.md` with new routes and examples

**Decisions Locked for MVP**
- [x] Keep `sucess` field spelling for backward compatibility
- [x] Use DB-backed refresh tokens (supports revocation/logout)
- [x] Use IP-based rate limiting first, improve later if needed
- [x] Exclude 2FA/OAuth for this iteration

**Definition of Done**
- [ ] All new endpoints implemented and passing tests
- [ ] Existing tests remain green (no regression)
- [ ] Login module docs updated and accurate
- [ ] Security checks validated (rate limit, token revocation, password strength)
