# AI Usage

## Tools Used

| Tool | Purpose |
|------|---------|
| **ChatGPT (OpenAI)** | First attempt at understanding the exercise requirements — discarded after a critical misunderstanding (see below) |
| **Google Gemini** | Used extensively to understand the exercise requirements correctly and to research each requested technology (Flask, Playwright, SauceDemo, project architecture) |
| **Claude Code (Anthropic)** | Used for the entire implementation phase — all project code was generated here |

---

## How AI Was Used

The project was built in phases. The developer did not simply prompt the AI to "write the code." The process for each phase was:

1. Ask the AI to read and fully understand the project before doing anything
2. Align on a work plan — what to do first, what comes after
3. Request a detailed plan for the next phase before any code was written
4. Review the plan, ask questions, and direct adjustments
5. Only then generate the code for that phase
6. After several phases, ask the AI to review all work done so far for consistency

---

## Real Prompts Used

> **Note:** The original prompts were written in Portuguese. The excerpts below are free translations into English.

**Prompt 1 — Project onboarding:**
> "Hi, I have the following project (I won't paste it here). Before anything, read it and understand it well, then we'll talk to align on exactly what needs to be done."

**Prompt 2 — Work planning:**
> "Now that we understand it, let's plan a work plan — how we'll divide the flow, what I need to do first and what comes after."

**Prompt 3 — Technology deep dive:**
> "I need a deep and complete explanation of Playwright, what logs are, and how the interaction between Flask and Playwright will work."

**Prompt 4 — Phase review before advancing:**
> "Phase 7 — please first review all the phases we've done so far and check if everything looks good. Then let's plan every step of phase 7 and understand it together."

**Prompt 5 — Understanding a specific component:**
> "Now explain to me exactly what conftest will do so I understand what it's about."

---

## AI Mistakes and How They Were Corrected

### Critical misunderstanding — ChatGPT (OpenAI)

When the exercise was sent to ChatGPT, it fundamentally misunderstood the requirement. It interpreted the project as: *build your own e-commerce website, and create a Playwright robot to test that website.*

The correct interpretation was the opposite: *use Playwright to automate and test an existing third-party site (SauceDemo) — no custom store to be built.*

**How it was caught and corrected:**
The developer found the response suspicious. As a safety measure of always verifying one AI against another, the same exercise was sent to Google Gemini. After an in-depth conversation with Gemini to confirm the correct understanding, the developer then moved to Claude Code for implementation — already with a solid grasp of what was actually required.

This incident reinforced a key practice: **never trust a single AI's interpretation of requirements without cross-checking.**

### Wrong default port — Claude Code

Claude suggested port `5000` (Flask default) for running the app. The developer flagged that ports `5000` and `5001` were already occupied by other projects on the machine.

**How it was corrected:** The developer informed Claude, which immediately updated the port to `5002` across `app.py` and all documentation. No code was merged with the wrong port.

---

## Keeping Credentials and Tokens Safe

SauceDemo credentials are stored in a `.env` file that is never committed to version control. Shipping details (name, postal code) are entered by the user at checkout time — no sensitive data is hardcoded.

**How it was implemented:**
- `.env` holds only `SAUCE_USERNAME` and `SAUCE_PASSWORD`
- `.gitignore` explicitly excludes `.env` from git tracking
- Code reads credentials via `os.getenv()` — no hardcoded secrets anywhere in the codebase

---

## Scope of AI Contribution

| Area | AI involvement |
|------|---------------|
| Architecture planning | Collaborative (developer-led, AI-suggested) |
| Code generation | 100% AI-generated |
| Bug identification | Shared — developer spotted issues, AI diagnosed and fixed |
| Testing strategy | Collaborative (developer-led, AI-implemented) |
| Documentation | AI-generated based on developer-provided context |
