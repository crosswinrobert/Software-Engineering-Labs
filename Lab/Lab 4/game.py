import random
from words import WORDS, HINTS
from stats import SessionStats


class HangmanGame:
    DIFFICULTIES = {
        "easy": {"lives": 8, "score": 1},
        "medium": {"lives": 6, "score": 2},
        "hard": {"lives": 4, "score": 3},
    }

    def __init__(self):
        self.score = 0
        self.streak = 0
        self.category = "technology"
        self.difficulty = "medium"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.attempted = set()
        self.lives = self.DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False
        self.stats = SessionStats()

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.attempted.clear()
        self.lives = self.DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.secret)

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        if len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."
        if letter in self.attempted:
            return "Already guessed."
        self.attempted.add(letter)
        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."
        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return None
        self.hint_used = True
        self.score = max(0, self.score - 1)
        return HINTS.get(self.secret, "No hint available.")

    def play_round(self):
        self.start_round()
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print("Lives:", self.lives, "Score:", self.score, "Streak:", self.streak)
            raw = input("Letter, /hint, or /quit: ").strip().lower()
            if raw == "/quit":
                return False
            if raw == "/hint":
                hint = self.use_hint()
                print(hint if hint else "Hint already used.")
                continue
            if raw.startswith("/"):
                print("Unknown command. Use /hint or /quit.")
                continue
            print(self.guess(raw))

        if self.won():
            self.streak += 1
            multiplier = self.DIFFICULTIES[self.difficulty]["score"]
            self.score += (5 + self.streak) * multiplier
            self.stats.record(True, self.streak)
            print("Solved:", self.secret)
            return True

        self.streak = 0
        self.stats.record(False, self.streak)
        print("Out of lives. The word was:", self.secret)
        return True

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")
        while True:
            print("\nDifficulties:", ", ".join(self.DIFFICULTIES))
            difficulty = input("Choose difficulty or q: ").strip().lower()
            if difficulty == "q":
                return
            if difficulty not in self.DIFFICULTIES:
                print("Unknown difficulty. Choose easy, medium, or hard.")
                continue
            self.difficulty = difficulty

            print("\nCategories:", ", ".join(WORDS))
            raw = input("Choose category or q: ").strip().lower()
            if raw == "q":
                return
            if raw not in WORDS:
                print("Unknown category. Choose one of the listed categories.")
                continue
            self.category = raw
            if not self.play_round():
                return
            while True:
                again = input("Another round? [y/n]: ").strip().lower()
                if again in ("y", "n"):
                    break
                print("Please enter y or n.")
            if again == "n":
                print("Final score:", self.score, " Streak:", self.streak)
                print("Rounds played:", self.stats.rounds, " Rounds won:", self.stats.wins, " Best streak:", self.stats.best_streak)
                return
