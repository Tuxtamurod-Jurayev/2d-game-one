import os
import json

class ScoreManager:
    def __init__(self, save_path="saves/highscore.json"):
        self.save_path = save_path
        self.high_score = self.load_high_score()
        self.current_score = 0
        self.coins = 0

    def load_high_score(self):
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return int(data.get("high_score", 0))
        except Exception as e:
            print(f"[ScoreManager] Failed to load high score: {e}")
        return 0

    def save_high_score(self):
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f, indent=2)
        except Exception as e:
            print(f"[ScoreManager] Failed to save high score: {e}")

    def add_score(self, points):
        self.current_score += points
        if self.current_score > self.high_score:
            self.high_score = self.current_score

    def add_coin(self):
        self.coins += 1
        self.add_score(100)

    def reset_current(self):
        self.save_high_score()
        self.current_score = 0
        self.coins = 0
