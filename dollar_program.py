#!/usr/bin/env python3
import re
import sys

# Improved regex for better recall
DOLLAR_REGEX = re.compile(r"""
(
    # $ followed by number, with optional commas/decimals, maybe split across lines, maybe unit
    \$\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s*\n?\s*(?:million|billion|thousand))?

    |   # plain numbers with 'million/billion/thousand dollars' (allow singular dollar)
    \d+(?:\.\d+)?\s*(?:million|billion|thousand)?\s+dollars?

    |   # numbers with just unit and singular dollar
    \d+(?:\.\d+)?\s*(?:million|billion|thousand)?\s+dollar

    |   # numbers with 'cents'
    \d+(?:\.\d+)?\s+cents?

    |   # year + dollars (like 1973 dollars)
    \d{4}\s+dollars?

    |   # word numbers + dollars/cents (catch singular & plural)
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

    # de-duplicate while preserving order
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
