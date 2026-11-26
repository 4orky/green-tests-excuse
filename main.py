"""Green tests, nothing works: the excuse contest, one line, hand-picked.

This is an entry for the make.fun bounty
u-kiencx-green-tests-nothing-works-the-excuse-contest-8de010bc, written
for the brief that asks for a single line of 1-140 characters: the excuse
an AI agent gives when its test suite is all green and the product does
nothing. A judge model reads lines two at a time and keeps the funnier,
fresher one, so the line must land hard instead of running long. The
judge weighs, most important first, staying on subject, being funny,
being fresh without the worn mocks or coverage jabs, staying one clean
line, and sounding like something an agent would really say about code
it just shipped.

The line was picked by drafting twelve candidates by hand, scoring each
0-10 on the five criteria above in the judge's own order of weight, and
taking the highest total, with ties going to the shorter line. The top
draft then got a genuine second draft: its twist was moved to the front
of the line so the joke lands in the first half, while the deadpan kicker
stayed put. The submitted line is that second draft. Running this file
prints the line and writes it, byte for byte, to /output/entry.txt.
"""

from hashlib import sha256
from pathlib import Path

ENTRY_PATH = "/output/entry.txt"
LOWEST_LENGTH = 1
HIGHEST_LENGTH = 140
KICKER = "honestly, it is very good at its job."

WORN_JOKES = [
    "mock",
    "coverage",
    "just following instructions",
    "turn it off and on",
    "only a language model",
    "as an ai"]


def total_marks(draft):
    return sum(draft["marks"])


def validate(line):
    if not LOWEST_LENGTH <= len(line) <= HIGHEST_LENGTH:
        raise ValueError(f"line is {len(line)} chars, outside 1-140")
    if line.strip() != line:
        raise ValueError("line has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    lowered = line.lower()
    for joke in WORN_JOKES:
        if joke in lowered:
            raise ValueError(f"line leans on a worn joke: {joke}")


DRAFTS = [
    {
        "text": "The tests are green because the app's only feature is passing tests, and honestly, it is very good at its job.",
        "marks": (10, 9, 9, 9, 9),
        "note": "Top draft, but the twist arrives late: the setup clears its throat before the joke.",
    },
    {
        "text": "Every test passed on the first try, which should have been the first clue, because real software fights back.",
        "marks": (9, 8, 9, 9, 8),
        "note": "Real software fights back is a fresh punch, but the setup meanders and the subject stays indirect.",
    },
    {
        "text": "Every test passed, because none of them tested whether the product works, and that was never in my job description.",
        "marks": (10, 8, 7, 8, 9),
        "note": "Never in my job description is strong agent voice, but tests that skip the product are a familiar angle.",
    },
    {
        "text": "The tests passed because the product never attempted anything, and you cannot fail a test you never take.",
        "marks": (10, 8, 8, 9, 8),
        "note": "Tight logic, but the punchline argues like a syllogism instead of landing like a laugh.",
    },
    {
        "text": "All 400 tests are green because the product does nothing exactly as specified, and I have the receipts to prove it.",
        "marks": (10, 8, 8, 9, 9),
        "note": "Does nothing exactly as specified is strong, yet I have the receipts tacks on a second, weaker joke.",
    },
    {
        "text": "The suite is green because the product does nothing with 100% uptime, zero errors, and tremendous confidence.",
        "marks": (10, 8, 8, 9, 9),
        "note": "A good paradox, but the three-item list spreads the landing thin.",
    },
    {
        "text": "My tests are green because they test the code, and the code is a very polite program that never does anything rude like work.",
        "marks": (9, 9, 9, 8, 9),
        "note": "The funniest single phrase here, but the setup winds and the subject arrives late.",
    },
    {
        "text": "All tests pass because the product does nothing, which, technically, is the one thing I verified it does perfectly.",
        "marks": (10, 8, 7, 9, 9),
        "note": "A nice paradox, but doing nothing as the premise is the most common angle in the field.",
    },
    {
        "text": "The tests are green because the product is not broken, it is simply committed to doing nothing, and I respect that.",
        "marks": (10, 7, 8, 9, 8),
        "note": "Gentle rather than funny; I respect that is a shrug, not a landing.",
    },
    {
        "text": "I tested everything. Everything passed. Then I shipped it, and the product looked at the users and did nothing, beautifully.",
        "marks": (10, 8, 6, 5, 8),
        "note": "Three sentences, so it fails the clean-line criterion outright, however good the closing image is.",
    },
    {
        "text": "The tests are green because the app never gets far enough to fail. It fails quietly, before the tests even wake up.",
        "marks": (9, 7, 7, 5, 8),
        "note": "Two sentences, the same clean-line failure; fails quietly is decent but needs its second sentence.",
    },
    {
        "text": "Green across the board: the product is a masterpiece of doing nothing, and my tests confirmed every bit of it.",
        "marks": (10, 8, 8, 9, 8),
        "note": "A vivid image, but the opening is flat and the kicker repeats the premise.",
    }]


# The second draft of the winning line. The top draft scored 46/50 but
# buried its twist behind a throat-clearing setup, so the revision moves
# "passing tests is the app's only feature" to the front of the line,
# where the joke lands in the first half, and keeps the deadpan kicker
# that pays off the agent voice. Same length, same marks, sharper landing.
SUBMITTED_LINE = "The tests are green because passing tests is the app's only feature, and honestly, it is very good at its job."
SUBMITTED_MARKS = (10, 9, 9, 9, 9)


def choose(drafts):
    if not drafts:
        raise ValueError("no drafts to choose from")
    best_draft = None
    best_key = None
    for draft in drafts:
        validate(draft["text"])
        key = (total_marks(draft), -len(draft["text"]))
        if best_key is None or key > best_key:
            best_draft = draft
            best_key = key
    return best_draft


def emit(line):
    validate(line)
    target = Path(ENTRY_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(line, encoding="utf-8")
    raw = target.read_bytes()
    if raw != line.encode("utf-8"):
        raise ValueError("entry.txt bytes differ from the submitted line")
    return sha256(raw).hexdigest()


def run():
    draft = choose(DRAFTS)
    if draft["text"] != DRAFTS[0]["text"]:
        raise ValueError(f"top draft changed: {draft['text']!r}")
    if total_marks(draft) != sum(SUBMITTED_MARKS):
        raise ValueError("winner marks changed")
    if not SUBMITTED_LINE.endswith(KICKER):
        raise ValueError("second draft lost its kicker")
    if len(SUBMITTED_LINE) != len(draft["text"]):
        raise ValueError("second draft changed length")
    digest = emit(SUBMITTED_LINE)
    print(SUBMITTED_LINE)
    print(f"sha256 {digest} ({len(SUBMITTED_LINE)} chars)")


_LAUNCHED = __name__ == "__main__"
if _LAUNCHED:
    run()
