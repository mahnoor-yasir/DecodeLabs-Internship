"""
Knowledge Hub ENTERPRISE GENERAL KNOWLEDGE QUIZ 
100% Pure Python & Tkinter Implementation (No External Dependencies Required)
"""

import os
import csv
import time
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import tkinter as tk
from tkinter import ttk, messagebox

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "flux_quiz.db"
EXPORTS_DIR = BASE_DIR / "exports"

EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = "Knowledge Hub Enterprise General Knowledge Quiz"
APP_VERSION = "v4.0.0-Tkinter"

THEMES = {
    "dark": {
        "bg_primary": "#0F172A",
        "bg_secondary": "#1E293B",
        "bg_card": "#334155",
        "accent_primary": "#2563EB",
        "accent_hover": "#1D4ED8",
        "text_primary": "#FFFFFF",
        "text_secondary": "#94A3B8",
        "success": "#10B981",
        "warning": "#F59E0B",
        "danger": "#EF4444"
    },
    "light": {
        "bg_primary": "#F8FAFC",
        "bg_secondary": "#E2E8F0",
        "bg_card": "#FFFFFF",
        "accent_primary": "#2563EB",
        "accent_hover": "#1D4ED8",
        "text_primary": "#0F172A",
        "text_secondary": "#64748B",
        "success": "#059669",
        "warning": "#D97706",
        "danger": "#DC2626"
    }
}

CATEGORIES = [
    "General Knowledge",
    "Science",
    "Technology",
    "History",
    "Sports",
    "Geography",
    "Python",
    "Mixed"
]

DIFFICULTIES = {
    "Easy": {"timer": 45},
    "Medium": {"timer": 30},
    "Hard": {"timer": 20},
    "Expert": {"timer": 12}
}

GRADE_SCALE = [
    (95, "A+", "🏆 Master Mind", "Perfect operational proficiency achieved."),
    (85, "A",  "🌟 Superior", "Exceptional subject area mastery."),
    (75, "B+", "👍 Very Good", "Strong knowledge retention displayed."),
    (65, "B",  "📈 Above Average", "Solid foundational performance."),
    (50, "C",  "📊 Average", "Passable. Focused revision recommended."),
    (35, "D",  "⚠️ Below Average", "Significant domain knowledge gaps."),
    (0,  "F",  "❌ Needs Review", "Immediate re-evaluation required.")
]

