import re, xml.etree.ElementTree as ET, sys

fn = "submission.xml"
if len(sys.argv) > 1:
    fn = sys.argv[1]

tree = ET.parse(fn)
root = tree.getroot()

# get the speech text
text = root.find("TEXT").text
if text is None:
    print("No TEXT found.")
    sys.exit(1)

tags = root.find("TAGS")
cursor = 0
for adj in tags.findall("ADJECTIVE"):
    word = adj.get("text")
    if not word:
        continue
    # find word after the cursor
    m = re.search(re.escape(word), text[cursor:])
    if not m:
        m = re.search(re.escape(word), text[cursor:], re.IGNORECASE)
    if not m:
        print(f"Could not find {word}")
        continue
    start = cursor + m.start()
    end = start + len(word)
    adj.set("spans", f"{start}~{end}")
    cursor = end

tree.write(fn, encoding="utf-8", xml_declaration=True)
print("Spans filled into", fn)
