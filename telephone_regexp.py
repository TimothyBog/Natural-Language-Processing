import re
import sys

PHONE_REGEX = re.compile(r"""
(
    (?:\+?1[\s\-.])?                # optional country code
    (?:\(\d{3}\)|\d{3})             # area code
    [\s\-.]?\d{3}[\s\-.]?\d{4}      # main number
    (?:\s*(?:x|ext\.?|extension)\s*\d{1,5})?
    |
    \b\d{3}[\s\-.]\d{4}\b           # 7-digit local
    |
    \b\d{10}\b                      # 10 digits in a row
)
""", re.VERBOSE | re.IGNORECASE)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 telephone_regexp.py input.txt")
        sys.exit(1)

    infile = sys.argv[1]
    with open(infile, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    matches = []
    for m in PHONE_REGEX.finditer(text):
        val = m.group(0).strip()
        val = re.sub(r"[.,;:]+$", "", val)
        matches.append(val)

    seen, uniq = set(), []
    for m in matches:
        if m not in seen:
            seen.add(m)
            uniq.append(m)

    for m in uniq:
        print(m)

    with open("telephone_output.txt", "w", encoding="utf-8") as out:
        for m in uniq:
            out.write(m + "\n")

if __name__ == "__main__":
    main()