# ==============================================================================
# DATABASE MANAGER
# ==============================================================================

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    question TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_option TEXT NOT NULL,
                    explanation TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    category TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    time_taken INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

        self._seed_default_questions()

    def _seed_default_questions(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM questions")
            if cursor.fetchone()[0] < 30: # Seed robust dataset
                default_data = [
                    # General Knowledge (10 Questions)
                    ("General Knowledge", "Easy", "What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", "C", "Paris has been the capital of France since 987 AD."),
                    ("General Knowledge", "Medium", "Which country gifts the Trafalgar Square Christmas tree to the UK?", "Norway", "Denmark", "Sweden", "Finland", "A", "Norway donates the tree in gratitude for WWII support."),
                    ("General Knowledge", "Easy", "Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B", "Mars appears red due to iron oxide on its surface."),
                    ("General Knowledge", "Medium", "What is the largest organ in the human body?", "Heart", "Liver", "Skin", "Lungs", "C", "Skin is the largest external organ."),
                    ("General Knowledge", "Hard", "Which currency is used in Japan?", "Yuan", "Won", "Yen", "Ringgit", "C", "The official currency of Japan is the Yen."),
                    ("General Knowledge", "Easy", "How many continents are there on Earth?", "5", "6", "7", "8", "C", "Earth has seven main continents."),
                    ("General Knowledge", "Medium", "Which element is essential for human respiration?", "Nitrogen", "Oxygen", "Carbon", "Helium", "B", "Humans require oxygen for cellular respiration."),
                    ("General Knowledge", "Hard", "What is the smallest country in the world?", "Monaco", "Vatican City", "San Marino", "Liechtenstein", "B", "Vatican City is the smallest independent state."),
                    ("General Knowledge", "Easy", "Which language has the most native speakers?", "English", "Mandarin Chinese", "Spanish", "Hindi", "B", "Mandarin Chinese has the highest native speaker count."),
                    ("General Knowledge", "Medium", "In which year did World War II end?", "1942", "1945", "1948", "1950", "B", "WWII formally ended in 1945."),

                    # Science (10 Questions)
                    ("Science", "Medium", "What is the chemical symbol for Gold?", "Au", "Ag", "Fe", "Pb", "A", "Au comes from the Latin word 'Aurum'."),
                    ("Science", "Easy", "What gas do plants absorb during photosynthesis?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "C", "Plants take in CO2 and release O2."),
                    ("Science", "Easy", "What is H2O commonly known as?", "Hydrogen Peroxide", "Salt", "Water", "Methane", "C", "H2O is the chemical formula for water."),
                    ("Science", "Medium", "What is the speed of light approx in vacuum?", "300,000 km/s", "150,000 km/s", "1,000,000 km/s", "50,000 km/s", "A", "Light moves at approximately 3x10^8 meters per second."),
                    ("Science", "Hard", "What particle in an atom carries a positive charge?", "Electron", "Neutron", "Proton", "Photon", "C", "Protons have positive charge."),
                    ("Science", "Medium", "Which planet is closest to the Sun?", "Venus", "Earth", "Mercury", "Mars", "C", "Mercury is the innermost planet."),
                    ("Science", "Easy", "What is the freezing point of water in Celsius?", "0°C", "32°C", "-10°C", "100°C", "A", "Water freezes at 0 degrees Celsius."),
                    ("Science", "Hard", "What unit measures electrical resistance?", "Volt", "Ampere", "Ohm", "Watt", "C", "Resistance is measured in Ohms."),
                    ("Science", "Medium", "Which vitamin is synthesized via sunlight exposure?", "Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D", "D", "Sunlight induces Vitamin D synthesis in skin."),
                    ("Science", "Hard", "What is the primary gas in Earth's atmosphere?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Argon", "C", "Nitrogen makes up ~78% of Earth's atmosphere."),

                    # Technology (10 Questions)
                    ("Technology", "Easy", "Which programming language created Tkinter?", "C++", "Python", "Java", "Ruby", "B", "Tkinter is Python's standard GUI toolkit."),
                    ("Technology", "Hard", "Who is regarded as the father of modern Computer Science?", "Steve Jobs", "Alan Turing", "Bill Gates", "Charles Babbage", "B", "Alan Turing formalized concepts of algorithm and computation."),
                    ("Technology", "Medium", "What does 'HTTP' stand for?", "HyperText Transfer Protocol", "High Transfer Text Logic", "Hyperlink Text Process", "Hyper Terminal Text Program", "A", "HTTP is the foundation of data communication on the Web."),
                    ("Technology", "Easy", "What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Power User", "Control Process Unit", "A", "CPU acts as the primary processor in a computer."),
                    ("Technology", "Medium", "Which database engine is embedded inside Python standard library?", "PostgreSQL", "SQLite", "MySQL", "MongoDB", "B", "SQLite3 is included in Python standard library."),
                    ("Technology", "Hard", "What year was Python first released by Guido van Rossum?", "1989", "1991", "1995", "2000", "B", "Python was first released in 1991."),
                    ("Technology", "Easy", "What does RAM stand for?", "Read Access Memory", "Random Access Memory", "Run Application Module", "Rapid Action Memory", "B", "RAM provides volatile temporary storage."),
                    ("Technology", "Medium", "Which company developed the Android Operating System originally?", "Google", "Android Inc.", "Apple", "Microsoft", "B", "Android Inc. developed it before Google acquired it in 2005."),
                    ("Technology", "Easy", "What file extension is used for Python scripts?", ".py", ".js", ".html", ".cpp", "A", "Python source files end with .py."),
                    ("Technology", "Hard", "What does SQL stand for?", "Structured Query Language", "Sequential Query Logic", "System Quality Language", "Standard Query Link", "A", "SQL manages relational database operations.")
                ]
                cursor.executemany("""
                    INSERT INTO questions (category, difficulty, question, option_a, option_b, option_c, option_d, correct_option, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, default_data)
                conn.commit()

    def get_categories(self) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM questions")
            db_cats = [row[0] for row in cursor.fetchall()]
            all_cats = list(dict.fromkeys(CATEGORIES + db_cats))
            return all_cats

    def get_questions(self, category="Mixed", difficulty="Medium", limit=10) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if category == "Mixed":
                query = "SELECT * FROM questions"
                params = []
                if difficulty != "All":
                    query += " WHERE difficulty = ?"
                    params.append(difficulty)
                query += " ORDER BY RANDOM() LIMIT ?"
                params.append(limit)
                cursor.execute(query, params)
                res = [dict(row) for row in cursor.fetchall()]
            else:
                # Primary fetch matching category & difficulty
                query = "SELECT * FROM questions WHERE category = ?"
                params = [category]
                if difficulty != "All":
                    query += " AND difficulty = ?"
                    params.append(difficulty)
                query += " ORDER BY RANDOM() LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                res = [dict(row) for row in cursor.fetchall()]

                # Fallback if less than limit available
                if len(res) < limit:
                    existing_ids = [r['id'] for r in res]
                    needed = limit - len(res)
                    
                    # Fetch from same category regardless of difficulty
                    fallback_query = f"SELECT * FROM questions WHERE category = ? "
                    fb_params = [category]
                    if existing_ids:
                        placeholders = ",".join(["?"] * len(existing_ids))
                        fallback_query += f"AND id NOT IN ({placeholders}) "
                        fb_params.extend(existing_ids)
                    
                    fallback_query += "ORDER BY RANDOM() LIMIT ?"
                    fb_params.append(needed)
                    
                    cursor.execute(fallback_query, fb_params)
                    res.extend([dict(row) for row in cursor.fetchall()])

                # Secondary fallback from any category if category has fewer questions overall
                if len(res) < limit:
                    existing_ids = [r['id'] for r in res]
                    needed = limit - len(res)
                    placeholders = ",".join(["?"] * len(existing_ids)) if existing_ids else ""
                    
                    fallback_query = f"SELECT * FROM questions "
                    fb_params = []
                    if existing_ids:
                        fallback_query += f"WHERE id NOT IN ({placeholders}) "
                        fb_params.extend(existing_ids)
                    
                    fallback_query += "ORDER BY RANDOM() LIMIT ?"
                    fb_params.append(needed)
                    
                    cursor.execute(fallback_query, fb_params)
                    res.extend([dict(row) for row in cursor.fetchall()])

            return res

    def add_question(self, q_data: Dict[str, Any]) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO questions (category, difficulty, question, option_a, option_b, option_c, option_d, correct_option, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (q_data['category'], q_data['difficulty'], q_data['question'],
                      q_data['option_a'], q_data['option_b'], q_data['option_c'],
                      q_data['option_d'], q_data['correct_option'], q_data.get('explanation', '')))
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Failed to add question: {e}")
            return False

    def save_result(self, result_data: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leaderboard (player_name, score, total_questions, percentage, category, difficulty, grade, time_taken)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (result_data['player_name'], result_data['score'], result_data['total_questions'],
                  result_data['percentage'], result_data['category'], result_data['difficulty'],
                  result_data['grade'], result_data['time_taken']))
            conn.commit()

    def get_leaderboard(self, limit=50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, player_name, score, total_questions, percentage, category, difficulty, grade, timestamp
                FROM leaderboard ORDER BY id DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def delete_result(self, result_id: int) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM leaderboard WHERE id = ?", (result_id,))
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Failed to delete result: {e}")
            return False

    def clear_all_results(self) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM leaderboard")
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Failed to clear results: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(percentage), MAX(score), MIN(score) FROM leaderboard")
            row = cursor.fetchone()
            
            cursor.execute("SELECT category, COUNT(*) as count FROM leaderboard GROUP BY category")
            category_dist = {r['category']: r['count'] for r in cursor.fetchall()}

            return {
                "total_games": row[0] or 0,
                "avg_percentage": round(row[1] or 0, 1),
                "highest_score": row[2] or 0,
                "lowest_score": row[3] or 0,
                "category_distribution": category_dist
            }

# ==============================================================================
# QUIZ RUNTIME ENGINE
# ==============================================================================

class QuizSession:
    def __init__(self, player_name: str, questions: List[Dict[str, Any]], category: str, difficulty: str):
        self.player_name = player_name
        self.questions = questions
        self.category = category
        self.difficulty = difficulty
        self.time_per_question = DIFFICULTIES.get(difficulty, {}).get("timer", 30)
        
        self.current_index = 0
        self.score = 0
        self.user_answers = {}
        self.start_time = time.time()
        self.end_time = 0.0

    def get_current_question(self) -> Optional[Dict[str, Any]]:
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def submit_answer(self, selected_option: str) -> bool:
        q = self.get_current_question()
        if not q:
            return False

        self.user_answers[self.current_index] = selected_option
        is_correct = (selected_option == q['correct_option'])
        if is_correct:
            self.score += 1
        return is_correct

    def next_question(self) -> bool:
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            return True
        return False

    def finish_quiz(self) -> Dict[str, Any]:
        self.end_time = time.time()
        total_q = len(self.questions)
        time_taken = int(self.end_time - self.start_time)
        percentage = round((self.score / total_q) * 100, 2) if total_q > 0 else 0.0

        grade_letter = "F"
        title = "Needs Review"
        message = "Re-evaluation recommended."
        for min_val, g, t, m in GRADE_SCALE:
            if percentage >= min_val:
                grade_letter, title, message = g, t, m
                break

        return {
            "player_name": self.player_name,
            "score": self.score,
            "total_questions": total_q,
            "percentage": percentage,
            "category": self.category,
            "difficulty": self.difficulty,
            "grade": grade_letter,
            "grade_title": title,
            "grade_message": message,
            "time_taken": time_taken,
            "skipped": total_q - len(self.user_answers),
            "wrong": len(self.user_answers) - self.score
        }

# ==============================================================================
# REPORT EXPORTER
# ==============================================================================

class ReportExporter:
    @staticmethod
    def export_to_csv(result_data: Dict[str, Any]) -> str:
        file_path = EXPORTS_DIR / f"Quiz_Result_{result_data['player_name']}_{int(result_data['time_taken'])}.csv"
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Metric", "Value"])
                for key, val in result_data.items():
                    writer.writerow([key.replace("_", " ").title(), val])
            return str(file_path)
        except Exception as e:
            logging.error(f"CSV Export Error: {e}")
            return ""

    @staticmethod
    def export_to_txt(result_data: Dict[str, Any]) -> str:
        file_path = EXPORTS_DIR / f"Assessment_Report_{result_data['player_name']}.txt"
        try:
            with open(file_path, mode="w", encoding="utf-8") as file:
                file.write("=" * 60 + "\n")
                file.write("     FLUX ENTERPRISE QUIZ PRO - ASSESSMENT REPORT\n")
                file.write("=" * 60 + "\n\n")
                for k, v in result_data.items():
                    file.write(f"{k.replace('_', ' ').title():<20}: {v}\n")
                file.write("\n" + "=" * 60 + "\n")
            return str(file_path)
        except Exception as e:
            logging.error(f"TXT Export Error: {e}")
            return ""

# ==============================================================================
# SCREENS & VIEWS
# ==============================================================================

class HomeScreen(tk.Frame):
    def __init__(self, master, app_controller):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_ui()

    def _build_ui(self):
        c = self.theme_colors
        
        lbl_title = tk.Label(self, text=APP_NAME.upper(), font=("Helvetica", 16, "bold"), fg=c["accent_primary"], bg=c["bg_primary"])
        lbl_title.pack(pady=(15, 5))

        lbl_sub = tk.Label(self, text=f"Enterprise Assessment Engine | {APP_VERSION}", font=("Helvetica", 10), fg=c["text_secondary"], bg=c["bg_primary"])
        lbl_sub.pack(pady=(0, 15))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=20, highlightbackground=c["bg_card"], highlightthickness=1)
        card.pack(padx=30, pady=10, fill="both", expand=True)

        tk.Label(card, text="Player Identification:", font=("Helvetica", 11, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(10, 5))
        self.ent_name = tk.Entry(card, font=("Helvetica", 11), bg=c["bg_card"], fg=c["text_primary"], insertbackground=c["text_primary"])
        self.ent_name.pack(fill="x", pady=(0, 15))

        tk.Label(card, text="Domain Category:", font=("Helvetica", 11, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(5, 5))
        
        categories = self.controller.db.get_categories()
        self.cmb_category = ttk.Combobox(card, values=categories, state="readonly", font=("Helvetica", 11))
        self.cmb_category.set(categories[0] if categories else "General Knowledge")
        self.cmb_category.pack(fill="x", pady=(0, 15))

        tk.Label(card, text="Difficulty Grade:", font=("Helvetica", 11, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(5, 5))
        self.cmb_difficulty = ttk.Combobox(card, values=list(DIFFICULTIES.keys()), state="readonly", font=("Helvetica", 11))
        self.cmb_difficulty.set("Medium")
        self.cmb_difficulty.pack(fill="x", pady=(0, 20))

        btn_start = tk.Button(card, text="🚀 INITIALIZE 10-MCQ QUIZ SESSION", font=("Helvetica", 12, "bold"), fg="#FFFFFF", bg=c["accent_primary"], activebackground=c["accent_hover"], activeforeground="#FFFFFF", command=self._on_start, relief="flat", pady=8)
        btn_start.pack(fill="x", pady=(10, 10))

    def _on_start(self):
        name = self.ent_name.get().strip() or "Candidate"
        category = self.cmb_category.get()
        difficulty = self.cmb_difficulty.get()
        self.controller.start_quiz_session(name, category, difficulty)

class QuizScreen(tk.Frame):
    def __init__(self, master, app_controller, session):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.session = session
        self.theme_colors = THEMES[self.controller.current_theme]

        self.time_left = self.session.time_per_question
        self.timer_job = None
        self.selected_option = tk.StringVar(value="")

        self._build_ui()
        self._load_question()

    def _build_ui(self):
        c = self.theme_colors
        self.top_bar = tk.Frame(self, bg=c["bg_primary"])
        self.top_bar.pack(fill="x", padx=30, pady=(15, 5))

        self.lbl_progress = tk.Label(self.top_bar, text="", font=("Helvetica", 12, "bold"), fg=c["text_primary"], bg=c["bg_primary"])
        self.lbl_progress.pack(side="left")

        self.lbl_timer = tk.Label(self.top_bar, text="⏱️ 00s", font=("Helvetica", 12, "bold"), fg=c["warning"], bg=c["bg_primary"])
        self.lbl_timer.pack(side="right")

        self.card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=20, highlightbackground=c["bg_card"], highlightthickness=1)
        self.card.pack(fill="both", expand=True, padx=30, pady=10)

        self.lbl_question = tk.Label(self.card, text="", font=("Helvetica", 13, "bold"), fg=c["text_primary"], bg=c["bg_secondary"], wraplength=600, justify="left")
        self.lbl_question.pack(anchor="w", pady=(10, 20))

        self.radio_btns = {}
        for opt_key in ["A", "B", "C", "D"]:
            rb = tk.Radiobutton(self.card, text="", value=opt_key, variable=self.selected_option, font=("Helvetica", 11), fg=c["text_primary"], bg=c["bg_secondary"], selectcolor=c["bg_card"], activebackground=c["bg_secondary"], activeforeground=c["text_primary"], anchor="w", justify="left")
            rb.pack(fill="x", pady=6)
            self.radio_btns[opt_key] = rb

        btn_submit = tk.Button(self, text="Submit Answer ➔", font=("Helvetica", 11, "bold"), fg="#FFFFFF", bg=c["accent_primary"], activebackground=c["accent_hover"], activeforeground="#FFFFFF", command=self._on_submit, relief="flat", padx=15, pady=6)
        btn_submit.pack(side="right", padx=30, pady=(10, 20))

    def _load_question(self):
        q = self.session.get_current_question()
        if not q:
            self._finish()
            return

        total = len(self.session.questions)
        curr = self.session.current_index + 1
        self.lbl_progress.configure(text=f"Question {curr} of {total}")

        self.lbl_question.configure(text=q['question'])
        self.selected_option.set("")

        self.radio_btns["A"].configure(text=f"A) {q['option_a']}")
        self.radio_btns["B"].configure(text=f"B) {q['option_b']}")
        self.radio_btns["C"].configure(text=f"C) {q['option_c']}")
        self.radio_btns["D"].configure(text=f"D) {q['option_d']}")

        self._reset_timer()

    def _reset_timer(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
        self.time_left = self.session.time_per_question
        self._update_timer()

    def _update_timer(self):
        self.lbl_timer.configure(text=f"⏱️ {self.time_left:02d}s")
        if self.time_left <= 0:
            self._on_submit()
        else:
            self.time_left -= 1
            self.timer_job = self.after(1000, self._update_timer)

    def _on_submit(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)

        sel = self.selected_option.get()
        if sel:
            self.session.submit_answer(sel)

        if self.session.next_question():
            self._load_question()
        else:
            self._finish()

    def _finish(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
        results = self.session.finish_quiz()
        self.controller.db.save_result(results)
        self.controller.show_results(results)

class ResultScreen(tk.Frame):
    def __init__(self, master, app_controller, results: dict):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.results = results
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_ui()

    def _build_ui(self):
        c = self.theme_colors
        tk.Label(self, text="PERFORMANCE SUMMARY", font=("Helvetica", 18, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(pady=(15, 5))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=20, highlightbackground=c["bg_card"], highlightthickness=1)
        card.pack(fill="x", padx=30, pady=10)

        color = c["success"] if self.results['percentage'] >= 60 else c["danger"]
        tk.Label(card, text=f"GRADE: {self.results['grade']}", font=("Helvetica", 28, "bold"), fg=color, bg=c["bg_secondary"]).pack(pady=(10, 2))
        tk.Label(card, text=f"{self.results['grade_title']} — {self.results['grade_message']}", font=("Helvetica", 11, "italic"), fg=c["text_secondary"], bg=c["bg_secondary"]).pack(pady=(0, 15))

        stats_frame = tk.Frame(self, bg=c["bg_primary"])
        stats_frame.pack(fill="x", padx=30, pady=10)

        for i, (title, val) in enumerate([("Total Score", f"{self.results['score']}/{self.results['total_questions']}"), ("Accuracy", f"{self.results['percentage']}%"), ("Time Elapsed", f"{self.results['time_taken']}s")]):
            f = tk.Frame(stats_frame, bg=c["bg_card"], padx=15, pady=10)
            f.grid(row=0, column=i, padx=5, sticky="ew")
            tk.Label(f, text=val, font=("Helvetica", 16, "bold"), fg=c["accent_primary"], bg=c["bg_card"]).pack()
            tk.Label(f, text=title.upper(), font=("Helvetica", 9, "bold"), fg=c["text_secondary"], bg=c["bg_card"]).pack()
            stats_frame.grid_columnconfigure(i, weight=1)

        btn_frame = tk.Frame(self, bg=c["bg_primary"])
        btn_frame.pack(fill="x", padx=30, pady=(20, 10))

        tk.Button(btn_frame, text="📄 Export CSV", command=self._export_csv, bg=c["bg_card"], fg=c["text_primary"], relief="flat", padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📑 Export TXT", command=self._export_txt, bg=c["bg_card"], fg=c["text_primary"], relief="flat", padx=10, pady=5).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Return to Dashboard ➔", command=lambda: self.controller.navigate_to("home"), bg=c["accent_primary"], fg="#FFFFFF", relief="flat", padx=10, pady=5).pack(side="right", padx=5)

        self.lbl_status_msg = tk.Label(self, text="", font=("Helvetica", 10), bg=c["bg_primary"])
        self.lbl_status_msg.pack(pady=5)

    def _export_csv(self):
        path = ReportExporter.export_to_csv(self.results)
        if path:
            self.lbl_status_msg.configure(text=f"Exported to: {path}", fg=self.theme_colors["success"])

    def _export_txt(self):
        path = ReportExporter.export_to_txt(self.results)
        if path:
            self.lbl_status_msg.configure(text=f"Exported to: {path}", fg=self.theme_colors["success"])

class LeaderboardScreen(tk.Frame):
    def __init__(self, master, app_controller):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_ui()

    def _build_ui(self):
        c = self.theme_colors
        
        top_frame = tk.Frame(self, bg=c["bg_primary"])
        top_frame.pack(fill="x", padx=30, pady=(15, 10))
        
        tk.Label(top_frame, text="GLOBAL LEADERBOARD & RESULTS MANAGER", font=("Helvetica", 15, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(side="left")
        
        btn_clear_all = tk.Button(top_frame, text="🗑️ Clear All Results", command=self._clear_all, bg=c["danger"], fg="#FFFFFF", relief="flat", font=("Helvetica", 9, "bold"), padx=10, pady=4)
        btn_clear_all.pack(side="right")

        card = tk.Frame(self, bg=c["bg_secondary"], padx=10, pady=10)
        card.pack(fill="both", expand=True, padx=30, pady=(0, 15))

        # Setup Treeview for structured result management & delete option
        columns = ("id", "player", "score", "percentage", "category", "grade", "action")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("player", text="Player")
        self.tree.heading("score", text="Score")
        self.tree.heading("percentage", text="Accuracy")
        self.tree.heading("category", text="Category")
        self.tree.heading("grade", text="Grade")
        self.tree.heading("action", text="Action")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("player", width=120, anchor="w")
        self.tree.column("score", width=80, anchor="center")
        self.tree.column("percentage", width=90, anchor="center")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("grade", width=60, anchor="center")
        self.tree.column("action", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_delete_sel = tk.Button(self, text="❌ Delete Selected Result", command=self._delete_selected, bg=c["bg_card"], fg=c["danger"], relief="flat", font=("Helvetica", 10, "bold"), pady=6)
        btn_delete_sel.pack(pady=(0, 15))

        self._refresh_records()

    def _refresh_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        records = self.controller.db.get_leaderboard(limit=50)
        for row in records:
            self.tree.insert("", "end", iid=row['id'], values=(
                row['id'],
                row['player_name'],
                f"{row['score']}/{row['total_questions']}",
                f"{row['percentage']}%",
                row['category'],
                row['grade'],
                "Delete"
            ))

    def _delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a result row from the list to delete.")
            return

        result_id = int(selected_item[0])
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete result entry #{result_id}?"):
            if self.controller.db.delete_result(result_id):
                self._refresh_records()
                messagebox.showinfo("Success", "Result record deleted successfully.")

    def _clear_all(self):
        if messagebox.askyesno("Confirm Clear All", "Are you sure you want to permanently delete ALL quiz result history?"):
            if self.controller.db.clear_all_results():
                self._refresh_records()
                messagebox.showinfo("Success", "All results deleted.")

class StatisticsScreen(tk.Frame):
    def __init__(self, master, app_controller):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_ui()

    def _build_ui(self):
        c = self.theme_colors
        tk.Label(self, text="ANALYTICAL METRICS", font=("Helvetica", 18, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(pady=(15, 10))

        stats = self.controller.db.get_statistics()

        stats_frame = tk.Frame(self, bg=c["bg_primary"])
        stats_frame.pack(fill="x", padx=30, pady=5)

        for i, (title, val) in enumerate([("Sessions Played", str(stats['total_games'])), ("Avg Accuracy", f"{stats['avg_percentage']}%"), ("High Score", str(stats['highest_score']))]):
            f = tk.Frame(stats_frame, bg=c["bg_card"], padx=15, pady=10)
            f.grid(row=0, column=i, padx=5, sticky="ew")
            tk.Label(f, text=val, font=("Helvetica", 16, "bold"), fg=c["accent_primary"], bg=c["bg_card"]).pack()
            tk.Label(f, text=title.upper(), font=("Helvetica", 9, "bold"), fg=c["text_secondary"], bg=c["bg_card"]).pack()
            stats_frame.grid_columnconfigure(i, weight=1)

        canvas_card = tk.Frame(self, bg=c["bg_secondary"], padx=15, pady=15)
        canvas_card.pack(fill="both", expand=True, padx=30, pady=15)

        tk.Label(canvas_card, text="Attempts by Category", font=("Helvetica", 12, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(0, 10))

        canvas = tk.Canvas(canvas_card, bg=c["bg_primary"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        cat_dist = stats.get("category_distribution", {})
        if cat_dist:
            max_val = max(cat_dist.values()) or 1
            bar_width = 40
            gap = 25
            start_x = 30
            canvas_height = 150

            for i, (cat, count) in enumerate(cat_dist.items()):
                x0 = start_x + i * (bar_width + gap)
                bar_h = (count / max_val) * (canvas_height - 30)
                y0 = canvas_height - bar_h
                x1 = x0 + bar_width
                y1 = canvas_height

                canvas.create_rectangle(x0, y0, x1, y1, fill=c["accent_primary"], outline="")
                canvas.create_text(x0 + bar_width/2, y0 - 10, text=str(count), fill=c["text_primary"], font=("Helvetica", 9, "bold"))
                canvas.create_text(x0 + bar_width/2, canvas_height + 15, text=cat[:8], fill=c["text_secondary"], font=("Helvetica", 8))
        else:
            canvas.create_text(150, 75, text="Insufficient Data for Analytics", fill=c["text_secondary"], font=("Helvetica", 11, "italic"))

class AdminScreen(tk.Frame):
    def __init__(self, master, app_controller):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_ui()

    def _build_ui(self):
        c = self.theme_colors
        tk.Label(self, text="QUESTION & CATEGORY CREATOR PORTAL", font=("Helvetica", 16, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(pady=(10, 5))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=10)
        card.pack(fill="both", expand=True, padx=30, pady=5)

        tk.Label(card, text="Category Name (Select Existing or Type New):", font=("Helvetica", 9, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(2, 0))
        
        categories = self.controller.db.get_categories()
        self.cmb_cat = ttk.Combobox(card, values=categories, font=("Helvetica", 10))
        self.cmb_cat.set(categories[0] if categories else "General Knowledge")
        self.cmb_cat.pack(fill="x", pady=2)

        tk.Label(card, text="Question Statement:", font=("Helvetica", 9, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(2, 0))
        self.ent_q = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_q.insert(0, "Enter question text...")
        self.ent_q.pack(fill="x", pady=2)

        tk.Label(card, text="Options:", font=("Helvetica", 9, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(2, 0))
        self.ent_a = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_a.insert(0, "Option A")
        self.ent_a.pack(fill="x", pady=1)

        self.ent_b = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_b.insert(0, "Option B")
        self.ent_b.pack(fill="x", pady=1)

        self.ent_c = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_c.insert(0, "Option C")
        self.ent_c.pack(fill="x", pady=1)

        self.ent_d = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_d.insert(0, "Option D")
        self.ent_d.pack(fill="x", pady=1)

        meta_frame = tk.Frame(card, bg=c["bg_secondary"])
        meta_frame.pack(fill="x", pady=4)

        tk.Label(meta_frame, text="Difficulty: ", font=("Helvetica", 9, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(side="left")
        self.cmb_diff = ttk.Combobox(meta_frame, values=list(DIFFICULTIES.keys()), state="readonly", width=10)
        self.cmb_diff.set("Medium")
        self.cmb_diff.pack(side="left", padx=2)

        tk.Label(meta_frame, text=" Correct Option: ", font=("Helvetica", 9, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(side="left")
        self.cmb_corr = ttk.Combobox(meta_frame, values=["A", "B", "C", "D"], state="readonly", width=5)
        self.cmb_corr.set("A")
        self.cmb_corr.pack(side="left", padx=2)

        self.ent_exp = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_exp.insert(0, "Explanation (optional)...")
        self.ent_exp.pack(fill="x", pady=2)

        btn_add = tk.Button(card, text="➕ Generate & Save MCQ to Category", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg=c["accent_primary"], activebackground=c["accent_hover"], command=self._add_q, relief="flat", pady=4)
        btn_add.pack(fill="x", pady=8)

        self.lbl_msg = tk.Label(card, text="", font=("Helvetica", 9), bg=c["bg_secondary"])
        self.lbl_msg.pack(pady=1)

    def _add_q(self):
        category = self.cmb_cat.get().strip()
        q, a, b, c, d = self.ent_q.get().strip(), self.ent_a.get().strip(), self.ent_b.get().strip(), self.ent_c.get().strip(), self.ent_d.get().strip()
        
        if not category or not all([q, a, b, c, d]):
            self.lbl_msg.configure(text="❌ Category and all option fields are required.", fg=self.theme_colors["danger"])
            return

        q_data = {
            "category": category,
            "difficulty": self.cmb_diff.get(),
            "question": q,
            "option_a": a, "option_b": b, "option_c": c, "option_d": d,
            "correct_option": self.cmb_corr.get(),
            "explanation": self.ent_exp.get().strip()
        }

        if self.controller.db.add_question(q_data):
            self.lbl_msg.configure(text=f"✅ MCQ added successfully to category '{category}'!", fg=self.theme_colors["success"])
            # Refresh category dropdown
            cats = self.controller.db.get_categories()
            self.cmb_cat['values'] = cats
        else:
            self.lbl_msg.configure(text="❌ Failed to register question.", fg=self.theme_colors["danger"])

class SettingsScreen(tk.Frame):
    def __init__(self, master, app_controller):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_ui()

    def _build_ui(self):
        c = self.theme_colors
        tk.Label(self, text="SYSTEM PREFERENCES", font=("Helvetica", 18, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(pady=(15, 10))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=20)
        card.pack(fill="both", expand=True, padx=30, pady=10)

        row1 = tk.Frame(card, bg=c["bg_secondary"])
        row1.pack(fill="x", pady=15)

        tk.Label(row1, text="UI Theme Mode:", font=("Helvetica", 12, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(side="left")

        btn_toggle = tk.Button(row1, text=f"Switch to {'Light' if self.controller.current_theme == 'dark' else 'Dark'} Mode", command=self._toggle_theme, bg=c["accent_primary"], fg="#FFFFFF", relief="flat", padx=10, pady=4)
        btn_toggle.pack(side="right")

    def _toggle_theme(self):
        new_theme = "light" if self.controller.current_theme == "dark" else "dark"
        self.controller.set_theme(new_theme)

# ==============================================================================
# MAIN CONTAINER & EXECUTABLE
# ==============================================================================

class MainWindow(tk.Frame):
    def __init__(self, master, app_controller):
        super().__init__(master, bg=THEMES[app_controller.current_theme]["bg_primary"])
        self.controller = app_controller
        self.theme_colors = THEMES[self.controller.current_theme]
        self._build_layout()

    def _build_layout(self):
        c = self.theme_colors
        self.sidebar = tk.Frame(self, width=180, bg=c["bg_secondary"])
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="KNOWLEDGE HUB", font=("Helvetica", 14, "bold"), fg=c["accent_primary"], bg=c["bg_secondary"]).pack(pady=(20, 20))

        nav_items = [
            ("🏠 Dashboard", "home"),
            ("🏆 Leaderboard", "leaderboard"),
            ("📊 Statistics", "statistics"),
            ("🛠️ Admin Portal", "admin"),
            ("⚙️ Settings", "settings")
        ]

        for label, route in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=label,
                anchor="w",
                font=("Helvetica", 10, "bold"),
                fg=c["text_primary"],
                bg=c["bg_secondary"],
                activebackground=c["bg_card"],
                activeforeground=c["text_primary"],
                relief="flat",
                command=lambda r=route: self.controller.navigate_to(r),
                pady=8,
                padx=15
            )
            btn.pack(fill="x", pady=2)

        self.view_container = tk.Frame(self, bg=c["bg_primary"])
        self.view_container.pack(side="right", fill="both", expand=True)

        self.controller.register_view_container(self.view_container)

class FluxAppController(tk.Tk):
    def __init__(self):
        super().__init__()

        self.current_theme = "dark"
        self.title(f"{APP_NAME} - {APP_VERSION}")
        self.geometry("900x600")
        self.minsize(850, 550)

        self.db = DatabaseManager()
        self.view_container = None
        self.current_view = None

        self.main_shell = MainWindow(self, self)
        self.main_shell.pack(fill="both", expand=True)
        self.navigate_to("home")

    def register_view_container(self, container):
        self.view_container = container

    def navigate_to(self, route: str):
        if not self.view_container:
            return

        if self.current_view:
            self.current_view.destroy()

        routes = {
            "home": HomeScreen,
            "leaderboard": LeaderboardScreen,
            "statistics": StatisticsScreen,
            "admin": AdminScreen,
            "settings": SettingsScreen
        }

        view_class = routes.get(route)
        if view_class:
            self.current_view = view_class(self.view_container, self)
            self.current_view.pack(fill="both", expand=True)

    def start_quiz_session(self, player_name: str, category: str, difficulty: str):
        questions = self.db.get_questions(category=category, difficulty=difficulty, limit=10)

        session = QuizSession(player_name, questions, category, difficulty)

        if self.current_view:
            self.current_view.destroy()

        self.current_view = QuizScreen(self.view_container, self, session)
        self.current_view.pack(fill="both", expand=True)

    def show_results(self, result_data: dict):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = ResultScreen(self.view_container, self, result_data)
        self.current_view.pack(fill="both", expand=True)

    def set_theme(self, theme_mode: str):
        self.current_theme = theme_mode
        self.main_shell.destroy()
        self.main_shell = MainWindow(self, self)
        self.main_shell.pack(fill="both", expand=True)
        self.navigate_to("settings")

if __name__ == "__main__":
    app = FluxAppController()
    app.mainloop()
