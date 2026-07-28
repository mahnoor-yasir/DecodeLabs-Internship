import csv
import json
import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class FluxExpenseTrackerPro:

    def __init__(self, root):
        self.root = root
        self.root.title("Enterprise Personal Finance Management System")
        self.root.geometry("1100x720")
        self.root.minsize(950, 650)

        # File Persistence Constants
        self.DATA_FILE = "expenses_pro_ledger.json"
        self.BACKUP_DIR = "backups"
        self.SETTINGS_FILE = "settings.json"

        # Color Palette Variables (Fixed Missing Attributes)
        self.BG_MAIN = "#f4f6f9"
        self.ACCENT_PRIMARY = "#1e293b"
        self.ACCENT_SECONDARY = "#2563eb"
        self.COLOR_DANGER = "#dc2626"
        self.COLOR_SUCCESS = "#16a34a"
        self.COLOR_WARNING = "#d97706"
        self.CARD_BG = "#ffffff"
        self.TEXT_DARK = "#0f172a"

        self.root.configure(bg=self.BG_MAIN)

        # Core State Variables
        self.user_name = ""
        self.currency = "PKR"
        self.monthly_budget = 50000.0
        self.categories = {
            "Food": ["Restaurant", "Groceries", "Café"],
            "Bills": ["Electricity", "Internet", "Water", "Gas"],
            "Travel": ["Fuel", "Taxi", "Public Transit"],
            "Shopping": ["Clothing", "Electronics"],
            "Entertainment": ["Movies", "Gaming", "Events"],
            "Healthcare": ["Medicines", "Doctor"],
            "Education": ["Books", "Courses"],
            "Miscellaneous": ["General"],
        }
        self.payment_methods = [
            "Cash",
            "JazzCash",
            "EasyPaisa",
            "Bank Transfer",
            "Card",
        ]
        self.transactions = []

        # Load Settings & Data First
        self.load_settings()
        self.load_data()

        # Hide Main Window while Asking User Name
        self.root.withdraw()
        self.ask_user_name()
        self.root.deiconify()

        # Build Full UI
        self.build_ui()

    # ----------------------------------------------------------------------
    # STARTUP USER NAME PROMPT
    # ----------------------------------------------------------------------
    def ask_user_name(self):
        # Prompt user on startup
        prompt_title = "Welcome to Expense Tracker Pro"
        prompt_msg = "Please enter your Name to continue:"
        
        entered_name = simpledialog.askstring(
            prompt_title, prompt_msg, initialvalue=self.user_name or "Mahnoor"
        )

        if entered_name and entered_name.strip():
            self.user_name = entered_name.strip()
        else:
            self.user_name = "User"

        self.save_settings()

    # ----------------------------------------------------------------------
    # DATA PERSISTENCE & HELPERS
    # ----------------------------------------------------------------------
    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    self.user_name = data.get("user_name", "")
                    self.currency = data.get("currency", "PKR")
                    self.monthly_budget = float(
                        data.get("monthly_budget", 50000.0)
                    )
                    if "categories" in data:
                        self.categories = data["categories"]
            except Exception:
                pass

    def save_settings(self):
        data = {
            "user_name": self.user_name,
            "currency": self.currency,
            "monthly_budget": self.monthly_budget,
            "categories": self.categories,
        }
        try:
            with open(self.SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save settings: {e}")

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as file:
                    self.transactions = json.load(file)
            except Exception:
                self.transactions = []

    def save_data(self):
        try:
            with open(self.DATA_FILE, "w") as file:
                json.dump(self.transactions, file, indent=4)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to persist data: {e}")

    def get_monthly_spent(self):
        current_month = datetime.now().strftime("%Y-%m")
        total = 0.0
        for t in self.transactions:
            if t.get("date_raw", "").startswith(current_month):
                total += t["amount"]
        return total

    def get_todays_spent(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total = 0.0
        for t in self.transactions:
            if t.get("date_raw") == today:
                total += t["amount"]
        return total

    # ----------------------------------------------------------------------
    # USER INTERFACE CONSTRUCTION
    # ----------------------------------------------------------------------
    def build_ui(self):
        # Top Banner Header with User Welcome
        header_frame = tk.Frame(self.root, bg=self.ACCENT_PRIMARY, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        self.header_label = tk.Label(
            header_frame,
            text=f"EXPENSE TRACKER PRO  |  Welcome, {self.user_name}!",
            font=("Helvetica", 14, "bold"),
            fg="#ffffff",
            bg=self.ACCENT_PRIMARY,
        )
        self.header_label.pack(pady=15)

        # Tabbed Navigation Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab Frames
        self.tab_dashboard = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.tab_analytics = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.tab_budget = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.tab_categories = tk.Frame(self.notebook, bg=self.BG_MAIN)
        self.tab_tools = tk.Frame(self.notebook, bg=self.BG_MAIN)

        self.notebook.add(self.tab_dashboard, text=" Dashboard & Ledger ")
        self.notebook.add(self.tab_analytics, text=" Statistics & Reports ")
        self.notebook.add(self.tab_budget, text=" Budget Manager ")
        self.notebook.add(self.tab_categories, text=" Category Manager ")
        self.notebook.add(self.tab_tools, text=" Data Tools & Settings ")

        # Build Tab Contents
        self.build_dashboard_tab()
        self.build_analytics_tab()
        self.build_budget_tab()
        self.build_categories_tab()
        self.build_tools_tab()

    # ----------------------------------------------------------------------
    # TAB 1: DASHBOARD & LEDGER
    # ----------------------------------------------------------------------
    def build_dashboard_tab(self):
        main_container = tk.Frame(self.tab_dashboard, bg=self.BG_MAIN)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Column: Inputs
        left_panel = tk.LabelFrame(
            main_container,
            text=" Record New Expense ",
            font=("Helvetica", 10, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_DARK,
            bd=1,
            relief=tk.SOLID,
        )
        left_panel.pack(
            side=tk.LEFT, fill=tk.Y, padx=(0, 10), ipadx=10, ipady=5
        )

        tk.Label(
            left_panel, text="Amount:", font=("Helvetica", 9), bg=self.CARD_BG
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.entry_amount = tk.Entry(
            left_panel, font=("Helvetica", 9), bd=1, relief=tk.SOLID
        )
        self.entry_amount.pack(fill=tk.X, padx=8, ipady=2)

        tk.Label(
            left_panel,
            text="Category:",
            font=("Helvetica", 9),
            bg=self.CARD_BG,
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.combo_category = ttk.Combobox(
            left_panel,
            values=list(self.categories.keys()),
            state="readonly",
            font=("Helvetica", 9),
        )
        if self.categories:
            self.combo_category.set(list(self.categories.keys())[0])
        self.combo_category.pack(fill=tk.X, padx=8, ipady=2)
        self.combo_category.bind(
            "<<ComboboxSelected>>", self.update_subcategory_options
        )

        tk.Label(
            left_panel,
            text="Sub Category:",
            font=("Helvetica", 9),
            bg=self.CARD_BG,
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.combo_subcategory = ttk.Combobox(
            left_panel, state="readonly", font=("Helvetica", 9)
        )
        self.combo_subcategory.pack(fill=tk.X, padx=8, ipady=2)
        self.update_subcategory_options()

        tk.Label(
            left_panel, text="Payment:", font=("Helvetica", 9), bg=self.CARD_BG
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.combo_payment = ttk.Combobox(
            left_panel,
            values=self.payment_methods,
            state="readonly",
            font=("Helvetica", 9),
        )
        self.combo_payment.set(self.payment_methods[0])
        self.combo_payment.pack(fill=tk.X, padx=8, ipady=2)

        tk.Label(
            left_panel,
            text="Description:",
            font=("Helvetica", 9),
            bg=self.CARD_BG,
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.entry_desc = tk.Entry(
            left_panel, font=("Helvetica", 9), bd=1, relief=tk.SOLID
        )
        self.entry_desc.pack(fill=tk.X, padx=8, ipady=2)

        tk.Label(
            left_panel,
            text="Location:",
            font=("Helvetica", 9),
            bg=self.CARD_BG,
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.entry_location = tk.Entry(
            left_panel, font=("Helvetica", 9), bd=1, relief=tk.SOLID
        )
        self.entry_location.insert(0, "Lahore")
        self.entry_location.pack(fill=tk.X, padx=8, ipady=2)

        tk.Label(
            left_panel, text="Tags:", font=("Helvetica", 9), bg=self.CARD_BG
        ).pack(anchor=tk.W, pady=(5, 0), padx=8)
        self.entry_tags = tk.Entry(
            left_panel, font=("Helvetica", 9), bd=1, relief=tk.SOLID
        )
        self.entry_tags.pack(fill=tk.X, padx=8, ipady=2)

        # Action Buttons
        tk.Button(
            left_panel,
            text="Add Expense",
            font=("Helvetica", 9, "bold"),
            bg=self.ACCENT_SECONDARY,
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.add_expense,
        ).pack(fill=tk.X, padx=8, pady=(12, 4), ipady=4)

        tk.Button(
            left_panel,
            text="Edit Selected",
            font=("Helvetica", 8),
            bg="#0f766e",
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.edit_selected,
        ).pack(fill=tk.X, padx=8, pady=2, ipady=3)

        tk.Button(
            left_panel,
            text="Delete Selected",
            font=("Helvetica", 8),
            bg=self.COLOR_WARNING,
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.delete_selected,
        ).pack(fill=tk.X, padx=8, pady=2, ipady=3)

        # Right Column: Displays
        right_panel = tk.Frame(main_container, bg=self.BG_MAIN)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Summary Bar
        summary_card = tk.Frame(
            right_panel, bg=self.CARD_BG, bd=1, relief=tk.SOLID
        )
        summary_card.pack(fill=tk.X, pady=(0, 8), ipady=6, ipadx=10)

        self.lbl_sum_today = tk.Label(
            summary_card,
            text="",
            font=("Helvetica", 9, "bold"),
            bg=self.CARD_BG,
            fg=self.ACCENT_PRIMARY,
        )
        self.lbl_sum_today.pack(side=tk.LEFT, padx=10)

        self.lbl_sum_month = tk.Label(
            summary_card,
            text="",
            font=("Helvetica", 9, "bold"),
            bg=self.CARD_BG,
            fg=self.ACCENT_SECONDARY,
        )
        self.lbl_sum_month.pack(side=tk.LEFT, padx=10)

        self.lbl_sum_budget = tk.Label(
            summary_card,
            text="",
            font=("Helvetica", 9, "bold"),
            bg=self.CARD_BG,
            fg=self.COLOR_SUCCESS,
        )
        self.lbl_sum_budget.pack(side=tk.LEFT, padx=10)

        # Search Bar
        search_card = tk.Frame(
            right_panel, bg=self.CARD_BG, bd=1, relief=tk.SOLID
        )
        search_card.pack(fill=tk.X, pady=(0, 8), ipady=4, ipadx=5)

        tk.Label(
            search_card,
            text="Search Records:",
            font=("Helvetica", 8, "bold"),
            bg=self.CARD_BG,
        ).pack(side=tk.LEFT, padx=(8, 2))
        self.entry_search = tk.Entry(
            search_card, font=("Helvetica", 8), bd=1, relief=tk.SOLID, width=25
        )
        self.entry_search.pack(side=tk.LEFT, padx=5)
        self.entry_search.bind("<KeyRelease>", lambda e: self.apply_filter())

        tk.Button(
            search_card,
            text="Reset Filter",
            font=("Helvetica", 8),
            bg="#e2e8f0",
            bd=1,
            relief=tk.SOLID,
            command=self.reset_dashboard_filter,
        ).pack(side=tk.LEFT, padx=5)

        # Table Grid
        table_frame = tk.Frame(
            right_panel, bg=self.CARD_BG, bd=1, relief=tk.SOLID
        )
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "ID",
            "Amount",
            "Category",
            "SubCategory",
            "Payment",
            "Date",
            "Time",
            "Location",
            "Tags",
            "Description",
        )
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col, width=80 if col not in ("Description", "Date") else 100
            )

        scrollbar_y = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_dashboard()

    def update_subcategory_options(self, event=None):
        selected_cat = self.combo_category.get()
        subs = self.categories.get(selected_cat, ["General"])
        self.combo_subcategory["values"] = subs
        if subs:
            self.combo_subcategory.set(subs[0])

    def refresh_dashboard(self, dataset=None):
        if dataset is None:
            dataset = self.transactions

        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in dataset:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item["id"],
                    f"{self.currency} {item['amount']:.2f}",
                    item["category"],
                    item.get("subcategory", "N/A"),
                    item["payment_method"],
                    item["date"],
                    item["time"],
                    item.get("location", "N/A"),
                    item.get("tags", "N/A"),
                    item["description"],
                ),
            )

        monthly_spent = self.get_monthly_spent()
        remaining = self.monthly_budget - monthly_spent

        self.lbl_sum_today.config(
            text=f"Today's Spent: {self.currency} {self.get_todays_spent():.2f}"
        )
        self.lbl_sum_month.config(
            text=f"This Month: {self.currency} {monthly_spent:.2f}"
        )
        self.lbl_sum_budget.config(
            text=f"Remaining Budget: {self.currency} {remaining:.2f}"
        )

    def add_expense(self):
        raw_amt = self.entry_amount.get().strip()
        try:
            amt = float(raw_amt)
            if amt <= 0:
                messagebox.showwarning(
                    "Validation Error", "Amount must be greater than zero."
                )
                return
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter a valid numeric amount."
            )
            return

        now = datetime.now()
        record_id = f"EXP-{len(self.transactions) + 1001}"
        record = {
            "id": record_id,
            "amount": round(amt, 2),
            "category": self.combo_category.get(),
            "subcategory": self.combo_subcategory.get(),
            "payment_method": self.combo_payment.get(),
            "description": self.entry_desc.get().strip() or "N/A",
            "date": now.strftime("%d-%m-%Y"),
            "date_raw": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%I:%M %p"),
            "location": self.entry_location.get().strip() or "Lahore",
            "tags": self.entry_tags.get().strip() or "N/A",
        }

        self.transactions.append(record)
        self.save_data()

        # Reset Form Entry Fields
        self.entry_amount.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_tags.delete(0, tk.END)

        self.refresh_dashboard()
        self.refresh_analytics()
        self.refresh_budget_display()

        # Check Monthly Warning
        monthly_spent = self.get_monthly_spent()
        if (
            self.monthly_budget > 0
            and (monthly_spent / self.monthly_budget) >= 0.9
        ):
            messagebox.showwarning(
                "Budget Warning",
                f"Warning: {self.user_name}, you have crossed 90% of your budget!\nSpent: {self.currency} {monthly_spent:.2f} / {self.currency} {self.monthly_budget:.2f}",
            )

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Record", "Please select a record from the table to edit.")
            return

        item_id = self.tree.item(selected)["values"][0]
        record = next((t for t in self.transactions if t["id"] == item_id), None)
        if not record:
            return

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Expense: {item_id}")
        edit_win.geometry("320x220")
        edit_win.grab_set()

        tk.Label(edit_win, text="New Amount:").pack(pady=(15, 2))
        e_amt = tk.Entry(edit_win)
        e_amt.insert(0, str(record["amount"]))
        e_amt.pack(pady=2)

        tk.Label(edit_win, text="New Description:").pack(pady=(10, 2))
        e_desc = tk.Entry(edit_win)
        e_desc.insert(0, record["description"])
        e_desc.pack(pady=2)

        def save_edits():
            try:
                record["amount"] = float(e_amt.get().strip())
                record["description"] = e_desc.get().strip()
                self.save_data()
                self.refresh_dashboard()
                self.refresh_analytics()
                self.refresh_budget_display()
                edit_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric amount.")

        tk.Button(
            edit_win,
            text="Save Changes",
            bg=self.ACCENT_SECONDARY,
            fg="#ffffff",
            bd=0,
            command=save_edits,
        ).pack(pady=15)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Record", "Please select a record to delete.")
            return

        item_id = self.tree.item(selected)["values"][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {item_id}?"):
            self.transactions = [
                t for t in self.transactions if t["id"] != item_id
            ]
            self.save_data()
            self.refresh_dashboard()
            self.refresh_analytics()
            self.refresh_budget_display()

    def apply_filter(self):
        query = self.entry_search.get().strip().lower()
        if not query:
            self.refresh_dashboard()
            return

        filtered = [
            t
            for t in self.transactions
            if query in str(t["id"]).lower()
            or query in t["category"].lower()
            or query in t["description"].lower()
            or query in t.get("tags", "").lower()
            or query in t.get("location", "").lower()
            or query in t.get("payment_method", "").lower()
        ]
        self.refresh_dashboard(filtered)

    def reset_dashboard_filter(self):
        self.entry_search.delete(0, tk.END)
        self.refresh_dashboard()

    # ----------------------------------------------------------------------
    # TAB 2: STATISTICS & REPORTS
    # ----------------------------------------------------------------------
    def build_analytics_tab(self):
        container = tk.Frame(self.tab_analytics, bg=self.CARD_BG, bd=1, relief=tk.SOLID)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=10, ipady=10)

        tk.Label(
            container,
            text="EXPENSE ANALYTICS & STATISTICAL AUDIT",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT_PRIMARY,
            fg="#ffffff",
        ).pack(fill=tk.X, pady=(0, 15))

        self.stats_text = tk.Text(
            container, font=("Courier", 10), bg="#f8fafc", bd=1, relief=tk.SOLID
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.refresh_analytics()

    def refresh_analytics(self):
        self.stats_text.delete("1.0", tk.END)
        if not self.transactions:
            self.stats_text.insert(tk.END, "No records logged yet. Add expenses to view statistical summary.")
            return

        total_spent = sum(t["amount"] for t in self.transactions)
        avg_spent = total_spent / len(self.transactions)
        highest = max(self.transactions, key=lambda x: x["amount"])
        lowest = min(self.transactions, key=lambda x: x["amount"])

        categories = {}
        for t in self.transactions:
            c = t["category"]
            categories[c] = categories.get(c, 0.0) + t["amount"]

        top_cat = max(categories, key=categories.get) if categories else "N/A"

        report = f"""
======================================================================
                  STATISTICAL REPORT FOR: {self.user_name.upper()}
======================================================================
  Total Cumulative Spend   : {self.currency} {total_spent:.2f}
  Average Expense / Entry  : {self.currency} {avg_spent:.2f}
  Highest Single Expense   : {self.currency} {highest['amount']:.2f} ({highest['category']} - {highest['description']})
  Lowest Single Expense    : {self.currency} {lowest['amount']:.2f} ({lowest['category']} - {lowest['description']})
  Top Expense Sector       : {top_cat} ({self.currency} {categories.get(top_cat, 0.0):.2f})
  Total Logged Entries     : {len(self.transactions)}
----------------------------------------------------------------------
  SECTOR BREAKDOWN:
"""
        for cat, amt in categories.items():
            pct = (amt / total_spent) * 100 if total_spent > 0 else 0
            bar = "█" * int(pct // 5)
            report += f"  {cat:<18} : {self.currency} {amt:>8.2f}  ({pct:>5.1f}%) [{bar:<20}]\n"

        report += "======================================================================\n"
        self.stats_text.insert(tk.END, report)

    # ----------------------------------------------------------------------
    # TAB 3: BUDGET MANAGER
    # ----------------------------------------------------------------------
    def build_budget_tab(self):
        container = tk.Frame(self.tab_budget, bg=self.CARD_BG, bd=1, relief=tk.SOLID)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=10, ipady=10)

        tk.Label(
            container,
            text="MONTHLY BUDGET CONTROL CENTER",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT_PRIMARY,
            fg="#ffffff",
        ).pack(fill=tk.X, pady=(0, 15))

        top_frame = tk.Frame(container, bg=self.CARD_BG)
        top_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            top_frame,
            text="Set Monthly Limit:",
            font=("Helvetica", 10),
            bg=self.CARD_BG,
        ).pack(side=tk.LEFT, padx=10)
        self.entry_budget_limit = tk.Entry(top_frame, font=("Helvetica", 10))
        self.entry_budget_limit.insert(0, str(self.monthly_budget))
        self.entry_budget_limit.pack(side=tk.LEFT, padx=10)

        tk.Button(
            top_frame,
            text="Update Limit",
            bg=self.ACCENT_SECONDARY,
            fg="#ffffff",
            bd=0,
            command=self.update_budget_limit,
        ).pack(side=tk.LEFT, padx=10)

        self.lbl_budget_status = tk.Label(
            container,
            text="",
            font=("Helvetica", 11, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_DARK,
        )
        self.lbl_budget_status.pack(anchor=tk.W, padx=10, pady=15)

        self.progress_budget = ttk.Progressbar(
            container, orient=tk.HORIZONTAL, length=400, mode="determinate"
        )
        self.progress_budget.pack(fill=tk.X, padx=10, pady=10)

        self.refresh_budget_display()

    def update_budget_limit(self):
        try:
            val = float(self.entry_budget_limit.get().strip())
            if val < 0:
                return
            self.monthly_budget = val
            self.save_settings()
            self.refresh_budget_display()
            self.refresh_dashboard()
            messagebox.showinfo("Updated", "Monthly budget updated successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric budget limit.")

    def refresh_budget_display(self):
        spent = self.get_monthly_spent()
        pct = (spent / self.monthly_budget * 100) if self.monthly_budget > 0 else 0
        rem = self.monthly_budget - spent

        self.progress_budget["value"] = min(pct, 100)
        status = f"Monthly Limit: {self.currency} {self.monthly_budget:.2f}\nSpent: {self.currency} {spent:.2f}\nRemaining: {self.currency} {rem:.2f}\nBudget Usage: {pct:.1f}%"
        self.lbl_budget_status.config(text=status)

    # ----------------------------------------------------------------------
    # TAB 4: CATEGORY MANAGER
    # ----------------------------------------------------------------------
    def build_categories_tab(self):
        container = tk.Frame(self.tab_categories, bg=self.CARD_BG, bd=1, relief=tk.SOLID)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=10, ipady=10)

        tk.Label(
            container,
            text="CUSTOM CATEGORY MANAGER",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT_PRIMARY,
            fg="#ffffff",
        ).pack(fill=tk.X, pady=(0, 15))

        f_input = tk.Frame(container, bg=self.CARD_BG)
        f_input.pack(fill=tk.X, pady=5)

        tk.Label(f_input, text="New Category Name:", bg=self.CARD_BG).pack(
            side=tk.LEFT, padx=5
        )
        self.e_new_cat = tk.Entry(f_input)
        self.e_new_cat.pack(side=tk.LEFT, padx=5)

        tk.Button(
            f_input,
            text="Add Category",
            bg=self.ACCENT_SECONDARY,
            fg="#ffffff",
            bd=0,
            command=self.add_custom_category,
        ).pack(side=tk.LEFT, padx=5)

        self.list_categories = tk.Listbox(container, font=("Helvetica", 10))
        self.list_categories.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.refresh_category_list()

    def refresh_category_list(self):
        self.list_categories.delete(0, tk.END)
        for cat in self.categories.keys():
            self.list_categories.insert(tk.END, cat)

    def add_custom_category(self):
        name = self.e_new_cat.get().strip()
        if name and name not in self.categories:
            self.categories[name] = ["General"]
            self.save_settings()
            self.refresh_category_list()
            self.combo_category["values"] = list(self.categories.keys())
            self.e_new_cat.delete(0, tk.END)

    # ----------------------------------------------------------------------
    # TAB 5: DATA TOOLS & SETTINGS
    # ----------------------------------------------------------------------
    def build_tools_tab(self):
        container = tk.Frame(self.tab_tools, bg=self.CARD_BG, bd=1, relief=tk.SOLID)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, ipadx=10, ipady=10)

        tk.Label(
            container,
            text="SETTINGS & DATA MANAGEMENT",
            font=("Helvetica", 11, "bold"),
            bg=self.ACCENT_PRIMARY,
            fg="#ffffff",
        ).pack(fill=tk.X, pady=(0, 15))

        # Change User Name
        f_user = tk.Frame(container, bg=self.CARD_BG)
        f_user.pack(fill=tk.X, pady=10, padx=10)

        tk.Label(f_user, text="User Profile Name:", font=("Helvetica", 10), bg=self.CARD_BG).pack(side=tk.LEFT, padx=5)
        self.e_change_name = tk.Entry(f_user, font=("Helvetica", 10))
        self.e_change_name.insert(0, self.user_name)
        self.e_change_name.pack(side=tk.LEFT, padx=5)

        tk.Button(
            f_user,
            text="Update Name",
            bg=self.ACCENT_SECONDARY,
            fg="#ffffff",
            bd=0,
            command=self.update_user_name,
        ).pack(side=tk.LEFT, padx=5)

        # Currency Switch
        f_curr = tk.Frame(container, bg=self.CARD_BG)
        f_curr.pack(fill=tk.X, pady=10, padx=10)

        tk.Label(
            f_curr, text="Active Currency:", font=("Helvetica", 10), bg=self.CARD_BG
        ).pack(side=tk.LEFT, padx=5)
        self.combo_curr = ttk.Combobox(
            f_curr, values=["PKR", "USD", "EUR", "AED"], state="readonly", width=10
        )
        self.combo_curr.set(self.currency)
        self.combo_curr.pack(side=tk.LEFT, padx=5)

        tk.Button(
            f_curr,
            text="Save Currency",
            bg=self.ACCENT_SECONDARY,
            fg="#ffffff",
            bd=0,
            command=self.change_currency,
        ).pack(side=tk.LEFT, padx=5)

        # Export & Backup Actions
        f_export = tk.Frame(container, bg=self.CARD_BG)
        f_export.pack(fill=tk.X, pady=15, padx=10)

        tk.Button(
            f_export,
            text="Export to CSV",
            bg="#0f766e",
            fg="#ffffff",
            bd=0,
            command=self.export_csv,
        ).pack(side=tk.LEFT, padx=5, ipady=4)

        tk.Button(
            f_export,
            text="Create Backup",
            bg=self.ACCENT_PRIMARY,
            fg="#ffffff",
            bd=0,
            command=self.create_backup,
        ).pack(side=tk.LEFT, padx=5, ipady=4)

    def update_user_name(self):
        new_n = self.e_change_name.get().strip()
        if new_n:
            self.user_name = new_n
            self.save_settings()
            self.header_label.config(text=f"EXPENSE TRACKER PRO  |  Welcome, {self.user_name}!")
            self.refresh_analytics()
            messagebox.showinfo("Updated", f"Profile name updated to {self.user_name}")

    def change_currency(self):
        self.currency = self.combo_curr.get()
        self.save_settings()
        self.refresh_dashboard()
        self.refresh_analytics()
        self.refresh_budget_display()
        messagebox.showinfo("Success", f"Currency set to {self.currency}")

    def export_csv(self):
        if not self.transactions:
            messagebox.showinfo("No Data", "No transactions available to export.")
            return

        file_path = "expenses_export.csv"
        try:
            keys = self.transactions[0].keys()
            with open(file_path, "w", newline="") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.transactions)
            messagebox.showinfo(
                "Export Complete", f"Data exported successfully to {file_path}"
            )
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def create_backup(self):
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(self.BACKUP_DIR, f"backup_ledger_{timestamp}.json")
        try:
            shutil.copy(self.DATA_FILE, dest)
            messagebox.showinfo("Backup Created", f"Ledger backed up to {dest}")
        except Exception as e:
            messagebox.showerror("Backup Failed", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FluxExpenseTrackerPro(root)
    root.mainloop()
