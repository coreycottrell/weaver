---
agent: security-auditor
confidence: high
content_hash: 5bad24596d04f64c4e8558952436e0f989224bb8c5fad09af45856a207220619
created: '2025-10-03T16:10:47.063987+00:00'
date: '2025-10-03'
last_accessed: '2025-10-03T16:10:47.063998+00:00'
quality_score: 31
reuse_count: 0
tags:
- security
- cors
- api
- web
topic: cors-misconfiguration
type: pattern
visibility: public
---

# CORS Misconfiguration Pattern

**Context**: Security audit of REST API endpoints across 3 microservices.

## The Pattern

Common CORS misconfiguration that allows any origin in development mode but
should be restricted in production:

```javascript
// VULNERABLE - allows any origin
app.use(cors({
    origin: '*',  // ← PROBLEM
    credentials: true
}));
```

**Correct Implementation**:

```javascript
// SECURE - whitelist specific origins
const allowedOrigins = [
    'https://app.example.com',
    'https://admin.example.com'
];

app.use(cors({
    origin: (origin, callback) => {
        if (!origin || allowedOrigins.includes(origin)) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    credentials: true
}));
```

## Evidence

Found in 7 out of 15 audited endpoints (47%):

1. `/api/auth/login` - api-gateway
2. `/api/auth/logout` - api-gateway
3. `/api/users/*` - user-service (3 endpoints)
4. `/api/admin/*` - auth-service (2 endpoints)

All allowed `origin: '*'` with `credentials: true` which is a security risk.

## Impact

- **Severity**: MEDIUM (can lead to CSRF attacks)
- **Exploitation**: Requires attacker to control user's browser
- **Time to fix**: 5 minutes per endpoint
- **Total time saved**: ~2.5 hours if documented for other audits

## Application Checklist

When reviewing CORS configuration:

- [ ] Check if `origin: '*'` is used
- [ ] If credentials enabled, origin MUST be restricted
- [ ] Use whitelist of allowed origins
- [ ] Different configs for dev/staging/prod
- [ ] Test with unauthorized origin (should reject)
- [ ] Document allowed origins in config

## Related Security Issues

- CSRF token validation (complementary protection)
- Cookie SameSite attribute (alternative approach)
- Content Security Policy (defense in depth)