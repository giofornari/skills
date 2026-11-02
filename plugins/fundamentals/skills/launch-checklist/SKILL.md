---
name: launch-checklist
description: "Pre-deploy checks, staged rollout, rollback plan. Not for: review-change."
---
> Source: addyosmani/agent-skills (MIT), read 2026-11-02

# Launch Checklist

Deploy safely: every launch reversible, observable and incremental, with a rollback plan written **before** the deploy and a clear definition of success. Use it for a first production deploy, a significant release, a data or infrastructure migration, or opening a beta. Every deploy carries risk, so every deploy qualifies.

## 1. Pre-launch checks

- **Code**: tests (unit, integration, e2e), build without warnings, lint and types pass, reviewed and approved, no TODO that must be resolved first, no debug logging, failure modes handled.
- **Security**: no secrets in code or history; the ecosystem's dependency audit shows no critical or high findings; input validated on user-facing endpoints; authn and authz in place; security headers (CSP, HSTS); rate limits on auth endpoints; CORS limited to named origins.
- **Performance**: Core Web Vitals in the Good range; no N+1 in critical paths; images optimised; bundle within budget; indexes on queried columns; caching for static assets and repeated queries.
- **Accessibility**: keyboard navigation, screen-reader structure, contrast 4.5:1 for text, focus management in modals, descriptive form errors, no axe or Lighthouse warnings.
- **Infrastructure**: production env vars set; migrations applied or ready; DNS, SSL and CDN configured; logging and error reporting on; a health-check endpoint that answers.
- **Docs**: README, API docs, ADRs for architectural decisions, changelog, user-facing docs.

## 2. Ship behind a feature flag

Decouple deploy from release. Lifecycle: deploy with the flag **off** → enable for the team → gradual rollout (5% → 25% → 50% → 100%) → monitor at every step → remove the flag and the dead path. Rules: each flag has an owner and an expiry; remove it within two weeks of full rollout; never nest flags; test both states in CI.

## 3. Staged rollout

1. Deploy to staging: full suite, manual smoke test of the critical flows.
2. Deploy to production with the flag off; health check passes, no new errors.
3. Enable for the team; watch 24 hours.
4. Canary at 5%; compare against baseline for 24-48 hours; advance only if every threshold below is green.
5. Step up to 25%, 50%, 100% with the same monitoring and the ability to drop back one step.
6. Full rollout; monitor for a week; clean up the flag.

| Metric | Advance | Hold and investigate | Roll back |
|---|---|---|---|
| Error rate | within 10% of baseline | 10-100% above | more than 2x baseline |
| P95 latency | within 20% | 20-50% above | more than 50% above |
| Client JS errors | no new types | new types on under 0.1% of sessions | new types on over 0.1% |
| Business metrics | neutral or better | down under 5% (maybe noise) | down over 5% |

Also roll back at once on a spike in user-reported issues, a data-integrity problem or a newly found vulnerability. A burn rate above baseline during the canary is a hold even when each threshold is green. Rolling back is responsible engineering, not an admission of failure.

**Error budget gate**: over 20% left, ship normally; 0-20%, slow rollouts and no high-risk changes; exhausted, freeze features and fix reliability until it resets.

## 4. Monitor

- **Application**: error rate (total and per endpoint), p50/p95/p99 latency, request volume, active users, key business metrics.
- **Infrastructure**: CPU, memory, DB connection pool, disk, network latency, queue depth.
- **Client**: LCP, INP, CLS, JS errors, API error rate as the client sees it, page load.
- Report errors with context (route, user id, component stack) from both an error boundary and server middleware; never expose internals to users.

**First hour after launch**: health endpoint returns 200; no new error types; latency has not regressed; walk the critical user flow by hand; logs are flowing and readable; the rollback mechanism is confirmed ready (dry run if possible). Someone must be watching.

## 5. Rollback plan (write it first)

- **Trigger conditions**: error rate above 2x baseline, P95 above a stated number, reports of a named issue.
- **Steps**: disable the flag, or redeploy the previous version (`git revert <commit>` then deploy); verify with the health check and error monitoring; tell the team.
- **Database**: the migration has a verified rollback command or runbook link; say whether data written by the new feature is kept or cleaned up.
- **Time to roll back**: flag under 1 minute, redeploy under 5, database under 15.

## Red flags

- No rollback plan, monitoring or error reporting; a big-bang release with no staging.
- A flag with no owner or expiry; nobody watching the first hour; "it's Friday afternoon, ship it".
- Production configured from memory rather than code; error budget exhausted and feature work continuing unchanged.
- "It works in staging": production has other data, traffic and edge cases.
