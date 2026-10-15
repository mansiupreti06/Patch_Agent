🛡️ PatchAgent: Autonomous Multi-Agent Code Auditor & Auto-Fixer

An enterprise-grade, multi-agent code analysis and self-healing pipeline that bridges the gap between static AST security checks, automated patching, and sandbox verification.

🌟 Key Features

🔍 Agent 1: Deterministic Static AST Auditor: Scans Python source code using Abstract Syntax Trees (ast) without executing untrusted code. Detects critical vulnerabilities such as unsafe eval() functions, bare division operations, and syntax errors.

💻 Agent 2: Autonomous Patch Developer: Analyzes flagged security issues and generates clean, refactored replacement code with side-by-side code diff visualizers.

🧪 Agent 3: Isolated Subprocess Sandbox Tester: Executes unit test assertions in an isolated operating system process (subprocess), returning real-time pass/fail execution logs and tracebacks.

📊 Enterprise Engineering Dashboard: Built on Streamlit, featuring real-time metric cards, execution time tracking (in milliseconds), custom test case builders, and dark-mode styling.

📐 System Architecture

Unlike traditional AI tools that merely generate text without verification, PatchAgent utilizes an autonomous, test-driven feedback pipeline:

                  ┌───────────────────────────────┐
                  │      User Source Code        │
                  └──────────────┬────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Auditor Agent (AST Static Security Check)                    │
│    • Parses AST structure without code execution                │
│    • Flags syntax errors & critical vulnerabilities             │
└────────────────────────────────┬────────────────────────────────┘
                                 │ (Issues Flagged)
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Developer Agent (Automated Code Refactor)                    │
│    • Generates secure patches for detected issues               │
│    • Displays side-by-side original vs. patched code diff       │
└────────────────────────────────┬────────────────────────────────┘
                                 │ (Patched Code)
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Tester Agent (Subprocess Sandbox Runner)                     │
│    • Injects custom unit test assertions into temp file         │
│    • Executes code inside isolated OS process                   │
│    • Captures stdout/stderr and returns verification status     │
└─────────────────────────────────────────────────────────────────┘


🛠️ Tech Stack

Language: Python 3.9+

Frontend Dashboard: Streamlit

Static Analysis: Native ast (Abstract Syntax Trees) module

Sandbox Execution: subprocess & tempfile modules

Configuration: Streamlit Custom Theme (config.toml)
