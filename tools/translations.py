"""Checks the translated Locales/<lang>.lua files.

The language files come from the public NeedRoll-Locales repository, where
players send translations. They run as Lua inside every player's game, so
each line must be a plain phrase and nothing else:

    L["Shopping List"] = "Einkaufsliste"

Anything that isn't a comment, a blank line, the standard header or a line
like that fails the check. A translation must also keep the key's %s, %d
(and the like) in the same order, or :format() would break in game.

    py tools/translations.py                 check NeedRoll/Locales
    py tools/translations.py DIR             check DIR (a NeedRoll-Locales copy)
    py tools/translations.py DIR --summary   also print a Markdown table of
                                             how much of each language is done

Exits 1 when a file breaks a rule. Phrases the addon no longer uses are only
reported, since an English change leaves the old translation behind.
"""
import pathlib
import re
import sys

LOCALES = ("deDE", "esES", "esMX", "frFR", "itIT", "koKR", "ptBR", "ruRU", "zhCN", "zhTW")
NAMES = {
    "deDE": "German", "esES": "Spanish (Spain)", "esMX": "Spanish (Mexico)",
    "frFR": "French", "itIT": "Italian", "koKR": "Korean",
    "ptBR": "Portuguese (Brazil)", "ruRU": "Russian",
    "zhCN": "Chinese (Simplified)", "zhTW": "Chinese (Traditional)",
}
DEFAULT = pathlib.Path(__file__).resolve().parent.parent / "NeedRoll" / "Locales"

STRING = r'"((?:[^"\\\n]|\\["\\n])*)"'
PHRASE = re.compile(r'^L\[' + STRING + r'\] = ' + STRING + r'$')
ENGLISH = re.compile(r'^L\[' + STRING + r'\] = true$')
FORMAT = re.compile(r'%(?:%|[-+ #0]*\d*(?:\.\d+)?[a-zA-Z])')


def header(locale):
    return [
        "local _, ns = ...",
        'local L = ns.Phrases("%s")' % locale,
        "if not L then return end",
    ]


# The header language files had before ns.Phrases; still accepted.
def old_header(locale):
    return [
        "local _, ns = ...",
        'if GetLocale() ~= "%s" then return end' % locale,
        "local L = ns.L",
    ]


def code_lines(path):
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.rstrip()
        if line and not line.startswith("--"):
            yield number, line


def english(folder):
    keys = []
    for _, line in code_lines(folder / "enUS.lua"):
        match = ENGLISH.match(line)
        if match:
            keys.append(match.group(1))
    return keys


def specifiers(text):
    return [s for s in FORMAT.findall(text) if s != "%%"]


def check(folder, locale, known):
    errors, unused, done = [], [], set()
    path = folder / (locale + ".lua")
    if not path.exists():
        return ["missing file"], unused, done
    lines = list(code_lines(path))
    want = header(locale)
    if [line for _, line in lines[:3]] not in (want, old_header(locale)):
        errors.append("the file must start with these lines (after comments):\n    " + "\n    ".join(want))
        return errors, unused, done
    for number, line in lines[3:]:
        if line.startswith("--[["):
            errors.append("line %d: block comments aren't allowed, start each comment line with --" % number)
            continue
        match = PHRASE.match(line)
        if not match:
            errors.append('line %d: not a phrase line like L["English"] = "Translation": %s' % (number, line))
            continue
        key, value = match.groups()
        if key in done:
            errors.append("line %d: %s is translated twice" % (number, key))
        done.add(key)
        if specifiers(key) != specifiers(value):
            errors.append("line %d: keep %s in the translation, in the same order (found %s)" % (
                number, " ".join(specifiers(key)) or "no % codes", " ".join(specifiers(value)) or "none"))
        if key not in known:
            unused.append(key)
    return errors, unused, done & known


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    folder = pathlib.Path(args[0]) if args else DEFAULT
    if (folder / "Locales").is_dir():
        folder = folder / "Locales"
    known = set(english(folder))
    status = 0
    rows = []
    for locale in LOCALES:
        errors, unused, done = check(folder, locale, known)
        for error in errors:
            print("%s.lua: %s" % (locale, error))
            status = 1
        for key in unused:
            print("%s.lua: not used by NeedRoll any more: %s" % (locale, key))
        rows.append((locale, len(done)))
    if "--summary" in sys.argv:
        print("\n| Language | Translated |\n| --- | --- |")
        for locale, count in rows:
            print("| %s (%s) | %d of %d |" % (NAMES[locale], locale, count, len(known)))
    return status


if __name__ == "__main__":
    sys.exit(main())
