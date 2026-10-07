# Humanless agent-readiness pilot

**Can AI agents find your product, sign up and finish real work? We test it, and we check the result ourselves.**

## The problem

AI agents now pick, sign up for and use developer tools on their own. Two things go wrong, and you rarely see either:

- **Agents say "done" when the job isn't.** The run log says "account created" or "deployed". Your database, inbox or API says otherwise.
- **Sign-up and verification flows stop agents.** Bot challenges, email codes, phone checks, SSO-only logins and keys that only a dashboard can issue stall an agent. The person who sent it never learns why.

Every stalled agent is a sign-up you never knew you lost.

## What we test

- **One product, up to 3 real workflows** you choose, each run end to end: discover, sign up, then a core task (for example, create a project and make the first API call).
- **2 agent setups** (for example, a browser agent and a coding agent using your API, CLI or MCP server), **3 repeat runs each**: 18 runs in total, so we can tell flaky from broken.
- **Discoverability:** llms.txt, docs as markdown, API and OpenAPI, MCP, robots rules.
- **Sign-up friction:** bot challenges, email or phone verification, SSO-only logins, and whether an agent can get a key or token without a human.

## How we verify

We don't take the agent's word for it. Each run's end state is checked separately through your API, a database query or a test inbox. A negative control is built in, so a false "success" shows up as a failure. Every run is recorded with traces: steps, requests, screenshots and timings.

## What you get

1. **A reproducible report:** pass or fail on the verified end state for each workflow and agent, with traces and the scripts so your team can rerun it.
2. **A failure list:** where each run stalled or wrongly reported success, and why.
3. **Prioritised fixes,** ranked by impact on agent completion and effort.
4. **One re-test** after you ship a fix, with before-and-after results.

## Timeline: 10 business days from access and deposit

Days 1–2: kickoff, pick workflows, set up test accounts. Days 3–7: runs and verification. Days 8–9: report. Day 10: report delivered, with a walkthrough by call or written Q&A. Re-test any time within 30 days of the report.

## Price and terms

- **A$4,500 fixed** (about US$3,130 at 6 October 2026 rates). No hourly billing.
- **50% deposit (A$2,250)** to start; balance on delivery of the report.
- **Full fee credited** against a Humanless implementation (A$25,000–50,000) if signed within 60 days of the report.
- We don't solve captchas, bypass security controls, load-test, or touch real customer data. Test accounts are cleaned up afterwards.

## What we need from you

- A named contact and a short kickoff (call or email).
- Up to 3 workflows, and what "done" looks like for each.
- One way to check the end state: a read-only API key, a database query or a log or webhook view.
- Permission to create test accounts, and whether to test your bot protection as it is (we report where it stops agents) or through a test bypass.

## Next step

Reply with your product and up to three workflows you want tested. We'll send a short order form and the deposit invoice the same day. A free sample audit is available on request.

**Miles Mercer, Humanless** · miles@mail.ricricho.com
