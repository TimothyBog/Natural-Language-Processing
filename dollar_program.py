#!/usr/bin/env python3
import re
import sys

# Better regex for complete dollar/cents expressions
DOLLAR_REGEX = re.compile(r"""
(
    # $ followed by number, optional commas/decimals, optional million/billion/thousand
    \$\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s*(?:million|billion|thousand))?

    |   # number with unit and 'dollars'
    \d+(?:\.\d+)?\s*(?:million|billion|thousand)?\s+dollars?

    |   # number with 'cents'
    \d+(?:\.\d+)?\s+cents?

    |   # word numbers + dollars/cents (e.g., "hundred dollars")
    (?:one|two|three|four|five|six|seven|eight|nine|ten|
       eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|
       twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|
       hundred|thousand|million|billion)(?:\s+[a-z]+)*\s+(?:dollars?|cents?)
)
""", re.IGNORECASE | re.VERBOSE)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dollar_program.py input.txt")
        sys.exit(1)

    infile = sys.argv[1]
    with open(infile, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    matches = []
    for m in DOLLAR_REGEX.finditer(text):
        val = m.group(1).strip()
        val = re.sub(r"[.,;:]+$", "", val)  # strip trailing punctuation
        matches.append(val)

    seen, uniq = set(), []
    for m in matches:
        if m not in seen:
            seen.add(m)
            uniq.append(m)

    # print to screen
    for m in uniq:
        print(m)

    # save to file
    with open("dollar_output.txt", "w", encoding="utf-8") as out:
        for m in uniq:
            out.write(m + "\n")

if __name__ == "__main__":
    main()
