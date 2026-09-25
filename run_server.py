#!/usr/bin/env python3
"""
Himanshu's Movie Directory - Movie Recommendation & Two-Tower ML Server (Port 8084)
Provides live REST APIs for user recommendations, AI mood & genre diagnosis, full movie catalog browsing, two-tower training simulations, and candidate funnel tracing.
"""

import http.server
import socketserver
import os
import sys
import json
import urllib.parse
import random
import math

PORT = 8084
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(DIRECTORY, "python_agent"))

from recommender_model import MOVIES_CATALOG, USER_PROFILES, get_recommendations_for_user
from mood_ai_agent import get_mood_recommendations, MOOD_PRESETS, analyze_user_mood


class MovieDirectoryHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "online",
                "app": "Himanshu's Movie Directory",
                "port": PORT,
                "catalog_size": len(MOVIES_CATALOG),
                "users_count": len(USER_PROFILES),
                "ai_agent": "Recommender.ai"
            }).encode("utf-8"))
            return

        if parsed.path == "/api/catalog":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "count": len(MOVIES_CATALOG),
                "movies": MOVIES_CATALOG
            }).encode("utf-8"))
            return

        if parsed.path == "/api/users":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(USER_PROFILES).encode("utf-8"))
            return

        if parsed.path == "/api/recommendations":
            user_id = params.get("user_id", ["u_romcom_fan"])[0]
            result = get_recommendations_for_user(user_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        if parsed.path == "/api/mood-presets":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(MOOD_PRESETS).encode("utf-8"))
            return

        if parsed.path == "/api/mood-recommend":
            query = params.get("q", ["cozy comfort and witty romcom"])[0]
            limit = int(params.get("limit", [12])[0])
            result = get_mood_recommendations(query, top_k=limit)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if parsed.path == "/api/mood-recommend":
            query = payload.get("query", "cozy comfort and witty romcom")
            limit = payload.get("limit", 12)
            result = get_mood_recommendations(query, top_k=limit)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        if parsed.path == "/api/train-step":
            epoch = payload.get("epoch", 1)
            decay = math.exp(-epoch / 10.0)
            train_loss = round(0.12 + 1.85 * decay + random.uniform(-0.02, 0.02), 4)
            val_loss = round(0.18 + 1.95 * decay + random.uniform(-0.03, 0.03), 4)
            recall_10 = round(min(0.92, 0.35 + 0.55 * (1 - decay) + random.uniform(-0.01, 0.01)), 4)
            ndcg_10 = round(min(0.88, 0.28 + 0.58 * (1 - decay) + random.uniform(-0.01, 0.01)), 4)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "recall_10": recall_10,
                "ndcg_10": ndcg_10
            }).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def run():
    server_address = ("", PORT)
    httpd = ThreadedHTTPServer(server_address, MovieDirectoryHandler)
    print("=" * 80)
    print(f"🎬  HIMANSHU'S MOVIE DIRECTORY — TWO-TOWER RECOMMENDATION ML SERVER")
    print(f"📡  Dashboard URL: http://localhost:{PORT}")
    print(f"📚  Total Movie Library: {len(MOVIES_CATALOG)} Movies")
    print(f"🤖  Recommender.ai Engine: Active")
    print("=" * 80)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == "__main__":
    run()

