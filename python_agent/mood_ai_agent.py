#!/usr/bin/env python3
"""
Recommender.ai - Neural Mood & Genre Recommendation Agent
Analyzes natural language user mood, energy levels, emotional context, and social vibe to diagnose the ideal movie genres and recommend matching titles from the 146-item catalog.
"""

import re
import math
import random
from typing import Dict, List, Any, Optional
from recommender_model import MOVIES_CATALOG, compute_genre_vector, cosine_similarity

# 9 Curated Mood Presets
MOOD_PRESETS = {
    "cozy_comfort": {
        "id": "cozy_comfort",
        "emoji": "🛋️",
        "label": "Cozy Comfort & Burnout Relief",
        "subtitle": "Exhausted after a long week",
        "description": "Seeking warm, low-stress comfort, charming banter, and feel-good romance to recharge.",
        "prompt": "I'm exhausted and stressed from a long week. I want something cozy, heartwarming, witty and comforting to unwind with."
    },
    "laugh_out_loud": {
        "id": "laugh_out_loud",
        "emoji": "😂",
        "label": "Hard Laughs & Comedy",
        "subtitle": "Need an instant mood boost",
        "description": "High-dopamine comedic relief with fast-paced jokes, quirky situations, and vibrant characters.",
        "prompt": "I need a hard laugh! Give me a hilarious, laugh-out-loud comedy with sharp banter and funny moments."
    },
    "date_night": {
        "id": "date_night",
        "emoji": "🍷",
        "label": "Romantic Date Night",
        "subtitle": "Spark chemistry & romance",
        "description": "Irresistible romantic chemistry, captivating meet-cutes, and charming witty moments to share together.",
        "prompt": "It's date night! Looking for irresistible romantic chemistry, clever humor, and feel-good romance."
    },
    "mind_bender": {
        "id": "mind_bender",
        "emoji": "🤯",
        "label": "Mind-Bending Sci-Fi",
        "subtitle": "Plot twists & puzzle plots",
        "description": "Intellectual stimulation, timeline paradoxes, philosophical concepts, and reality-altering twists.",
        "prompt": "I want a mind-bending sci-fi mystery with crazy plot twists and deep concepts that will blow my mind."
    },
    "adrenaline_rush": {
        "id": "adrenaline_rush",
        "emoji": "⚡",
        "label": "High-Octane Adrenaline",
        "subtitle": "Pumping action & heists",
        "description": "Pulse-pounding kinetic action, slick heists, relentless pacing, and badass heroes.",
        "prompt": "Need high adrenaline! Fast-paced action, thrilling heists, badass characters, and explosive excitement."
    },
    "dark_mystery": {
        "id": "dark_mystery",
        "emoji": "🕯️",
        "label": "Neo-Noir & Psychological Thrills",
        "subtitle": "Late-night suspense & tension",
        "description": "Moody atmospheric tension, psychological mind games, detective puzzles, and dark secrets.",
        "prompt": "Feeling in the mood for a dark, suspenseful psychological thriller or gritty detective mystery."
    },
    "good_cry": {
        "id": "good_cry",
        "emoji": "💔",
        "label": "Emotional Catharsis",
        "subtitle": "Deeply moving & poignant",
        "description": "Deep feelings, poignant human connection, bittersweet beauty, and a cathartic tearjerker.",
        "prompt": "Feeling emotional and reflective, want a deeply moving, bittersweet drama about love, life, and connection."
    },
    "whimsical_escapism": {
        "id": "whimsical_escapism",
        "emoji": "🌴",
        "label": "Whimsical Escapism & Animation",
        "subtitle": "Pure imagination & magic",
        "description": "Escape reality with breathtaking visual animation, enchanting worlds, and uplifting soundtracks.",
        "prompt": "Want to escape reality with gorgeous animation, magical worlds, vibrant colors, and inspiring adventure."
    },
    "thoughtful_cinema": {
        "id": "thoughtful_cinema",
        "emoji": "💭",
        "label": "Auteur Masterpieces",
        "subtitle": "Award-winning storytelling",
        "description": "Impeccable cinematography, nuanced acting, deep philosophical themes, and visionary directing.",
        "prompt": "Looking for a rich, critically acclaimed cinematic masterpiece with phenomenal acting and deep storytelling."
    }
}

