"""AI failure analyzer for the self-healing CI/CD pipeline.

Reads a CI log file, asks a Llama model on Groq to diagnose the failure,
and prints a Markdown report (suitable for $GITHUB_STEP_SUMMARY).

Usage:
    python ai_module/analyzer.py build.log
    python ai_module/analyzer.py build.log >> "$GITHUB_STEP_SUMMARY"

Environment:
    GROQ_API_KEY   required for a live diagnosis (falls back to a log excerpt)
    GROQ_MODEL     optional, default: llama-3.3-70b-versatile
"""
import os
import sys

import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
MAX_LOG_CHARS = 6000  # keep the tail: the error is almost always at the end

SYSTEM_PROMPT = (
    "You are a senior DevOps engineer reviewing a failed CI/CD run. "
    "Be concise and concrete. Respond in Markdown with exactly these sections: "
    "**Root cause**, **Evidence** (quote the key log line), "
    "**Suggested fix** (exact file and change), **Confidence** (low/medium/high)."
)


def read_log_tail(path, max_chars=MAX_LOG_CHARS):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text[-max_chars:]


def build_messages(log_tail):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "This CI run failed. Here is the end of the log:\n\n```\n"
            + log_tail
            + "\n```",
        },
    ]


def call_groq(messages, api_key, model=None, timeout=30):
    resp = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model or os.environ.get("GROQ_MODEL", DEFAULT_MODEL),
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 600,
        },
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def diagnose(log_path, api_key=None):
    """Return a Markdown report for the failed run in `log_path`."""
    log_tail = read_log_tail(log_path)
    header = "## 🤖 Self-Healing Pipeline: AI Failure Diagnosis\n\n"

    if not api_key:
        return (
            header
            + "_GROQ_API_KEY not set, showing raw log excerpt instead._\n\n"
            + "```\n"
            + log_tail[-1500:]
            + "\n```\n"
        )
    try:
        analysis = call_groq(build_messages(log_tail), api_key)
    except (requests.RequestException, KeyError, ValueError) as exc:
        return (
            header
            + f"_AI analysis unavailable ({type(exc).__name__}). Raw log excerpt:_\n\n"
            + "```\n"
            + log_tail[-1500:]
            + "\n```\n"
        )
    return header + analysis + "\n"


def main(argv):
    if len(argv) != 2:
        print("usage: analyzer.py <log-file>", file=sys.stderr)
        return 2
    if not os.path.isfile(argv[1]):
        print(f"log file not found: {argv[1]}", file=sys.stderr)
        return 2
    print(diagnose(argv[1], os.environ.get("GROQ_API_KEY")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
