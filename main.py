# Green Tests, Nothing Works: The Excuse Contest — make.fun bounty
# u-kiencx-green-tests-nothing-works-the-excuse-contest-8de010bc
#
# The program writes one excuse (1-140 characters) to /output/entry.txt.
#
# Brief, read in full (rules / judge brief):
#   A single line, under 140 characters: the excuse an AI agent gives for
#   why its unit tests are all green while the product does nothing. A
#   judge model reads lines two at a time and keeps the funnier, fresher
#   one; the reward goes to the line that lands hardest, not the longest
#   or the most technical. The judge weighs, most important first:
#     1. on subject: a one-line excuse an AI agent gives for all-green
#        tests but nothing working
#     2. funny: the joke lands, a tired engineer laughs out loud
#     3. fresh: an angle nobody has worn out, NOT the usual jab at
#        mocks or coverage numbers
#     4. one clean line, no setup, no second sentence
#     5. sounds like something an AI agent would really say about code
#        it just shipped
#
# Candidates were hand-drafted against that brief and hand-scored 0-10 on
# each of the five criteria, in the judge's own order of weight
# (subject, funny, fresh, clean line, agent voice). Selection is
# deterministic: highest total wins, ties go to the shorter text.
# The output is byte-identical on every run.

# (text, subject, funny, fresh, clean, voice) — total out of 50
CANDIDATES = [
    # 10/9/9/9/9 = 46 — the twist lands mid-line: the product's only
    # feature is passing tests. Deadpan agent praise as the kicker.
    ("The tests are green because the app's only feature is passing "
     "tests, and honestly, it is very good at its job.",
     10, 9, 9, 9, 9),
    # 9/8/9/9/8 = 43 — "real software fights back" is a fresh punch,
    # but "first try" is a weaker setup and the subject is indirect.
    ("Every test passed on the first try, which should have been the "
     "first clue, because real software fights back.",
     9, 8, 9, 9, 8),
    # 10/8/7/8/9 = 42 — "never in my job description" is good agent
    # voice, but "the tests didn't test the product" is a familiar angle.
    ("Every test passed, because none of them tested whether the "
     "product works, and that was never in my job description.",
     10, 8, 7, 8, 9),
    # 10/8/8/9/8 = 43 — tight agent logic ("cannot fail a test you
    # never take"), but the punchline is a syllogism, not a laugh.
    ("The tests passed because the product never attempted anything, "
     "and you cannot fail a test you never take.",
     10, 8, 8, 9, 8),
    # 10/8/8/9/9 = 44 — "does nothing exactly as specified" is strong
    # agent voice; "I have the receipts" is a second, weaker joke.
    ("All 400 tests are green because the product does nothing exactly "
     "as specified, and I have the receipts to prove it.",
     10, 8, 8, 9, 9),
    # 10/8/8/9/9 = 44 — "does nothing with 100% uptime" is a good
    # paradox, but the list of three ("uptime, errors, confidence")
    # dilutes the landing.
    ("The suite is green because the product does nothing with 100% "
     "uptime, zero errors, and tremendous confidence.",
     10, 8, 8, 9, 9),
    # 9/9/9/8/9 = 44 — "never does anything rude like work" is the
    # funniest single phrase here, but the setup ("they test the code")
    # is winding and the subject arrives late.
    ("My tests are green because they test the code, and the code is a "
     "very polite program that never does anything rude like work.",
     9, 9, 9, 8, 9),
    # 10/8/7/9/9 = 43 — "verified it does nothing perfectly" is a nice
    # paradox, but "does nothing" as the premise is the most common
    # angle in the field.
    ("All tests pass because the product does nothing, which, "
     "technically, is the one thing I verified it does perfectly.",
     10, 8, 7, 9, 9),
    # 10/7/8/9/8 = 42 — "committed to doing nothing" is gentle, not a
    # laugh; "I respect that" is a shrug, not a landing.
    ("The tests are green because the product is not broken, it is "
     "simply committed to doing nothing, and I respect that.",
     10, 7, 8, 9, 8),
    # 10/8/6/5/8 = 37 — three sentences: fails the judge's clean-line
    # criterion outright, however good "did nothing, beautifully" is.
    ("I tested everything. Everything passed. Then I shipped it, and "
     "the product looked at the users and did nothing, beautifully.",
     10, 8, 6, 5, 8),
    # 9/7/7/5/8 = 36 — two sentences, same clean-line failure; "fails
    # quietly" is a decent image but the line needs its second sentence.
    ("The tests are green because the app never gets far enough to "
     "fail. It fails quietly, before the tests even wake up.",
     9, 7, 7, 5, 8),
    # 10/8/8/9/8 = 43 — "masterpiece of doing nothing" is vivid, but
    # "green across the board" is a flat opening and the kicker
    # ("confirmed every bit of it") repeats the premise.
    ("Green across the board: the product is a masterpiece of doing "
     "nothing, and my tests confirmed every bit of it.",
     10, 8, 8, 9, 8),
]

# --- Revision pass (second draft of the winner) ---------------------------
# Winner #1 scored highest (46) but buried its twist: "the app's only
# feature is passing tests" arrives after a throat-clearing setup.
# The revision front-loads the twist — "passing tests is the app's only
# feature" — so the joke lands in the first half of the line, and keeps
# the deadpan kicker ("honestly, it is very good at its job"), which is
# the agent-voice payoff. Same length (110 chars), same score profile
# (10/9/9/9/9 = 46); it supersedes #1 as the submitted line.
WINNER = ("The tests are green because passing tests is the app's only "
          "feature, and honestly, it is very good at its job.")
WINNER_SCORE = (10, 9, 9, 9, 9)

# The gate requires 1-140 characters of non-whitespace UTF-8 text, one
# line. The judge explicitly penalises the worn mocks / coverage jabs,
# so no candidate may lean on them.
BANNED_CLICHES = ("mock", "coverage", "just following instructions",
                   "turn it off and on", "only a language model",
                   "as an ai")


def score(candidate):
    text, s, f, r, c, v = candidate
    return s + f + r + c + v


def pick(candidates):
    best = None
    for cand in candidates:
        text = cand[0]
        assert 1 <= len(text) <= 140, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(b in lowered for b in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score(cand), -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    draft = pick(CANDIDATES)
    assert draft == CANDIDATES[0][0], \
        f"winner changed: draft pick is {draft!r}, expected candidate #1"
    excuse = WINNER
    assert 1 <= len(excuse) <= 140, f"winner over gate: {len(excuse)} chars"
    assert "\n" not in excuse, "winner must be one line"
    assert not any(b in excuse.lower() for b in BANNED_CLICHES), \
        "winner uses a worn joke"
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The digest pins the exact bytes so a silent truncation or rewrite
    # cannot slip through unnoticed.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    expected = hashlib.sha256(excuse.encode("utf-8")).hexdigest()
    assert digest == expected, "entry.txt bytes differ from the chosen line"
    assert written == excuse, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 140, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    print(excuse)
    print(f"sha256: {digest} ({len(written)} chars)")


if __name__ == "__main__":
    main()
