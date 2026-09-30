"""Built-in (offline) workout planner.

Used automatically when Gemini cannot answer (daily/minute quota reached, no internet,
missing key ...) so that FitBuddy always returns a usable 7-day plan.
The plan clearly states that it came from the built-in template.
"""
import re

INTENSITY = {
    "low":    {"sets": 2, "reps": "10-12", "rest": "60-90 sec", "cardio": 20},
    "medium": {"sets": 3, "reps": "10-12", "rest": "45-60 sec", "cardio": 30},
    "high":   {"sets": 4, "reps": "8-12",  "rest": "30-45 sec", "cardio": 40},
}

WARMUP = "Arm circles, marching in place, hip hinges and shallow squats (5-10 mins)"
COOLDOWN = "Slow static stretching, 30 seconds per muscle, and deep breathing (5 mins)"

# Each day: (title, [exercise, ...]).  Exercises with '{S}' and '{R}' get sets / reps.
# An empty list means a rest / recovery day.
GOAL_DAYS = {
    "weight loss": [
        ("Full Body Circuit", ["Bodyweight squats: {S} sets of {R} reps", "Push-ups (or wall push-ups): {S} sets of 8-12 reps",
                               "Dumbbell / backpack rows: {S} sets of {R} reps", "Plank: {S} sets of 30-45 sec"]),
        ("Cardio", ["Brisk walk, jog or cycling: {C} minutes at steady pace", "Finish with 5 minutes of easy walking"]),
        ("Lower Body & Core", ["Reverse lunges: {S} sets of {R} reps per leg", "Glute bridges: {S} sets of 15 reps",
                               "Mountain climbers: {S} sets of 30 sec", "Bicycle crunches: {S} sets of 15 reps per side"]),
        ("Active Recovery", []),
        ("Upper Body & Intervals", ["Dumbbell shoulder press: {S} sets of {R} reps", "Incline push-ups: {S} sets of 10 reps",
                                    "Jumping jacks: 4 rounds of 40 sec on / 20 sec off"]),
        ("Cardio & Core", ["Skipping, cycling or fast walk: {C} minutes", "Leg raises: {S} sets of 12 reps", "Side plank: {S} sets of 20-30 sec per side"]),
        ("Rest Day", []),
    ],
    "muscle gain": [
        ("Upper Body Push", ["Bench press or push-ups: {S} sets of {R} reps", "Incline dumbbell press: {S} sets of {R} reps",
                             "Overhead press: {S} sets of {R} reps", "Triceps dips / pushdowns: {S} sets of 12 reps"]),
        ("Lower Body", ["Barbell or goblet squats: {S} sets of {R} reps", "Romanian deadlifts: {S} sets of {R} reps",
                        "Walking lunges: {S} sets of 12 reps per leg", "Calf raises: {S} sets of 15 reps"]),
        ("Active Recovery", []),
        ("Upper Body Pull", ["Pull-ups or lat pulldowns: {S} sets of {R} reps", "Bent-over rows: {S} sets of {R} reps",
                             "Dumbbell curls: {S} sets of 12 reps", "Face pulls / rear-delt flies: {S} sets of 15 reps"]),
        ("Legs & Core", ["Front squats or leg press: {S} sets of {R} reps", "Hip thrusts: {S} sets of 12 reps",
                         "Hamstring curls: {S} sets of 12 reps", "Plank: {S} sets of 45-60 sec"]),
        ("Full Body Strength", ["Deadlifts: {S} sets of 6-8 reps", "Push press: {S} sets of 8 reps", "Farmer's carry: {S} rounds of 30 m"]),
        ("Rest Day", []),
    ],
    "flexibility": [
        ("Full Body Mobility Flow", ["Cat-cow: 2 sets of 10", "World's greatest stretch: 2 sets of 6 per side", "Deep squat hold: 3 x 30 sec"]),
        ("Hips & Hamstrings", ["Pigeon pose: 2 x 45 sec per side", "Seated forward fold: 3 x 45 sec", "Couch stretch: 2 x 45 sec per side"]),
        ("Light Strength & Balance", ["Bodyweight squats: {S} sets of {R} reps", "Single-leg balance: 3 x 30 sec per leg", "Bird-dog: {S} sets of 8 per side"]),
        ("Active Recovery", []),
        ("Shoulders & Back", ["Thread the needle: 2 x 8 per side", "Child's pose with side reach: 3 x 30 sec", "Wall angels: 3 x 10"]),
        ("Yoga Flow", ["Sun salutation A: 5 rounds", "Warrior I / II flow: 3 rounds per side", "Bridge pose: 3 x 30 sec"]),
        ("Rest Day", []),
    ],
    "general wellness": [
        ("Full Body Strength", ["Bodyweight squats: {S} sets of {R} reps", "Push-ups (or knee push-ups): {S} sets of 8-12 reps",
                                "Dumbbell rows: {S} sets of {R} reps", "Plank: {S} sets of 30-45 sec"]),
        ("Cardio", ["Brisk walk, jog or cycling: {C} minutes"]),
        ("Mobility & Core", ["Cat-cow: 2 sets of 10", "Dead bug: {S} sets of 10 per side", "Glute bridges: {S} sets of 15 reps"]),
        ("Active Recovery", []),
        ("Lower Body & Balance", ["Split squats: {S} sets of {R} reps per leg", "Step-ups: {S} sets of 10 per leg", "Single-leg balance: 3 x 30 sec"]),
        ("Cardio & Yoga", ["Easy cardio: {C} minutes", "Yoga flow: 15 minutes"]),
        ("Rest Day", []),
    ],
}