# Lexicon keyword weights for mood parsing (8-dimensional vector)
MOOD_KEYWORDS = {
    # 0: Sci-Fi [SciFi, Space, Cyberpunk, Mind-Bender, Future, AI]
    0: ["scifi", "sci-fi", "space", "alien", "galaxy", "future", "futuristic", "time travel", "timeline", "matrix", "mind-bending", "mind blown", "paradox", "quantum", "robot", "cyberpunk", "simulation", "interstellar", "dune", "philosophy", "cosmos", "existential", "technology", "artificial intelligence", "dimension", "multiverse"],
    
    # 1: Action [Action, Heist, Adrenaline, Fight, Superhero, Explosion]
    1: ["action", "adrenaline", "heist", "pumped", "badass", "fight", "combat", "gunfight", "explosive", "fast-paced", "hype", "superhero", "chase", "mission", "revenge", "assassin", "viking", "warrior", "thrill", "intensity", "martial arts", "badass", "speed", "blockbuster"],
    
    # 2: Thriller / Crime / Mystery [Detective, Whodunit, Psychological, Dark, Suspense]
    2: ["thriller", "suspense", "mystery", "crime", "detective", "investigation", "whodunit", "plot twist", "murder", "psychological", "serial killer", "dark", "gritty", "noir", "neo-noir", "secrets", "tension", "mafia", "gangster", "fbi", "police", "conspiracy", "twists", "eerie"],
    
    # 3: Romance [Love, Rom-Com, Chemistry, Dating, Heartfelt, Sweet, Flirty]
    3: ["romance", "romantic", "rom-com", "romcom", "love", "date night", "chemistry", "dating", "sweet", "crush", "wedding", "kiss", "heartwarming", "relationship", "cute", "flirty", "lovers", "soulmate", "couple", "butterflies", "enemies to lovers", "valentines", "wholesome", "heartfelt", "cozy", "soft"],
    
    # 4: Comedy [Funny, Laugh, Hilarious, Banter, Silly, Satire, Lighthearted]
    4: ["comedy", "funny", "laugh", "hilarious", "humor", "witty", "banter", "silly", "satire", "dramedy", "goofy", "lighthearted", "fun", "cheering", "chuckle", "jokes", "parody", "feel-good", "upbeat", "breezy", "entertaining", "happy", "smile"],
    
    # 5: Drama / Biography [Emotional, Deep, Moving, Tearjerker, Inspiring]
    5: ["drama", "emotional", "moving", "deep", "cry", "tearjerker", "bittersweet", "sad", "poignant", "heartbreaking", "inspiring", "biography", "true story", "historical", "period", "family", "grief", "human connection", "redemption", "masterpiece", "life", "loss", "meaning"],
    
    # 6: Animation / Family [Anime, Studio Ghibli, Whimsical, Colorful, Magic]
    6: ["animation", "animated", "anime", "cartoon", "ghibli", "pixar", "whimsical", "magical", "enchanting", "colorful", "family", "kids", "childhood", "fairytale", "spider-verse", "fantasy world", "dreamy", "aesthetic", "cozy animation"],
    
    # 7: Horror / Supernatural [Scary, Creepy, Spooky, Monster, Haunted]
    7: ["horror", "scary", "spooky", "creepy", "haunted", "ghost", "demon", "slasher", "nightmare", "eerie", "sinister", "supernatural", "frightening", "paranormal", "gore", "jump scare", "halloween", "disturbing", "macabre"]
}

VIBE_MODIFIERS = {
    "exhausted": {"energy": -0.45, "warmth": +0.55, "complexity": -0.35, "comedy_boost": 0.45, "romance_boost": 0.40},
    "tired": {"energy": -0.40, "warmth": +0.50, "complexity": -0.30, "comedy_boost": 0.35, "romance_boost": 0.30},
    "stressed": {"energy": -0.35, "warmth": +0.60, "complexity": -0.35, "comedy_boost": 0.45, "romance_boost": 0.35},
    "burnout": {"energy": -0.45, "warmth": +0.60, "complexity": -0.40, "comedy_boost": 0.50},
    "relax": {"energy": -0.30, "warmth": +0.45, "complexity": -0.20, "romance_boost": 0.30},
    "cozy": {"energy": -0.25, "warmth": +0.80, "romance_boost": 0.40, "comedy_boost": 0.30},
    "bored": {"energy": +0.45, "complexity": +0.40, "action_boost": 0.40, "mystery_boost": 0.35},
    "sad": {"energy": -0.25, "warmth": +0.30, "drama_boost": 0.55, "romance_boost": 0.30},
    "crying": {"energy": -0.25, "warmth": +0.20, "drama_boost": 0.65},
    "heartbroken": {"energy": -0.25, "warmth": +0.40, "romance_boost": 0.45, "drama_boost": 0.50},
    "hyped": {"energy": +0.80, "adrenaline": +0.85, "action_boost": 0.65},
    "excited": {"energy": +0.70, "adrenaline": +0.75, "action_boost": 0.55},
    "date": {"warmth": +0.70, "romance_boost": 0.75, "comedy_boost": 0.45},
    "alone": {"warmth": +0.35, "drama_boost": 0.30, "scifi_boost": 0.30},
    "curious": {"complexity": +0.75, "scifi_boost": 0.45, "mystery_boost": 0.45},
    "spooky": {"adrenaline": +0.60, "horror_boost": 0.70, "mystery_boost": 0.40}
}


