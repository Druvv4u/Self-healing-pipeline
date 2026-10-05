"""Interview demo helper: break or fix the app on purpose.

    python scripts/demo.py break   # /health now returns "broken" -> tests fail -> AI diagnosis runs
    python scripts/demo.py fix     # restore the healthy response

Then: git add -A && git commit -m "demo" && git push
"""
import pathlib
import sys

MAIN = pathlib.Path(__file__).resolve().parent.parent / "app" / "main.py"
GOOD = '{"status": "healthy"}'
BAD = '{"status": "broken"}'


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("break", "fix"):
        print(__doc__)
        return 2
    src = MAIN.read_text(encoding="utf-8")
    old, new = (GOOD, BAD) if sys.argv[1] == "break" else (BAD, GOOD)
    if old not in src:
        print(f"Nothing to do: app is already in '{sys.argv[1]}' state.")
        return 0
    MAIN.write_text(src.replace(old, new), encoding="utf-8")
    print(f"app/main.py updated ({sys.argv[1]}). Now commit and push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
