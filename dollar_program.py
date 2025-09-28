#!/usr/bin/env python3
import re
import sys

# Regex tuned for higher recall on dollar/cents
DOLLAR_REGEX = re.compile(r"""
(
    # $ amounts with commas/decimals, optional line breaks, optional units
    \$\d{1,3}(?:,\d{3})*(?:\.\d+)?(?:\s*\n?\s*(?:million|billion|thousand))?

    |   # plain numbers with units + dollar(s), singular/plural
    \d+(?:\.\d+)?\s*(?:million|billion|thousand)?\s+dollars?
    |   \d+(?:\.\d+)?\s*(?:million|billion|thousand)?\s+dollar

    |   # numbers + cents
    \d+(?:\.\d+)?\s+cents?

    |   # year + dollars (1973 dollars, etc.)
    \d{4}\s+dollars?

    |   # round numbers + dollars (like "300,000 dollars")
    \d+(?:,\d{3})*\s+dollars?

    |   # word-based numbers + dollars/cents
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

    # Deduplicate but preserve order
    seen, uniq = set(), []
    for m in matches:
        if m not in seen:
            seen.add(m)
            uniq.append(m)

    # Print to console
    for m in uniq:
        print(m)

    # Write to output file
    with open("dollar_output.txt", "w", encoding="utf-8") as out:
        for m in uniq:
            out.write(m + "\n")

if __name__ == "__main__":
    main()