def _key(goal: str) -> str:
    g = (goal or "").lower()
    if "loss" in g or "fat" in g:
        return "weight loss"
    if "muscle" in g or "gain" in g or "strength" in g:
        return "muscle gain"
    if "flex" in g or "mobil" in g or "yoga" in g:
        return "flexibility"
    return "general wellness"


def _reason(text: str) -> str:
    t = (text or "").lower()
    if "quota" in t or "rate" in t or "429" in t:
        return "Gemini quota/rate limit reached"
    if "key" in t:
        return "Gemini API key problem"
    return "Gemini was unavailable"


def build_plan(user_input: dict, reason: str = "") -> str:
    p = INTENSITY.get(str(user_input.get("intensity", "medium")).lower(), INTENSITY["medium"])
    key = _key(user_input.get("goal", ""))
    lines = [
        f"NOTE: {_reason(reason)}, so this plan was created by FitBuddy's built-in template instead of Gemini.",
        "",
        f"## 7-Day {key.title()} Workout Plan ({str(user_input.get('intensity', 'medium')).title()} Intensity)",
        f"Prepared for age {user_input.get('age')}, weight {user_input.get('weight')} kg.",
        "",
    ]
    for i, (title, ex) in enumerate(GOAL_DAYS[key], start=1):
        lines.append(f"Day {i}: {title}")
        if not ex:
            if "Rest" in title:
                lines += ["* Full rest. Sleep 7-9 hours, hydrate well and eat enough protein."]
            else:
                lines += ["* Easy 20-30 minute walk, light stretching or foam rolling to aid recovery."]
            lines.append("")
            continue
        lines.append(f"Warm-up: {WARMUP}")
        lines.append("Main Workout:")
        for e in ex:
            lines.append("* " + e.format(S=p["sets"], R=p["reps"], C=p["cardio"]))
        if any("{S}" in e for e in ex):
            lines.append(f"* Rest between sets: {p['rest']}")
        lines.append(f"Cooldown: {COOLDOWN}")
        lines.append("")
    return "\n".join(lines).strip()


# ------------------------------------------------------------ feedback
_ADDONS = [
    (r"cardio|run|running|fat|endurance", "* Added from feedback - Extra cardio: 15 minutes of brisk walking, cycling or skipping"),
    (r"yoga|stretch|flexib|mobility", "* Added from feedback - Yoga / mobility flow: 15 minutes"),
    (r"abs|core|plank", "* Added from feedback - Core finisher: plank 3 x 45 sec and leg raises 3 x 12"),
    (r"\blegs?\b|lower body|glute", "* Added from feedback - Extra lower-body work: walking lunges 3 x 12 per leg"),
    (r"arms?|biceps|triceps|shoulder|chest|upper body", "* Added from feedback - Extra upper-body work: push-ups 3 x 10 and dumbbell curls 3 x 12"),
]


def _split_days(plan: str):
    parts = re.split(r"(?im)^(?=[#*\s]*Day\s*\d)", plan)
    head, days = parts[0], [p for p in parts[1:] if p.strip()]
    return head, days


def _insert_before_cooldown(block: str, extra: str) -> str:
    m = re.search(r"(?im)^[ \t]*[*\-]?[ \t]*\**cooldown", block)
    if not m:
        return block
    return block[:m.start()] + extra + "\n" + block[m.start():]


def apply_feedback(plan: str, feedback: str, reason: str = "") -> str:
    fb = (feedback or "").lower()
    head, days = _split_days(plan)
    # drop an older note/header so notes do not pile up
    head = re.sub(r"(?im)^NOTE:.*\n?", "", head).lstrip("\n")
    header = (f"NOTE: {_reason(reason)}, so this plan was updated by FitBuddy's built-in template.\n"
              f"Feedback applied: \"{feedback.strip()}\"\n\n")
    if len(days) < 7:  # unfamiliar layout - keep plan and add coaching notes
        notes = [x for pat, x in _ADDONS if re.search(pat, fb)] or ["* Keep the plan and progress gradually each week."]
        return header + plan.strip() + "\n\nAdjustments from your feedback:\n" + "\n".join(notes)

    wants_rest = re.search(r"rest|recover|tired|sore|fatigue|too much|exhaust", fb)
    easier = re.search(r"easy|easier|beginner|too hard|difficult|less intense", fb)
    harder = re.search(r"harder|more intense|challeng|too easy|advanced", fb)
    shorter = re.search(r"short|quick|less time|time", fb)

    out = []
    for idx, block in enumerate(days, start=1):
        first = block.splitlines()[0].lower()
        is_rest = "rest" in first or "recovery" in first
        if wants_rest and idx in (3, 6) and not is_rest:
            block = f"Day {idx}: Rest Day (added from feedback)\n* Full rest, light stretching and good sleep.\n\n"
        elif not is_rest:
            for pat, extra in _ADDONS:
                if re.search(pat, fb):
                    block = _insert_before_cooldown(block, extra)
            if easier:
                block = _insert_before_cooldown(block, "* Added from feedback - Easier option: do one set less per exercise and rest 15 sec longer")
            if harder:
                block = _insert_before_cooldown(block, "* Added from feedback - Progression: add one set to every exercise")
            if shorter:
                block = _insert_before_cooldown(block, "* Added from feedback - Short on time: keep the session to about 30 minutes")
        out.append(block if block.endswith("\n") else block + "\n")
    return header + head.strip() + ("\n\n" if head.strip() else "") + "\n".join(out).strip()