def analyze_user_mood(query_text: str) -> Dict[str, Any]:
    """Analyzes freeform mood text into a structured emotion & genre diagnosis."""
    q_lower = query_text.lower()
    words = re.findall(r'\b[a-z\-]+\b', q_lower)
    
    # 8-dimensional target genre vector [SciFi, Action, Thriller, Romance, Comedy, Drama, Animation, Horror]
    weights = [0.10] * 8
    
    # 1. Match against keyword lexicon
    for genre_idx, kw_list in MOOD_KEYWORDS.items():
        score = 0.0
        for kw in kw_list:
            if kw in q_lower:
                score += 0.40
            if any(w == kw for w in words):
                score += 0.30
        weights[genre_idx] += score

    # 2. Check vibe modifiers
    energy_level = 50.0
    emotional_warmth = 50.0
    complexity_level = 50.0
    adrenaline_level = 50.0

    for mod_key, mod_vals in VIBE_MODIFIERS.items():
        if mod_key in q_lower:
            if "energy" in mod_vals:
                energy_level += mod_vals["energy"] * 30.0
            if "warmth" in mod_vals:
                emotional_warmth += mod_vals["warmth"] * 30.0
            if "complexity" in mod_vals:
                complexity_level += mod_vals["complexity"] * 30.0
            if "adrenaline" in mod_vals:
                adrenaline_level += mod_vals["adrenaline"] * 30.0
            
            # Boost specific genre indices
            if "romance_boost" in mod_vals: weights[3] += mod_vals["romance_boost"]
            if "comedy_boost" in mod_vals: weights[4] += mod_vals["comedy_boost"]
            if "drama_boost" in mod_vals: weights[5] += mod_vals["drama_boost"]
            if "action_boost" in mod_vals: weights[1] += mod_vals["action_boost"]
            if "scifi_boost" in mod_vals: weights[0] += mod_vals["scifi_boost"]
            if "mystery_boost" in mod_vals: weights[2] += mod_vals["mystery_boost"]
            if "horror_boost" in mod_vals: weights[7] += mod_vals["horror_boost"]

    # Normalize weights to range [0.05, 0.98]
    max_w = max(weights)
    if max_w > 0.10:
        norm_weights = [min(0.98, max(0.05, (w / max_w) * 0.95)) for w in weights]
    else:
        # Default balanced cozy feel-good if query is very short/unclear
        norm_weights = [0.20, 0.25, 0.30, 0.92, 0.88, 0.50, 0.40, 0.10]
        emotional_warmth = 80.0

    energy_level = round(min(98.0, max(15.0, energy_level)), 1)
    emotional_warmth = round(min(98.0, max(10.0, emotional_warmth)), 1)
    complexity_level = round(min(98.0, max(15.0, complexity_level)), 1)
    adrenaline_level = round(min(98.0, max(10.0, adrenaline_level)), 1)

    GENRE_NAMES = [
        "Sci-Fi & Cyberpunk",
        "Action & Adventure",
        "Thriller & Mystery",
        "Romance & Love",
        "Comedy & Satire",
        "Drama & Human Stories",
        "Animation & Epic Worlds",
        "Horror & Dark Suspense"
    ]

    GENRE_ICONS = ["🌌", "⚡", "🕵️‍♂️", "💖", "😂", "🎭", "✨", "🕯️"]

    genre_scores = []
    for idx, (g_name, icon, val) in enumerate(zip(GENRE_NAMES, GENRE_ICONS, norm_weights)):
        genre_scores.append({
            "genre_index": idx,
            "genre": g_name,
            "icon": icon,
            "affinity_pct": round(val * 100, 1),
            "weight": val
        })
    genre_scores.sort(key=lambda x: x["affinity_pct"], reverse=True)

    top_idx = genre_scores[0]["genre_index"]

    if top_idx == 3 or (top_idx == 4 and norm_weights[3] > 0.6):
        archetype = "The Heartfelt Romantic & Comfort Seeker 💖"
        vibe_tag = "Warmth, Charming Banter & Romantic Spark"
        insight = "You're craving feel-good emotional warmth, effortless chemistry, and delightful wit that uplifts your spirits and melts away daily fatigue."
        artwork_bias = "emotional"
    elif top_idx == 4:
        archetype = "The Pure Joy & Laughter Enthusiast 😂"
        vibe_tag = "High Energy, Clever Comedy & Dopamine Rush"
        insight = "You need high-dopamine comedic relief with fast-paced jokes, quirky situations, and zero existential heaviness."
        artwork_bias = "action"
    elif top_idx == 0:
        archetype = "The Cosmic Thinker & Mind-Bender Explorer 🌌"
        vibe_tag = "High-Concept Mystery & Intellectual Intrigue"
        insight = "Your mind is seeking puzzle-solving satisfaction, expansive worldbuilding, and thought-provoking philosophical layers."
        artwork_bias = "action"
    elif top_idx == 1:
        archetype = "The Adrenaline Thrill-Seeker ⚡"
        vibe_tag = "High-Octane Kinetic Action & Badass Spectacle"
        insight = "You want pure kinetic energy, pulse-pounding pacing, and visceral excitement to recharge your focus."
        artwork_bias = "action"
    elif top_idx == 2:
        archetype = "The Shadow Sleuth & Suspense Aficionado 🕵️‍♂️"
        vibe_tag = "Atmospheric Tension & Unpredictable Twists"
        insight = "You're primed for edge-of-your-seat tension, dark motives, and layered mystery where nothing is what it seems."
        artwork_bias = "action"
    elif top_idx == 5:
        archetype = "The Deep Cinephile & Cathartic Dreamer 🎭"
        vibe_tag = "Poignant Emotion & Masterful Storytelling"
        insight = "You're ready for an emotional cinematic journey with nuanced acting, deep resonance, and unforgettable human truth."
        artwork_bias = "emotional"
    elif top_idx == 6:
        archetype = "The Whimsical Dreamer & World Explorer ✨"
        vibe_tag = "Pure Imagination, Visual Magic & Heart"
        insight = "You're longing for imaginative escapism, vibrant art, and uplifting wonder that transports you to extraordinary realms."
        artwork_bias = "emotional"
    else:
        archetype = "The Midnight Chills Seeker 🕯️"
        vibe_tag = "Eerie Atmosphere & Visceral Fear"
        insight = "You want intense psychological suspense and spine-tingling dark thrills that keep you glued to the screen."
        artwork_bias = "action"

    return {
        "query": query_text,
        "archetype": archetype,
        "vibe_tag": vibe_tag,
        "insight": insight,
        "artwork_bias": artwork_bias,
        "metrics": {
            "energy_level": energy_level,
            "emotional_warmth": emotional_warmth,
            "complexity_level": complexity_level,
            "adrenaline_level": adrenaline_level
        },
        "target_vector": norm_weights,
        "top_genres": genre_scores[:3],
        "all_genres": genre_scores
    }


