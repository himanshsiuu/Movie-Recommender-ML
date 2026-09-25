# 🎬 Movie Recommender ML & Cinema Lounge

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Two-Tower ML](https://img.shields.io/badge/ML-Two--Tower%20Neural%20Embeddings-FF6F00.svg)](https://github.com/himanshsiuu/Movie-Recommender-ML)
[![Web Audio API](https://img.shields.io/badge/Audio-Web%20Audio%20Synthesis-00C7B7.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
[![YouTube Embeds](https://img.shields.io/badge/Previews-100%25%20Verified%20Embeds-FF0000.svg?logo=youtube)](https://www.youtube.com/)

A modern, full-stack movie & TV series recommendation platform powered by **Two-Tower Neural Embeddings**, **Dynamic Dynamic Artwork Selection**, **Web Audio Synthesized Soundscapes**, and **Verified Cinema Video Previews with Sound**.

---

## 🤖 Recommender.ai — Neural Mood & Genre Matcher

- **Natural Language Emotion Diagnosis**: Tell **Recommender.ai** your emotional state or current mood, and it infers your optimal 8D genre vector, archetype, and cognitive energy levels.
- **9 Quick Vibe Archetypes**: 1-click access to curated moods (*Cozy Comfort, Hard Laughs, Date Night, Mind-Bender, Adrenaline Rush, Dark Mystery, Emotional Catharsis, Whimsical Escapism, Auteur Masterpiece*).
- **Context-Aware Recommendations**: Handpicks titles with tailored AI explanations for why each movie matches your current vibe.

## ✨ Features

- **🧠 Two-Tower Neural Candidate Retrieval & Ranking**:
  - Encodes multi-dimensional user taste vectors and 8D content embeddings across genres (*Sci-Fi, Action, Thriller/Crime, Romance, Comedy, Drama/Bio, Animation/Anime, Horror*).
  - Multi-task optimization predicting click probability ($P_{\text{click}}$) and completion probability ($P_{\text{complete}}$).
  - Real-time cosine similarity and personalized feed generation.

- **🎞️ Cinema Clips & Audio Lounge**:
  - Live video preview trailers for all **146 catalog titles** (112 Movies & 34 TV Series).
  - 100% pre-validated against YouTube oEmbed APIs to prevent playback restrictions.
  - Interactive Web Audio API frequency-synthesizer providing custom genre acoustic themes (Acoustic Guitar, 80s Synthpop, Epic Cinematic Brass, Lo-Fi, Gothic Chants).

- **🎭 Adaptive Persona Engine**:
  - Instant persona switching (Emma, Alex Chen, Sarah Miller, Maya, Liam Vance, Noah Rivera).
  - Dynamic poster artwork biasing (`action` vs `emotional` framing).

- **📚 Expanded 146+ Title Catalog**:
  - 25+ curated Rom-Coms & Feel-Good classics (*Anyone But You, The Holiday, Love Actually, Pretty Woman, Clueless, Sing Street, Set It Up, Begin Again*, and more).
  - Comprehensive IMDb ratings, vote counts, director/cast listings, awards, and metascores.

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone git@github.com:himanshsiuu/Movie-Recommender-ML.git
cd Movie-Recommender-ML
```

### 2. Start the Server
```bash
python3 run_server.py
```

### 3. Open the Dashboard
Navigate to **`http://localhost:8084`** in your browser to browse the library, test persona recommendations, and listen to cinema audio previews.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/status` | `GET` | Health check, server status, and active catalog count |
| `/api/catalog` | `GET` | Retrieve full library with metadata, trailers, and audio themes |
| `/api/recommendations?user_id={id}` | `GET` | Generate personalized Two-Tower ML recommendations |

---

## 📄 License
MIT License © Himanshu
