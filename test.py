import json
import re

with open("dataset/clean/text_data.json", "r") as file:
    data = json.load(file)


pattern = re.compile(
    r"(\\u[0-9a-fA-F]{4})|[\ue000-\uf8ff]|([^\x00-\x7FążźćńółęśĄŻŹĆŃÓŁĘŚ])"
)

glyphs_to_code = {
    "\u0105": "ą",
    "\u0c17": "j",
    "\u0119": "ę",
    "\u01f3": "n",
    "\u0133": "j",
    "\u01f2": "Dz",
    "\ufb01": "fi",
    "\uf731": "1",
    "\uf738": "8",
    "\uf739": "9",
    "\u2026": "...",
    "\u201e": '"',
    "\u201d": '"',
    "\u2014": "-",
    "\uf76a": " ",
    "\uf76b": " ",
    "\uf734": " ",
    "\uf777": " ",
    "\uf769": " ",
    "\uf761": " ",
    "\uf774": " ",
    "\uf765": " ",
    "\uf764": " ",
    "\uf76d": " ",
    "\uf763": " ",
    "\uf77a": " ",
}


unique_chars: set[str] = set()
for i in range(len(data)):
    text = data[i]["text"]

    for glyph, unicode_char in glyphs_to_code.items():
        text = text.replace(glyph, unicode_char)

    matches: list[str] = []
    for match in pattern.finditer(text):
        groups = match.groups()
        for m in groups:
            if m is not None:
                matches.append(m)

    for char in matches:
        unique_chars.add(f"{char}: {char.encode('unicode_escape').decode('ascii')}")


for char in unique_chars:
    print(char)
