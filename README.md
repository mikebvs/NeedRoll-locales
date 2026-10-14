# NeedRoll translations

[NeedRoll](https://www.curseforge.com/projects/1731901) is a loot browser
for WoW: Forever. This repository holds only its translations, so anyone can
fix or add phrases in their language. Merged translations ship with the next
NeedRoll release.

Questions, or not comfortable with GitHub? Come to the localization channels
on the NeedRoll Discord and post the fix there.

## Languages

| Language | File |
| --- | --- |
| German | [Locales/deDE.lua](Locales/deDE.lua) |
| Spanish (Spain) | [Locales/esES.lua](Locales/esES.lua) |
| Spanish (Mexico) | [Locales/esMX.lua](Locales/esMX.lua) |
| French | [Locales/frFR.lua](Locales/frFR.lua) |
| Italian | [Locales/itIT.lua](Locales/itIT.lua) |
| Korean | [Locales/koKR.lua](Locales/koKR.lua) |
| Portuguese (Brazil) | [Locales/ptBR.lua](Locales/ptBR.lua) |
| Russian | [Locales/ruRU.lua](Locales/ruRU.lua) |
| Chinese (Simplified) | [Locales/zhCN.lua](Locales/zhCN.lua) |
| Chinese (Traditional) | [Locales/zhTW.lua](Locales/zhTW.lua) |

The check on each pull request prints how much of every language is done.

## How to translate

[Locales/enUS.lua](Locales/enUS.lua) lists every English phrase NeedRoll
shows, grouped by the part of the addon it's in. It's updated from NeedRoll
automatically, so don't edit it.

To translate a phrase, add a line to your language's file with the English
on the left, copied exactly, and your translation on the right:

```lua
L["Shopping List"] = "Einkaufsliste"
L["Requires %s %d"] = "Benötigt %s %d"
```

- Keep `%s` (a name), `%d` (a number) and the like, **in the same order** as
  the English. You can move them within the sentence.
- Keep `\n` (a line break) and anything between `|c` and `|r` (a color) as
  they are.
- Use `\"` for a quote mark inside a phrase.
- Only phrase lines and `--` comments are allowed. Anything else fails the
  check, because these files run inside the game.
- A phrase you leave out shows in English, so partial translations are
  welcome.

Then open a pull request. On github.com you can do it all in the browser:
open your language's file, press the pencil, add your lines and choose
"Propose changes".

Names that come from the game itself (items, spells, zones, NPCs) are
already in your language and don't need translating here.

## Reporting a problem

Wrong, missing or cut-off text in your language: open an issue with the
"Translation problem" form, or post it in the Discord's localization
channels.

## License

GPL v3, the same as NeedRoll. By sending a translation you agree it's
shared under that license.
