"""Optional helper: simple offline fallback tips used if the Flash call fails."""

FALLBACK_TIPS = {
    "weight loss": "Prioritise protein and fibre at every meal and drink water before meals to stay full.",
    "muscle gain": "Include protein in your post-workout meal and get 7-9 hours of sleep for recovery.",
    "flexibility": "Stay hydrated and add magnesium-rich foods such as nuts and leafy greens.",
    "general wellness": "Eat a balanced plate: half vegetables, a quarter protein, a quarter whole grains.",
}


def fallback_tip(goal: str) -> str:
    return FALLBACK_TIPS.get(goal.lower().strip(), FALLBACK_TIPS["general wellness"])
