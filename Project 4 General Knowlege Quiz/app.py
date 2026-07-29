"""
Knowledge Hub ENTERPRISE GENERAL KNOWLEDGE QUIZ - Graphical Interface (Tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app import (
    APP_NAME, APP_VERSION, THEMES, CATEGORIES, DIFFICULTIES,
    DatabaseManager, QuizSession, ReportExporter
)

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
        
        lbl_title = tk.Label(self, text=APP_NAME.upper(), font=("Helvetica", 18, "bold"), fg=c["accent_primary"], bg=c["bg_primary"])
        lbl_title.pack(pady=(20, 5))

        lbl_sub = tk.Label(self, text=f"Enterprise Assessment Engine | {APP_VERSION}", font=("Helvetica", 11), fg=c["text_secondary"], bg=c["bg_primary"])
        lbl_sub.pack(pady=(0, 20))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=20, highlightbackground=c["bg_card"], highlightthickness=1)
        card.pack(padx=40, pady=10, fill="both", expand=True)

        tk.Label(card, text="Player Identification:", font=("Helvetica", 11, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(10, 5))
        self.ent_name = tk.Entry(card, font=("Helvetica", 11), bg=c["bg_card"], fg=c["text_primary"], insertbackground=c["text_primary"])
        self.ent_name.pack(fill="x", pady=(0, 15))

        tk.Label(card, text="Domain Category:", font=("Helvetica", 11, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(5, 5))
        self.cmb_category = ttk.Combobox(card, values=CATEGORIES, state="readonly", font=("Helvetica", 11))
        self.cmb_category.set(CATEGORIES[0])
        self.cmb_category.pack(fill="x", pady=(0, 15))

        tk.Label(card, text="Difficulty Grade:", font=("Helvetica", 11, "bold"), fg=c["text_primary"], bg=c["bg_secondary"]).pack(anchor="w", pady=(5, 5))
        self.cmb_difficulty = ttk.Combobox(card, values=list(DIFFICULTIES.keys()), state="readonly", font=("Helvetica", 11))
        self.cmb_difficulty.set("Medium")
        self.cmb_difficulty.pack(fill="x", pady=(0, 20))

        btn_start = tk.Button(card, text="🚀 INITIALIZE QUIZ SESSION", font=("Helvetica", 12, "bold"), fg="#FFFFFF", bg=c["accent_primary"], activebackground=c["accent_hover"], activeforeground="#FFFFFF", command=self._on_start, relief="flat", pady=8)
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

        self.lbl_question = tk.Label(self.card, text="", font=("Helvetica", 14, "bold"), fg=c["text_primary"], bg=c["bg_secondary"], wraplength=600, justify="left")
        self.lbl_question.pack(anchor="w", pady=(10, 20))

        self.radio_btns = {}
        for opt_key in ["A", "B", "C", "D"]:
            rb = tk.Radiobutton(self.card, text="", value=opt_key, variable=self.selected_option, font=("Helvetica", 12), fg=c["text_primary"], bg=c["bg_secondary"], selectcolor=c["bg_card"], activebackground=c["bg_secondary"], activeforeground=c["text_primary"], anchor="w", justify="left")
            rb.pack(fill="x", pady=8)
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
        tk.Label(self, text="GLOBAL LEADERBOARD", font=("Helvetica", 18, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(pady=(15, 10))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=10, pady=10)
        card.pack(fill="both", expand=True, padx=30, pady=10)

        records = self.controller.db.get_leaderboard(limit=20)
        if not records:
            tk.Label(card, text="No records found in database.", font=("Helvetica", 11, "italic"), fg=c["text_secondary"], bg=c["bg_secondary"]).pack(pady=20)
            return

        for idx, row in enumerate(records, start=1):
            row_frame = tk.Frame(card, bg=c["bg_card"] if idx % 2 == 0 else c["bg_secondary"], pady=4)
            row_frame.pack(fill="x", pady=1)

            rank_str = f"#{idx}  {row['player_name']}"
            tk.Label(row_frame, text=rank_str, font=("Helvetica", 10), fg=c["text_primary"], bg=row_frame['bg'], width=22, anchor="w").pack(side="left", padx=10)
            tk.Label(row_frame, text=f"{row['score']}/{row['total_questions']}", font=("Helvetica", 10), fg=c["text_primary"], bg=row_frame['bg'], width=10).pack(side="left")
            tk.Label(row_frame, text=f"{row['percentage']}%", font=("Helvetica", 10), fg=c["text_primary"], bg=row_frame['bg'], width=10).pack(side="left")
            tk.Label(row_frame, text=row['grade'], font=("Helvetica", 10, "bold"), fg=c["accent_primary"], bg=row_frame['bg'], width=8).pack(side="left")

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
        tk.Label(self, text="QUESTION MANAGEMENT PORTAL", font=("Helvetica", 18, "bold"), fg=c["accent_primary"], bg=c["bg_primary"]).pack(pady=(15, 10))

        card = tk.Frame(self, bg=c["bg_secondary"], padx=20, pady=15)
        card.pack(fill="both", expand=True, padx=30, pady=10)

        self.ent_q = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_q.insert(0, "Enter question text...")
        self.ent_q.pack(fill="x", pady=4)

        self.ent_a = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_a.insert(0, "Option A")
        self.ent_a.pack(fill="x", pady=2)

        self.ent_b = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_b.insert(0, "Option B")
        self.ent_b.pack(fill="x", pady=2)

        self.ent_c = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_c.insert(0, "Option C")
        self.ent_c.pack(fill="x", pady=2)

        self.ent_d = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_d.insert(0, "Option D")
        self.ent_d.pack(fill="x", pady=2)

        meta_frame = tk.Frame(card, bg=c["bg_secondary"])
        meta_frame.pack(fill="x", pady=5)

        self.cmb_cat = ttk.Combobox(meta_frame, values=CATEGORIES, state="readonly", width=15)
        self.cmb_cat.set(CATEGORIES[0])
        self.cmb_cat.pack(side="left", padx=2)

        self.cmb_diff = ttk.Combobox(meta_frame, values=list(DIFFICULTIES.keys()), state="readonly", width=10)
        self.cmb_diff.set("Medium")
        self.cmb_diff.pack(side="left", padx=2)

        self.cmb_corr = ttk.Combobox(meta_frame, values=["A", "B", "C", "D"], state="readonly", width=5)
        self.cmb_corr.set("A")
        self.cmb_corr.pack(side="left", padx=2)

        self.ent_exp = tk.Entry(card, font=("Helvetica", 10), bg=c["bg_card"], fg=c["text_primary"])
        self.ent_exp.insert(0, "Explanation...")
        self.ent_exp.pack(fill="x", pady=4)

        btn_add = tk.Button(card, text="➕ Add Question to Database", font=("Helvetica", 11, "bold"), fg="#FFFFFF", bg=c["accent_primary"], activebackground=c["accent_hover"], command=self._add_q, relief="flat", pady=5)
        btn_add.pack(fill="x", pady=10)

        self.lbl_msg = tk.Label(card, text="", font=("Helvetica", 10), bg=c["bg_secondary"])
        self.lbl_msg.pack(pady=2)

    def _add_q(self):
        q, a, b, c, d = self.ent_q.get().strip(), self.ent_a.get().strip(), self.ent_b.get().strip(), self.ent_c.get().strip(), self.ent_d.get().strip()
        if not all([q, a, b, c, d]):
            self.lbl_msg.configure(text="❌ All fields required.", fg=self.theme_colors["danger"])
            return

        q_data = {
            "category": self.cmb_cat.get(),
            "difficulty": self.cmb_diff.get(),
            "question": q,
            "option_a": a, "option_b": b, "option_c": c, "option_d": d,
            "correct_option": self.cmb_corr.get(),
            "explanation": self.ent_exp.get().strip()
        }

        if self.controller.db.add_question(q_data):
            self.lbl_msg.configure(text="✅ Question added successfully!", fg=self.theme_colors["success"])
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

        tk.Label(self.sidebar, text="KNOWLEDGE HUB", font=("Helvetica", 16, "bold"), fg=c["accent_primary"], bg=c["bg_secondary"]).pack(pady=(25, 25))

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
        if not questions:
            questions = self.db.get_questions(category="Mixed", difficulty="All", limit=10)

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