def generate_mood_reason(movie: Dict[str, Any], mood_analysis: Dict[str, Any]) -> str:
    """Generates an intelligent context-aware explanation for why this movie fits the user's mood."""
    genres = movie.get("genres", [])
    title = movie.get("title", "")
    sound = movie.get("sound_theme", "")
    director = movie.get("director", "")
    
    # Specific iconic callouts
    if title == "Anyone But You":
        return "✨ Sun-drenched Sydney beaches, hilarious fake-dating banter, and infectious pop guitar energy to melt all stress."
    if title == "The Holiday":
        return "❄️ Cozy snowy Surrey cottage, warm fireplaces, and Hans Zimmer strings for the ultimate comforting night in."
    if title == "Love Actually":
        return "❤️ Multi-layered London holiday charm, iconic romantic confessions, and uplifting orchestral strings."
    if title == "Pretty Woman":
        return "🌹 Classic Beverly Hills glamour, charming laugh-out-loud chemistry, and iconic romantic nostalgia."
    if title == "Clueless":
        return "🛍️ Effortlessly funny 90s makeover vibes, snappy dialogue, and vibrant upbeat energy."
    if title == "Set It Up":
        return "🍕 Breezy Manhattan rooftop romance, witty matchmaker banter, and charming modern chemistry."
    if title == "Sing Street":
        return "🎸 Uplifting 80s new wave band energy, youthful passion, and infectious optimism."
    if title == "Begin Again":
        return "🎶 Acoustic NYC street recording sessions, soulful music, and soothing emotional connection."
    if title == "Inception":
        return "🌀 Multilayered dream heist puzzle, breathtaking visual setpieces, and Hans Zimmer horns."
    if title == "Interstellar":
        return "🌌 Grand cosmic scale, emotional father-daughter bond, and transcendental organ music."
    if title == "Knives Out":
        return "🕵️ Autumnal mansion aesthetic, sharp eccentric humor, and a deliciously satisfying whodunit."
    if title == "Spirited Away":
        return "🏯 Spellbinding hand-drawn magic, soothing Joe Hisaishi piano, and timeless wonder."
    if title == "John Wick: Chapter 4":
        return "⚡ Masterclass kinetic martial arts, neon lighting, and relentless heart-pumping adrenaline."
    if title == "Mad Max: Fury Road":
        return "🔥 Pure non-stop kinetic spectacle, thunderous percussion, and relentless desert intensity."
    if title == "The Dark Knight":
        return "🃏 Legendary psychological tension, unforgettable performances, and edge-of-seat pacing."

    if "Romance" in genres and "Comedy" in genres:
        return f"✨ Charming wit, low-stress romance, and {sound.split('&')[0].strip()} for pure feel-good recharge."
    elif "Romance" in genres:
        return f"🌹 Deeply resonant romantic chemistry with a moving emotional arc to sweep you off your feet."
    elif "Comedy" in genres:
        return f"😂 Non-stop laughs and charismatic humor that will instantly lift your spirits."
    elif "Sci-Fi" in genres and "Mystery" in genres:
        return f"🤯 Mind-bending puzzle mechanics and jaw-dropping twists that will keep your gears turning."
    elif "Sci-Fi" in genres:
        return f"🌌 Visionary worldbuilding and conceptual scale for immersive escapism."
    elif "Action" in genres and "Thriller" in genres:
        return f"⚡ Heart-pounding suspense and masterclass kinetic sequences to surge your adrenaline."
    elif "Action" in genres:
        return f"🔥 High-octane thrill ride with explosive set-pieces and relentless entertainment value."
    elif "Crime" in genres or "Mystery" in genres:
        return f"🕵️ Layered detective storytelling and moody tension that will keep you guessing until the final scene."
    elif "Animation" in genres:
        return f"🎨 Breathtaking visual wonder, imaginative heart, and magical storytelling to enchant your evening."
    elif "Drama" in genres:
        return f"🎭 Masterclass performances and unforgettable emotional depth for a truly resonant watch."
    else:
        return f"🍿 Top-rated IMDb favorite perfectly calibrated with your diagnosed {mood_analysis['top_genres'][0]['genre']} vibe."


