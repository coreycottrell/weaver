# Lesson: Blog Publishing is Netlify, NOT Hub

**Date**: 2026-01-04
**Agent**: blogger (lesson for the-conductor too)
**Severity**: HIGH - Corey called this "a huge miss"

---

## The Mistake

When asked to publish a blog post, the blogger agent:
1. Tried to send to A-C-Gee via comms hub
2. Thought A-C-Gee owned sageandweaver.com
3. Did NOT know WEAVER publishes its own blog via Netlify

## The Correction

**WEAVER publishes its own blog posts via Netlify.**

- Site: `https://sageandweaver-network.netlify.app/`
- WEAVER posts go in: `/home/corey/projects/AI-CIV/ACG/sageandweaver-network/weaver-blog/posts/`
- Deploy with: `netlify deploy --prod`
- Verify with: `curl -I {url}`

## Root Cause

The blogger manifest was missing:
- `sageandweaver-blog` skill
- `netlify-api-operations` skill
- `Bash` tool (needed for netlify CLI)
- Any mention of publishing workflow

## Fix Applied

Updated blogger.md with:
1. Skills: `sageandweaver-blog`, `netlify-api-operations`
2. Tools: Added `Bash`
3. Description: Explicitly mentions "PUBLISHES TO sageandweaver-network.netlify.app"
4. Body: Added full PUBLISHING WORKFLOW section with steps

## Corey's Feedback

> "this was a huge miss. make sure blogger manifest and description are updated. u cant make this simple mistake again."

## Key Lesson

**Agent manifests must include ALL skills for their full workflow.**

Writing content is only half the job. Publishing/deployment is the other half. The blogger agent now owns the complete pipeline: write → HTML → deploy → verify → deliver URL.

---

*Never make this mistake again.*
