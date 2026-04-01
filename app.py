import streamlit as st
import anthropic

st.set_page_config(page_title="Foundree42 Copilot", layout="wide")
st.title("Foundree42 Prospecting Copilot")

api_key = st.secrets.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error("Missing ANTHROPIC_API_KEY in Streamlit secrets.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

SYSTEM_PROMPT = """
You are a senior Salesforce GTM strategist at Foundree42 — a lean, senior-led Salesforce consulting firm.

Foundree42 positioning:
- "Clarity before code. Outcomes before output."
- Fixes messy, underperforming, or stalled Salesforce environments
- Strong POV on AI/Agentforce: enforcement > advice, orchestration > features
- Deep healthcare vertical experience: VBC, Health Cloud, digital health commercial stacks

Core beliefs:
- Enforcement > Advice: AI that advises doesn't change behavior. AI that enforces does.
- Clarity Before Code: You can't automate a broken process. You can only make it fail faster.
- Crawl/Walk/Run is a delay strategy: phased rollouts produce pilots and demos, not outcomes.
- Data ownership is a people problem, not a technical one. Dirty data = accountability gap.
- Outcomes over output: behavior change and forecast accuracy, not dashboards and demos.
- Healthcare is a vertical, not a template: VBC orgs fail because clinical workflows get mapped
  to commercial objects and nobody owns the boundary between them.

Write with clarity, specificity, and restraint.
No buzzwords. No generic consulting language. Sound like an operator, not a consultant.
Write for an executive audience.
"""

def call_claude(prompt, max_tokens=1200):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            temperature=0.3,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {type(e).__name__}: {str(e)}"


tab1, tab2, tab3 = st.tabs(["Account Brief", "Fit Scorer", "LinkedIn Outreach"])


# ── TAB 1: ACCOUNT BRIEF ──────────────────────────────────────────────────────
with tab1:
    st.subheader("Account Brief")
    st.caption("Signal-anchored, 5-section brief for outreach and call prep.")

    col1, col2 = st.columns(2)
    with col1:
        ab_company = st.text_input("Company", key="ab_company")
        ab_name    = st.text_input("Contact Name", key="ab_name")
        ab_title   = st.text_input("Contact Title", key="ab_title")
    with col2:
        ab_signal  = st.text_input(
            "Signal to Anchor On",
            key="ab_signal",
            placeholder="e.g. Series C close, new CRO hire, post-acquisition, Salesforce expansion"
        )
        ab_notes   = st.text_area(
            "Notes (LinkedIn bio, news, company context)",
            key="ab_notes",
            height=120
        )

    if st.button("Generate Account Brief", key="btn_brief"):
        if ab_company and ab_title:
            with st.spinner("Building brief..."):
                prompt = f"""
Generate a concise, executive-ready account brief. The goal is NOT to pitch —
it is to surface a clear point of view that creates a reason to engage.

Company: {ab_company}
Contact: {ab_name} — {ab_title}
Signal to Anchor On: {ab_signal if ab_signal else "derive from context"}
Notes: {ab_notes if ab_notes else "none provided"}

Output exactly this format:

### 1. Company Snapshot
2-3 sentences. What they do, where they are in scale/maturity. Factual and grounded.

### 2. Contact Context
2-3 sentences. What this person owns, what they are measured on, what pressures they are under.

### 3. Signal Interpretation
2-4 sentences. What the signal actually suggests — not what it is. Why it matters operationally.
What is likely happening beneath the surface. Do not restate the signal. Interpret it.

### 4. Core Hypothesis (One Only)
1-2 sentences. What is most likely not working as well as it should.
Tied to execution, not strategy. Specific, not broad. Should feel like an insight, not a guess.

### 5. Angle (Observation → Implication → Open)
3-5 sentences. Observation: a grounded pattern seen in similar situations.
Implication: what that typically leads to. Open: a neutral question that invites conversation.
Do NOT pitch services. Do NOT suggest a meeting. Do NOT sound salesy.

Rules: no buzzwords, no generic statements, prioritize specificity over completeness.
"""
                st.markdown(call_claude(prompt))
        else:
            st.warning("Company and Title are required.")


# ── TAB 2: FIT SCORER ─────────────────────────────────────────────────────────
with tab2:
    st.subheader("Account Fit Scorer")
    st.caption("Score an account 1–10 across 5 dimensions before investing time in a brief.")

    col1, col2 = st.columns(2)
    with col1:
        fs_company  = st.text_input("Company", key="fs_company")
        fs_industry = st.text_input("Industry", key="fs_industry")
        fs_size     = st.text_input("Company Size", key="fs_size", placeholder="e.g. 200 employees, $50M ARR")
        fs_title    = st.text_input("Contact Title", key="fs_title")
    with col2:
        fs_trigger  = st.text_input(
            "Trigger Event",
            key="fs_trigger",
            placeholder="e.g. new CRO, post-acquisition, Salesforce admin job posted"
        )
        fs_notes    = st.text_area("Known Notes", key="fs_notes", height=120)

    if st.button("Score This Account", key="btn_score"):
        if fs_company and fs_title:
            with st.spinner("Scoring..."):
                prompt = f"""
Score this account for Foundree42 fit. Be sharp and honest — including about misfit.

Company: {fs_company}
Industry: {fs_industry if fs_industry else "unknown"}
Size: {fs_size if fs_size else "unknown"}
Contact Title: {fs_title}
Trigger Event: {fs_trigger if fs_trigger else "none identified"}
Notes: {fs_notes if fs_notes else "none provided"}

Score on each dimension (1-10):
1. Salesforce Complexity — how likely is a complex, multi-cloud, technically deep org?
2. Messy Middle / Underperformance Potential — signs of process debt, adoption failure, ownership gaps?
3. AI / Agentforce Relevance — is there a realistic enforcement use case, not just "AI is interesting"?
4. Foundree42 Fit — do they need lean/senior/outcome-focused work, or a big SI with bench depth?
5. Access / Entry Potential — warm path, clear trigger, named contact, or cold enterprise with no door?

Output exactly this format:

Overall Score: X/10
Priority Level: High / Medium / Low

Why this score:
- [bullet]
- [bullet]
- [bullet]
- [bullet]

Best entry point:
[specific person, role, or path — not generic]

Recommended next action:
[one concrete action only]

Be honest. If access is low, reflect it in the score.
If they need a large SI, say so. A score without sharp reasoning is useless.
"""
                st.markdown(call_claude(prompt))
        else:
            st.warning("Company and Contact Title are required.")


# ── TAB 3: LINKEDIN OUTREACH ──────────────────────────────────────────────────
with tab3:
    st.subheader("LinkedIn Outreach")
    st.caption("Two versions: warm/relationship-first and direct/slightly provocative.")

    col1, col2 = st.columns(2)
    with col1:
        lo_name    = st.text_input("Contact Name", key="lo_name")
        lo_title   = st.text_input("Contact Title", key="lo_title")
        lo_company = st.text_input("Company", key="lo_company")
    with col2:
        lo_context = st.text_area(
            "Context (trigger event, new role, signal)",
            key="lo_context",
            height=80
        )
        lo_angle   = st.text_area(
            "Angle (optional — leave blank to derive from context)",
            key="lo_angle",
            height=80
        )

    lo_content = st.text_area(
        "Recent content (optional — paste a recent LinkedIn post or blog angle to reference naturally)",
        key="lo_content",
        height=80
    )

    if st.button("Write Outreach Messages", key="btn_outreach"):
        if lo_name and lo_title and lo_company and lo_context:
            with st.spinner("Writing messages..."):
                prompt = f"""
Write two LinkedIn outreach messages on behalf of a senior Salesforce consultant at Foundree42.
The message is not a pitch. It is a peer-level observation from someone who has seen this situation before.

Name: {lo_name}
Title: {lo_title}
Company: {lo_company}
Context: {lo_context}
Angle: {lo_angle if lo_angle else "derive the most specific and useful one from the context"}
Recent content: {lo_content if lo_content else "none — do not reference content"}

### Version A — Warm / Relationship-First
Tone: thoughtful, observational, genuine curiosity.
Acknowledges their situation, shares a pattern worth considering, opens a door without pushing through it.

### Version B — Direct / Slightly Provocative
Tone: confident, slightly edgy, still respectful.
Names something uncomfortable but true. Earns attention by being specific and a little bold.

Constraints for both versions:
- 5-7 sentences max
- No "hope you're doing well" or "just checking in"
- No service list, no capabilities, no credentials
- Reference something specific: their role, the trigger, or what it implies
- Foundree42 positioning: one subtle phrase at most, tied to context
- End with a soft, low-friction question — not "let's hop on a call"
- Write in first person as the consultant
- If recent content is provided, reference it only if the connection is organic — never force it

Output just the two messages with Version A / Version B headers. No preamble. No explanation after.
"""
                st.markdown(call_claude(prompt, max_tokens=800))
        else:
            st.warning("Name, Title, Company, and Context are required.")