def get_mood_recommendations(query_text: str, top_k: int = 12) -> Dict[str, Any]:
    """Given a user mood description, analyzes the mood and scores the 146-catalog items."""
    mood_analysis = analyze_user_mood(query_text)
    target_vec = mood_analysis["target_vector"]
    q_lower = query_text.lower()
    q_words = set(re.findall(r'\b[a-z]{3,}\b', q_lower))

    scored_movies = []
    for m in MOVIES_CATALOG:
        m_vec = compute_genre_vector(m["genres"])
        vec_sim = cosine_similarity(target_vec, m_vec)
        
        # Keyword bonus
        m_text = f"{m['title']} {' '.join(m['genres'])} {m['director']} {m['plot']} {' '.join(m.get('match_keywords', []))} {m.get('sound_theme', '')}".lower()
        keyword_hits = sum(1 for w in q_words if w in m_text)
        keyword_boost = min(0.15, keyword_hits * 0.04)

        # Rating quality prior
        rating_boost = (float(m.get("rating", 7.0)) / 10.0) * 0.10

        # Total combined mood score
        final_score = (vec_sim * 0.76) + keyword_boost + rating_boost
        match_pct = round(min(99.4, max(55.0, (vec_sim * 0.84 + keyword_boost * 1.2 + 0.12) * 100)), 1)

        # Select poster based on artwork bias
        bias = mood_analysis["artwork_bias"]
        selected_poster = m["poster_variants"].get(bias, m["poster_variants"].get("emotional", list(m["poster_variants"].values())[0]))

        reason = generate_mood_reason(m, mood_analysis)

        scored_movies.append({
            **m,
            "match_pct": match_pct,
            "mood_score": round(final_score, 4),
            "ai_reason": reason,
            "selected_poster": selected_poster,
            "artwork_style": bias
        })

    scored_movies.sort(key=lambda x: x["mood_score"], reverse=True)

    return {
        "agent_name": "Recommender.ai",
        "mood_analysis": mood_analysis,
        "recommendations": scored_movies[:top_k],
        "total_catalog_count": len(MOVIES_CATALOG),
        "presets": MOOD_PRESETS
    }
