CUSTOMERS = {
    "C-1234": {
        "name": "Nayana Sharma",
        "email": "nayana@email.com",
        "plan": "pro",
        "member_since": "2023-03-15",
        "past_tickets": 2,
    },
    "C-5678": {
        "name": "Arjun Mehta",
        "email": "arjun@email.com",
        "plan": "free",
        "member_since": "2025-01-10",
        "past_tickets": 0,
    },
    "C-9012": {
        "name": "Priya Nair",
        "email": "priya@company.com",
        "plan": "enterprise",
        "member_since": "2021-07-22",
        "past_tickets": 14,
    },
}

KNOWLEDGE_BASE = {
    "login": {
        "title": "Login Issues — Troubleshooting Guide",
        "solution": "1. Clear browser cache. 2. Check if account is locked after 5 failed attempts. 3. Verify email is correct. 4. Try password reset link.",
    },
    "billing": {
        "title": "Billing & Charges FAQ",
        "solution": "Charges appear within 24hrs of plan change. Refunds take 5-7 business days. Duplicate charges can be disputed via support.",
    },
    "export": {
        "title": "Data Export Guide",
        "solution": "Go to Settings > Data > Export. Supported formats: CSV, JSON. Large exports (>10k rows) are emailed as a link.",
    },
    "api": {
        "title": "API Rate Limits",
        "solution": "Free plan: 100 req/hr. Pro plan: 1000 req/hr. Enterprise: custom limits. Rate limit errors return HTTP 429.",
    },
    "performance": {
        "title": "Known Performance Issues",
        "solution": "Dashboard loading times are affected during peak hours (9-11 AM UTC). Team is working on optimization. Use API for bulk operations.",
    },
}

SAMPLE_TICKETS = [
    "Hi, I've been trying to log into my account for the past 2 hours. I reset my password twice but it still says 'invalid credentials.' My account ID is C-1234. I have a presentation tomorrow and all my files are in there. Please help urgently.",
    "I was charged $49.99 twice this month for my Pro plan. My account ID is C-1234. Please refund the duplicate charge.",
    "Our API keeps returning 429 errors since yesterday. We're on the enterprise plan and this is blocking our production pipeline. Account ID: C-9012.",
    "How do I export my data as CSV? I can't find the option anywhere. Account: C-5678.",
    "The dashboard has been extremely slow for the past week. Pages take 20+ seconds to load. This is unacceptable for an enterprise account. Account ID: C-9012.",
]
