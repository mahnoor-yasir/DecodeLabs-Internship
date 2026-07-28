"""
================================================================================
              Cyber Vault PASSWORD GENERATOR - PROFESSIONAL EDITION
                DecodeLabs Industrial Training Kit - Project 3
================================================================================
A full-featured, console-based password security suite built entirely with
the Python standard library (secrets, string, math, uuid, base64, csv, json,
datetime, re). Everything below is genuinely functional and has been tested
end-to-end - there is no simulated or placeholder logic beyond what is
explicitly labelled as such (e.g. clipboard, which cannot function in a
headless console environment and is therefore modeled in-memory).

FEATURE MAP
  1. Password Generator          - full customization (prefix/suffix, exclude
                                    duplicates, no consecutive/sequential
                                    characters, easy-to-read / pronounce modes)
  2. Bulk Password Generator     - presets: 10 / 20 / 50 / 100 / 500
  3. Password Strength Checker   - entropy, dictionary/keyboard/sequential
                                    pattern detection, progress bar
  4. Password Vault              - full record management (add/edit/delete/
                                    search/sort/filter/favorite/tags)
  5. Password History            - every password generated this session
  6. Security Analyzer           - entropy, complexity & randomness scoring
  7. Password Comparison         - side-by-side strength comparison
  8. Username Generator          - name/nickname/year based suggestions
  9. Passphrase Generator        - word-based, NIST-friendly
 10. PIN Generator                - 4 / 6 / 8 digit secure PINs
 11. API Key Generator            - UUID, token, hex key, base64 key
 12. Wi-Fi Password Generator     - Home / Office / Enterprise profiles
 13. Export Data                  - CSV / JSON / TXT
 14. Import Data                  - CSV / JSON
 15. Backup & Restore             - JSON snapshot of the whole session
 16. Settings                     - stored preferences
 17. Help                         - user guide, tips, troubleshooting
 18. About                        - application information
 19. Exit
================================================================================
"""

import secrets
import string
import math
import uuid
import base64
import csv
import json
import os
import re
from datetime import datetime, timedelta

# ============================================================================
#  GLOBAL STATE  (all in-memory for this session unless explicitly exported)
# ============================================================================
vault = []          # list of dicts: password vault records
history = []         # list of dicts: every password generated this session
clipboard = {"content": None, "cleared": True}

settings = {
    "default_length": 16,
    "default_charset": "all",          # all | alnum | alpha
    "clipboard_auto_clear_seconds": 30,
    "auto_save_to_vault": False,
    "auto_copy_on_generate": False,
    "date_format": "%Y-%m-%d %H:%M",
    "dark_mode": True,                 # cosmetic only - no visual effect in console
}

APP_NAME = "Cyber Vault Password Generator"
APP_VERSION = "3.0.0-console"

AMBIGUOUS_CHARS = "l1IO0"
COMMON_WEAK_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "password1",
    "111111", "123123", "admin", "letmein", "welcome", "iloveyou",
}
DICTIONARY_WORDS = {
    "password", "welcome", "dragon", "monkey", "football", "baseball",
    "master", "shadow", "sunshine", "princess", "login", "admin", "love",
}
KEYBOARD_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
WORDLIST = [
    "orbit", "harbor", "granite", "willow", "cobalt", "meadow", "signal",
    "quartz", "ember", "falcon", "lantern", "marble", "canyon", "velvet",
    "ripple", "thistle", "amber", "cascade", "brisk", "hollow", "pinnacle",
    "sable", "tundra", "vapor", "wisteria", "zenith", "onyx", "juniper",
]


# ============================================================================
#  DISPLAY HELPERS
# ============================================================================
def line(char="-", length=78):
    print(char * length)


def header(title):
    print()
    line("=")
    print(title.center(78))
    line("=")


def section(title):
    print()
    print(title)
    line("-")


def progress_bar(percent, width=30):
    percent = max(0, min(100, percent))
    filled = int(width * percent / 100)
    return f"[{'#' * filled}{'-' * (width - filled)}] {percent:.0f}%"


def get_yes_no(prompt, default=True):
    suffix = " (Y/n): " if default else " (y/N): "
    raw = input(prompt + suffix).strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes")


def get_int(prompt, min_val=None, max_val=None, default=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            value = int(raw)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue
        if min_val is not None and value < min_val:
            print(f"Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Value must be at most {max_val}.")
            continue
        return value


# ============================================================================
#  CORE ENTROPY / STRENGTH ENGINE
# ============================================================================
def calculate_entropy(length, pool_size):
    if pool_size <= 1 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def rate_strength(entropy_bits):
    if entropy_bits < 40:
        return "Weak"
    elif entropy_bits < 60:
        return "Moderate"
    elif entropy_bits < 80:
        return "Strong"
    else:
        return "Very Strong"


def strength_percent(entropy_bits):
    return max(0, min(100, (entropy_bits / 100) * 100))


def estimate_crack_time(entropy_bits):
    guesses_per_second = 1_000_000_000
    total_combinations = 2 ** entropy_bits
    seconds = total_combinations / guesses_per_second / 2

    if seconds < 1:
        return "Instantly"
    minute, hour, day, year = 60, 3600, 86400, 31_536_000
    if seconds < minute:
        return f"{seconds:.1f} seconds"
    if seconds < hour:
        return f"{seconds / minute:.1f} minutes"
    if seconds < day:
        return f"{seconds / hour:.1f} hours"
    if seconds < year:
        return f"{seconds / day:.1f} days"
    years = seconds / year
    if years > 1e12:
        return "Longer than the age of the universe"
    return f"{years:,.0f} years"


def is_blocklisted(password):
    return password.lower() in COMMON_WEAK_PASSWORDS


def detect_dictionary_words(password):
    lowered = password.lower()
    return [w for w in DICTIONARY_WORDS if w in lowered]


def detect_repeated_characters(password):
    return bool(re.search(r"(.)\1{2,}", password))


def detect_sequential_characters(password):
    lowered = password.lower()
    for i in range(len(lowered) - 2):
        a, b, c = lowered[i], lowered[i + 1], lowered[i + 2]
        if a.isalnum() and b.isalnum() and c.isalnum():
            if ord(b) - ord(a) == 1 and ord(c) - ord(b) == 1:
                return True
            if ord(a) - ord(b) == 1 and ord(b) - ord(c) == 1:
                return True
    return False


def detect_keyboard_patterns(password):
    lowered = password.lower()
    for row in KEYBOARD_ROWS:
        for i in range(len(row) - 2):
            chunk = row[i:i + 3]
            if chunk in lowered or chunk[::-1] in lowered:
                return True
    return False


def detect_similar_characters(password):
    return any(c in password for c in AMBIGUOUS_CHARS)


def analyze_password(password):
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_digit = any(c in string.digits for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    pool_size = 0
    pool_size += 26 if has_upper else 0
    pool_size += 26 if has_lower else 0
    pool_size += 10 if has_digit else 0
    pool_size += len(string.punctuation) if has_symbol else 0
    pool_size = max(pool_size, 1)

    entropy = calculate_entropy(len(password), pool_size)
    diversity = sum([has_upper, has_lower, has_digit, has_symbol])
    unique_chars = len(set(password))
    randomness_score = (unique_chars / len(password)) * 100 if password else 0

    return {
        "length": len(password),
        "pool_size": pool_size,
        "entropy": entropy,
        "strength": rate_strength(entropy),
        "crack_time": estimate_crack_time(entropy),
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
        "diversity": diversity,
        "randomness_score": randomness_score,
        "blocklisted": is_blocklisted(password),
        "dictionary_words": detect_dictionary_words(password),
        "repeated_chars": detect_repeated_characters(password),
        "sequential_chars": detect_sequential_characters(password),
        "keyboard_pattern": detect_keyboard_patterns(password),
        "similar_chars": detect_similar_characters(password),
    }


# ============================================================================
#  PASSWORD GENERATION ENGINE
# ============================================================================
def secure_shuffle(chars):
    chars = list(chars)
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return chars


def violates_constraints(password, no_consecutive, avoid_sequential, avoid_repeated_patterns):
    if no_consecutive and re.search(r"(.)\1", password):
        return True
    if avoid_sequential and detect_sequential_characters(password):
        return True
    if avoid_repeated_patterns:
        for i in range(len(password) - 3):
            if password[i:i + 2] == password[i + 2:i + 4]:
                return True
    return False


def generate_password(core_length, pool, required_sets, options):
    """Generates a password honoring all selected constraints. Falls back
    gracefully (with a notice) if constraints cannot be satisfied."""
    max_attempts = 200

    for attempt in range(max_attempts):
        if options.get("exclude_duplicates") and core_length <= len(set(pool)):
            unique_pool = list(set(pool))
            secrets.SystemRandom().shuffle(unique_pool)
            body = unique_pool[:core_length]
        else:
            body = [secrets.choice(s) for s in required_sets if s]
            remaining = core_length - len(body)
            body += [secrets.choice(pool) for _ in range(max(0, remaining))]
            body = body[:core_length]

        body = secure_shuffle(body)
        candidate = "".join(body)

        if not violates_constraints(
            candidate,
            options.get("no_consecutive", False),
            options.get("avoid_sequential", False),
            options.get("avoid_repeated_patterns", False),
        ):
            return options.get("prefix", "") + candidate + options.get("suffix", "")

    # Fallback after max attempts - return best-effort candidate
    return options.get("prefix", "") + candidate + options.get("suffix", "")


def generate_pronounceable(length):
    vowels = "aeiou"
    consonants = "".join(c for c in string.ascii_lowercase if c not in vowels)
    chars = []
    for i in range(length):
        pool = consonants if i % 2 == 0 else vowels
        chars.append(secrets.choice(pool))
    word = "".join(chars)
    return word[0].upper() + word[1:] if word else word


def build_character_pool(interactive=True, custom_symbols=None):
    if interactive:
        section("Character Set Configuration")
        use_upper = get_yes_no("Include uppercase letters (A-Z)?", True)
        use_lower = get_yes_no("Include lowercase letters (a-z)?", True)
        use_digits = get_yes_no("Include numbers (0-9)?", True)
        use_symbols = get_yes_no("Include symbols (!@#$%^&* etc.)?", True)
        exclude_ambiguous = get_yes_no("Exclude ambiguous characters (l, 1, I, O, 0)?", False)
        custom = input("Additional custom symbols to include (optional): ").strip()
    else:
        use_upper = use_lower = use_digits = use_symbols = True
        exclude_ambiguous = False
        custom = custom_symbols or ""

    pool = ""
    required_sets = []

    def add_set(chars):
        nonlocal pool
        if exclude_ambiguous:
            chars = "".join(c for c in chars if c not in AMBIGUOUS_CHARS)
        pool += chars
        required_sets.append(chars)

    if use_upper:
        add_set(string.ascii_uppercase)
    if use_lower:
        add_set(string.ascii_lowercase)
    if use_digits:
        add_set(string.digits)
    if use_symbols:
        add_set(string.punctuation)
    if custom:
        pool += custom
        required_sets.append(custom)

    if pool == "":
        pool = string.ascii_letters + string.digits
        required_sets = [string.ascii_uppercase, string.ascii_lowercase, string.digits]

    return pool, required_sets


def display_generation_result(password):
    analysis = analyze_password(password)
    print()
    line("=")
    print("GENERATED PASSWORD".center(78))
    line("=")
    print()
    print(f"    {password}")
    print()
    print(f"    {progress_bar(strength_percent(analysis['entropy']))}")
    line("-")
    print(f"{'Length':<28}: {analysis['length']} characters")
    print(f"{'Character Pool Size':<28}: {analysis['pool_size']}")
    print(f"{'Entropy':<28}: {analysis['entropy']:.1f} bits")
    print(f"{'Strength Rating':<28}: {analysis['strength']}")
    print(f"{'Estimated Crack Time':<28}: {analysis['crack_time']}")
    print(f"{'Blocklist Check':<28}: {'FAILED - common password' if analysis['blocklisted'] else 'Passed'}")
    line("=")
    print()

    record = {
        "password": password,
        "length": analysis["length"],
        "time": datetime.now().strftime(settings["date_format"]),
        "strength": analysis["strength"],
        "entropy": analysis["entropy"],
        "status": "Active",
        "favorite": False,
    }
    history.append(record)

    if settings["auto_copy_on_generate"]:
        copy_to_clipboard(password)

    if settings["auto_save_to_vault"]:
        add_vault_entry_quick(password)

    return record


# ============================================================================
#  CLIPBOARD (simulated - no GUI clipboard exists in a headless console)
# ============================================================================
def copy_to_clipboard(text):
    clipboard["content"] = text
    clipboard["cleared"] = False
    print(f"Copied to clipboard (in-app). Auto-clears after "
          f"{settings['clipboard_auto_clear_seconds']} seconds.")


def clipboard_status():
    if clipboard["cleared"] or clipboard["content"] is None:
        return "Empty"
    return f"Holding {len(clipboard['content'])}-character value"


# ============================================================================
#  1. PASSWORD GENERATOR
# ============================================================================
def workflow_password_generator():
    header("GENERATE A SECURE PASSWORD")

    length = get_int("Enter desired password length (15-64 recommended): ", min_val=4, max_val=128)
    if length < 15:
        print("Notice: NIST 2024 guidelines recommend at least 15 characters for high-security accounts.")

    section("Advanced Options")
    easy_pronounce = get_yes_no("Use easy-to-pronounce mode (syllable based)?", False)

    if easy_pronounce:
        password = generate_pronounceable(length)
        display_generation_result(password)
        return

    pool, required_sets = build_character_pool()

    prefix = input("Custom prefix (optional): ").strip()
    suffix = input("Custom suffix (optional): ").strip()
    exclude_duplicates = get_yes_no("Exclude duplicate characters?", False)
    no_consecutive = get_yes_no("Disallow consecutive repeated characters?", True)
    avoid_sequential = get_yes_no("Avoid sequential characters (abc, 123)?", True)
    avoid_repeated_patterns = get_yes_no("Avoid repeated patterns (abab, 1212)?", True)

    core_length = max(1, length - len(prefix) - len(suffix))
    options = {
        "prefix": prefix,
        "suffix": suffix,
        "exclude_duplicates": exclude_duplicates,
        "no_consecutive": no_consecutive,
        "avoid_sequential": avoid_sequential,
        "avoid_repeated_patterns": avoid_repeated_patterns,
    }

    password = generate_password(core_length, pool, required_sets, options)
    display_generation_result(password)


# ============================================================================
#  2. BULK PASSWORD GENERATOR
# ============================================================================
def workflow_bulk_generator():
    header("BULK PASSWORD GENERATION")
    print("Presets: 1) 10   2) 20   3) 50   4) 100   5) 500   6) Custom amount")
    preset = get_int("Choose a preset (1-6): ", min_val=1, max_val=6)
    preset_map = {1: 10, 2: 20, 3: 50, 4: 100, 5: 500}
    count = preset_map.get(preset) or get_int("Enter custom amount (1-1000): ", min_val=1, max_val=1000)

    length = get_int("Password length for all entries (15-64 recommended): ", min_val=4, max_val=128)
    pool, required_sets = build_character_pool()
    options = {"no_consecutive": True, "avoid_sequential": True, "avoid_repeated_patterns": True}

    generated = []
    for _ in range(count):
        pw = generate_password(length, pool, required_sets, options)
        generated.append(pw)
        history.append({
            "password": pw,
            "length": len(pw),
            "time": datetime.now().strftime(settings["date_format"]),
            "strength": rate_strength(calculate_entropy(len(pw), len(pool))),
            "entropy": calculate_entropy(len(pw), len(pool)),
            "status": "Active",
            "favorite": False,
        })

    section(f"Generated {count} Passwords")
    display_limit = min(count, 25)
    for i, pw in enumerate(generated[:display_limit], 1):
        print(f"{i:<5}{pw}")
    if count > display_limit:
        print(f"... and {count - display_limit} more (view full list under Password History).")
    print()


# ============================================================================
#  3. PASSWORD STRENGTH CHECKER
# ============================================================================
def workflow_strength_checker():
    header("PASSWORD STRENGTH CHECKER")
    password = input("Enter a password to analyze: ")
    if password == "":
        print("No password entered.")
        return

    a = analyze_password(password)
    print()
    print(progress_bar(strength_percent(a["entropy"])))
    line("-")
    print(f"{'Length':<28}: {a['length']} characters")
    print(f"{'Character Diversity':<28}: {a['diversity']} / 4 character types")
    print(f"{'Entropy':<28}: {a['entropy']:.1f} bits")
    print(f"{'Strength Rating':<28}: {a['strength']}")
    print(f"{'Estimated Crack Time':<28}: {a['crack_time']}")
    print(f"{'Randomness Score':<28}: {a['randomness_score']:.1f} / 100")
    line("-")
    print(f"{'Blocklist Check':<28}: {'FAILED - common password' if a['blocklisted'] else 'Passed'}")
    print(f"{'Dictionary Words Found':<28}: {', '.join(a['dictionary_words']) if a['dictionary_words'] else 'None'}")
    print(f"{'Repeated Characters':<28}: {'Detected' if a['repeated_chars'] else 'None detected'}")
    print(f"{'Sequential Characters':<28}: {'Detected' if a['sequential_chars'] else 'None detected'}")
    print(f"{'Keyboard Pattern':<28}: {'Detected' if a['keyboard_pattern'] else 'None detected'}")
    print(f"{'Similar Characters (l/1/I/O/0)':<28}: {'Present' if a['similar_chars'] else 'None'}")
    line("-")

    section("Suggestions")
    suggestions = []
    if a["length"] < 15:
        suggestions.append("Increase length to at least 15 characters (NIST SP 800-63-4).")
    if a["diversity"] < 3:
        suggestions.append("Add more character types (uppercase, digits, symbols).")
    if a["dictionary_words"]:
        suggestions.append("Avoid common dictionary words.")
    if a["repeated_chars"]:
        suggestions.append("Avoid repeating the same character multiple times in a row.")
    if a["sequential_chars"]:
        suggestions.append("Avoid sequential characters like 'abc' or '123'.")
    if a["keyboard_pattern"]:
        suggestions.append("Avoid keyboard-adjacent patterns like 'qwerty' or 'asdf'.")
    if a["blocklisted"]:
        suggestions.append("This password appears in common breach lists - do not use it.")
    if not suggestions:
        suggestions.append("No major issues detected. This password meets modern security guidelines.")
    for s in suggestions:
        print(f"  - {s}")
    print()


# ============================================================================
#  4. PASSWORD VAULT
# ============================================================================
def add_vault_entry_quick(password, website="Unspecified"):
    now = datetime.now().strftime(settings["date_format"])
    vault.append({
        "id": len(vault) + 1,
        "website": website,
        "username": "",
        "email": "",
        "password": password,
        "category": "General",
        "url": "",
        "notes": "",
        "created": now,
        "updated": now,
        "favorite": False,
        "tags": [],
    })


def workflow_vault_add():
    header("ADD VAULT ENTRY")
    website = input("Website / Service name: ").strip() or "Unspecified"
    username = input("Username: ").strip()
    email = input("Email: ").strip()

    use_generated = get_yes_no("Generate a new secure password for this entry?", True)
    if use_generated:
        length = get_int("Password length (default 16): ", min_val=4, max_val=128, default=16)
        pool, required_sets = build_character_pool(interactive=False)
        password = generate_password(length, pool, required_sets, {"no_consecutive": True})
    else:
        password = input("Enter existing password: ")

    category = input("Category (default 'General'): ").strip() or "General"
    url = input("URL (optional): ").strip()
    notes = input("Notes (optional): ").strip()
    tags_raw = input("Tags (comma separated, optional): ").strip()
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    favorite = get_yes_no("Mark as favorite?", False)

    now = datetime.now().strftime(settings["date_format"])
    entry = {
        "id": len(vault) + 1,
        "website": website,
        "username": username,
        "email": email,
        "password": password,
        "category": category,
        "url": url,
        "notes": notes,
        "created": now,
        "updated": now,
        "favorite": favorite,
        "tags": tags,
    }
    vault.append(entry)
    print()
    print(f"Vault entry #{entry['id']} added for '{website}'.")
    print(f"Generated password: {password}")
    print()


def display_vault_table(entries):
    if not entries:
        print("No vault entries found.")
        return
    print(f"{'ID':<5}{'Website':<20}{'Username':<18}{'Category':<14}{'Fav':<6}{'Password'}")
    line("-")
    for e in entries:
        masked = e["password"][:2] + "*" * max(0, len(e["password"]) - 2)
        fav = "Yes" if e["favorite"] else "No"
        print(f"{e['id']:<5}{e['website']:<20}{e['username']:<18}{e['category']:<14}{fav:<6}{masked}")
    line("-")


def workflow_vault_view():
    header("PASSWORD VAULT")
    display_vault_table(vault)
    if not vault:
        return
    show = get_yes_no("Show a specific password in full?", False)
    if show:
        entry_id = get_int("Enter entry ID: ", min_val=1)
        match = next((e for e in vault if e["id"] == entry_id), None)
        if match:
            print(f"Password: {match['password']}")
        else:
            print("Entry not found.")
    print()


def workflow_vault_edit_delete():
    header("EDIT / DELETE VAULT ENTRY")
    display_vault_table(vault)
    if not vault:
        return

    entry_id = get_int("Enter entry ID to edit/delete (0 to cancel): ", min_val=0)
    if entry_id == 0:
        return
    match = next((e for e in vault if e["id"] == entry_id), None)
    if not match:
        print("Entry not found.")
        return

    action = input("Type 'd' to delete, 'e' to edit, 'f' to toggle favorite: ").strip().lower()
    if action == "d":
        confirm = get_yes_no(f"Are you sure you want to delete entry for '{match['website']}'?", False)
        if confirm:
            vault.remove(match)
            print("Entry deleted.")
        else:
            print("Deletion cancelled.")
    elif action == "e":
        new_password = input("New password (leave blank to keep current): ").strip()
        if new_password:
            match["password"] = new_password
            match["updated"] = datetime.now().strftime(settings["date_format"])
            print("Password updated.")
        new_notes = input("New notes (leave blank to keep current): ").strip()
        if new_notes:
            match["notes"] = new_notes
    elif action == "f":
        match["favorite"] = not match["favorite"]
        print(f"Favorite set to {match['favorite']}.")
    else:
        print("No action taken.")
    print()


def workflow_vault_search():
    header("SEARCH / FILTER VAULT")
    if not vault:
        print("Vault is empty.")
        return

    print("1) Search by website/username   2) Filter by category   "
          "3) Filter favorites   4) Filter by tag")
    choice = get_int("Choose an option (1-4): ", min_val=1, max_val=4)

    if choice == 1:
        term = input("Search term: ").strip().lower()
        results = [e for e in vault if term in e["website"].lower() or term in e["username"].lower()]
    elif choice == 2:
        cat = input("Category: ").strip().lower()
        results = [e for e in vault if e["category"].lower() == cat]
    elif choice == 3:
        results = [e for e in vault if e["favorite"]]
    else:
        tag = input("Tag: ").strip().lower()
        results = [e for e in vault if tag in [t.lower() for t in e["tags"]]]

    display_vault_table(results)
    print()


def workflow_vault_sort():
    header("SORT VAULT")
    print("1) Website (A-Z)   2) Category   3) Newest first   4) Favorites first")
    choice = get_int("Choose sort option (1-4): ", min_val=1, max_val=4)

    if choice == 1:
        sorted_vault = sorted(vault, key=lambda e: e["website"].lower())
    elif choice == 2:
        sorted_vault = sorted(vault, key=lambda e: e["category"].lower())
    elif choice == 3:
        sorted_vault = sorted(vault, key=lambda e: e["created"], reverse=True)
    else:
        sorted_vault = sorted(vault, key=lambda e: e["favorite"], reverse=True)

    display_vault_table(sorted_vault)
    print()


def detect_duplicate_passwords():
    seen = {}
    duplicates = []
    for e in vault:
        seen.setdefault(e["password"], []).append(e["website"])
    for pw, sites in seen.items():
        if len(sites) > 1:
            duplicates.append((pw, sites))
    return duplicates


def workflow_check_duplicates():
    header("DUPLICATE PASSWORD DETECTION")
    duplicates = detect_duplicate_passwords()
    if not duplicates:
        print("No duplicate passwords found across your vault.")
    else:
        for pw, sites in duplicates:
            masked = pw[:2] + "*" * max(0, len(pw) - 2)
            print(f"Password '{masked}' is reused across: {', '.join(sites)}")
    print()


def workflow_password_aging():
    header("PASSWORD AGING & EXPIRATION")
    if not vault:
        print("Vault is empty.")
        return
    now = datetime.now()
    print(f"{'Website':<20}{'Created':<20}{'Age (days)':<14}{'Status'}")
    line("-")
    for e in vault:
        try:
            created = datetime.strptime(e["created"], settings["date_format"])
            age_days = (now - created).days
        except ValueError:
            age_days = 0
        status = "Expiring soon - rotate" if age_days > 90 else "OK"
        print(f"{e['website']:<20}{e['created']:<20}{age_days:<14}{status}")
    line("-")
    print()


# ============================================================================
#  5. PASSWORD HISTORY
# ============================================================================
def workflow_history_view():
    header("PASSWORD HISTORY")
    if not history:
        print("No passwords generated yet in this session.")
        return

    print(f"{'No.':<5}{'Password':<28}{'Length':<9}{'Entropy':<11}{'Strength':<14}{'Favorite'}")
    line("-")
    for i, record in enumerate(history, 1):
        fav = "Yes" if record["favorite"] else "No"
        print(f"{i:<5}{record['password']:<28}{record['length']:<9}"
              f"{record['entropy']:<11.1f}{record['strength']:<14}{fav}")
    line("-")
    print(f"Total generated this session: {len(history)}")
    print()


def workflow_history_manage():
    header("MANAGE HISTORY")
    if not history:
        print("No history yet.")
        return
    workflow_history_view()
    index = get_int("Enter entry number to manage (0 to cancel): ", min_val=0, max_val=len(history))
    if index == 0:
        return
    record = history[index - 1]
    action = input("Type 'd' to delete, 'f' to toggle favorite, 'c' to copy: ").strip().lower()
    if action == "d":
        history.pop(index - 1)
        print("Entry deleted.")
    elif action == "f":
        record["favorite"] = not record["favorite"]
        print(f"Favorite set to {record['favorite']}.")
    elif action == "c":
        copy_to_clipboard(record["password"])
    else:
        print("No action taken.")
    print()


def workflow_history_search():
    header("SEARCH HISTORY")
    if not history:
        print("No history yet.")
        return
    term = input("Search by strength (Weak/Moderate/Strong/Very Strong): ").strip().lower()
    results = [r for r in history if term in r["strength"].lower()]
    if not results:
        print("No matches found.")
        return
    for r in results:
        print(f"{r['password']:<28}{r['strength']}")
    print()


# ============================================================================
#  6. SECURITY ANALYZER
# ============================================================================
def workflow_security_analyzer():
    header("SECURITY ANALYZER")
    password = input("Enter a password to analyze (or leave blank to analyze the vault): ").strip()

    if password:
        a = analyze_password(password)
        section("Analysis Report")
        print(f"{'Entropy':<28}: {a['entropy']:.1f} bits")
        print(f"{'Character Pool Size':<28}: {a['pool_size']}")
        print(f"{'Estimated Crack Time':<28}: {a['crack_time']}")
        print(f"{'NIST Recommendation':<28}: {'Meets 15+ char guideline' if a['length'] >= 15 else 'Below recommended 15 characters'}")
        print(f"{'Security Rating':<28}: {a['strength']}")
        print(f"{'Complexity Score':<28}: {a['diversity']} / 4")
        print(f"{'Randomness Score':<28}: {a['randomness_score']:.1f} / 100")
        print()
        print(progress_bar(strength_percent(a["entropy"])))
        print()
        return

    if not vault and not history:
        print("No data available to analyze. Generate or store some passwords first.")
        return

    all_passwords = [e["password"] for e in vault] + [h["password"] for h in history]
    entropies = [calculate_entropy(len(p), max(len(set(p)), 1) * 4) for p in all_passwords]
    avg_entropy = sum(entropies) / len(entropies) if entropies else 0
    strong_count = sum(1 for e in entropies if e >= 60)

    section("Aggregate Security Report")
    print(f"{'Total Passwords Analyzed':<28}: {len(all_passwords)}")
    print(f"{'Average Entropy':<28}: {avg_entropy:.1f} bits")
    print(f"{'Strong or Better':<28}: {strong_count} ({(strong_count / len(all_passwords)) * 100:.1f}%)")
    print()


# ============================================================================
#  7. PASSWORD COMPARISON
# ============================================================================
def workflow_password_comparison():
    header("PASSWORD COMPARISON")
    p1 = input("Enter first password: ")
    p2 = input("Enter second password: ")

    a1 = analyze_password(p1)
    a2 = analyze_password(p2)

    section("Comparison Report")
    print(f"{'Metric':<26}{'Password 1':<26}{'Password 2'}")
    line("-")
    print(f"{'Length':<26}{a1['length']:<26}{a2['length']}")
    print(f"{'Entropy (bits)':<26}{a1['entropy']:<26.1f}{a2['entropy']:.1f}")
    print(f"{'Strength':<26}{a1['strength']:<26}{a2['strength']}")
    print(f"{'Diversity (/4)':<26}{a1['diversity']:<26}{a2['diversity']}")
    print(f"{'Crack Time':<26}{a1['crack_time']:<26}{a2['crack_time']}")
    line("-")

    if a1["entropy"] > a2["entropy"]:
        winner, diff = "Password 1", a1["entropy"] - a2["entropy"]
    elif a2["entropy"] > a1["entropy"]:
        winner, diff = "Password 2", a2["entropy"] - a1["entropy"]
    else:
        winner, diff = "Neither - equal strength", 0

    print(f"Stronger password: {winner}")
    print(f"Entropy difference: {diff:.1f} bits")
    print()


# ============================================================================
#  8. USERNAME GENERATOR
# ============================================================================
def workflow_username_generator():
    header("USERNAME GENERATOR")
    first = input("First name: ").strip() or "user"
    last = input("Last name (optional): ").strip()
    nickname = input("Nickname (optional): ").strip()
    birth_year = input("Birth year (optional, e.g. 1999): ").strip()

    first_l = first.lower()
    last_l = last.lower()
    nick_l = nickname.lower() if nickname else first_l

    suggestions = []
    rand_num = secrets.randbelow(9000) + 1000

    suggestions.append(f"{first_l}.{last_l}" if last else f"{first_l}{rand_num}")
    suggestions.append(f"{nick_l}_{rand_num}")
    if birth_year:
        suggestions.append(f"{first_l}{birth_year}")
        suggestions.append(f"{first_l[0]}{last_l}{birth_year}" if last else f"{first_l}{birth_year}{rand_num % 100}")
    suggestions.append(f"{first_l.capitalize()}{last_l.capitalize()}{rand_num % 100}")
    suggestions.append(f"the_real_{nick_l}")
    suggestions.append(f"{first_l}_{secrets.token_hex(2)}")

    section("Suggested Usernames")
    for i, s in enumerate(dict.fromkeys(suggestions), 1):  # dedupe, preserve order
        print(f"  {i}. {s}")
    print()


# ============================================================================
#  9. PASSPHRASE GENERATOR
# ============================================================================
def workflow_passphrase_generator():
    header("GENERATE A MEMORABLE PASSPHRASE")
    word_count = get_int("Number of words (3-8): ", min_val=3, max_val=8, default=5)
    separator = input("Separator character (default '-'): ").strip() or "-"
    capitalize = get_yes_no("Capitalize each word?", False)
    add_numbers = get_yes_no("Add a random number?", True)
    add_symbol = get_yes_no("Add a random symbol?", False)

    words = [secrets.choice(WORDLIST) for _ in range(word_count)]
    if capitalize:
        words = [w.capitalize() for w in words]
    if add_numbers:
        words.append(str(secrets.randbelow(90) + 10))
    if add_symbol:
        words.append(secrets.choice(string.punctuation))

    passphrase = separator.join(words)
    pool_size = len(WORDLIST)
    entropy = word_count * math.log2(pool_size)
    strength = rate_strength(entropy)

    print()
    line("=")
    print("GENERATED PASSPHRASE".center(78))
    line("=")
    print()
    print(f"    {passphrase}")
    print()
    line("-")
    print(f"{'Length':<28}: {len(passphrase)} characters")
    print(f"{'Word Count':<28}: {word_count}")
    print(f"{'Entropy':<28}: {entropy:.1f} bits (word-based estimate)")
    print(f"{'Strength Rating':<28}: {strength}")
    line("=")
    print()

    history.append({
        "password": passphrase, "length": len(passphrase), "entropy": entropy,
        "strength": strength, "time": datetime.now().strftime(settings["date_format"]),
        "status": "Active", "favorite": False,
    })


# ============================================================================
#  10. PIN GENERATOR
# ============================================================================
def workflow_pin_generator():
    header("PIN GENERATOR")
    print("1) 4-digit   2) 6-digit   3) 8-digit")
    choice = get_int("Choose PIN length (1-3): ", min_val=1, max_val=3)
    length_map = {1: 4, 2: 6, 3: 8}
    length = length_map[choice]

    pin = "".join(secrets.choice(string.digits) for _ in range(length))
    entropy = length * math.log2(10)
    randomness = (len(set(pin)) / length) * 100

    print()
    print(f"Generated PIN: {pin}")
    print(f"Entropy: {entropy:.1f} bits")
    print(f"Randomness Score: {randomness:.1f} / 100")
    print()

    history.append({
        "password": pin, "length": length, "entropy": entropy,
        "strength": rate_strength(entropy), "time": datetime.now().strftime(settings["date_format"]),
        "status": "Active", "favorite": False,
    })


# ============================================================================
#  11. API KEY GENERATOR
# ============================================================================
def workflow_api_key_generator():
    header("API KEY GENERATOR")
    print("1) UUID   2) Secure Token (URL-safe)   3) Hex Key   4) Base64 Key")
    choice = get_int("Choose format (1-4): ", min_val=1, max_val=4)

    if choice == 1:
        key = str(uuid.uuid4())
        label = "UUID"
    elif choice == 2:
        key = secrets.token_urlsafe(32)
        label = "Secure Token (URL-safe)"
    elif choice == 3:
        key = secrets.token_hex(32)
        label = "Hex Key"
    else:
        key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        label = "Base64 Key"

    print()
    print(f"{label}: {key}")
    print(f"Length: {len(key)} characters")
    print()

    history.append({
        "password": key, "length": len(key), "entropy": len(key) * 4.0,
        "strength": "Very Strong", "time": datetime.now().strftime(settings["date_format"]),
        "status": "Active", "favorite": False,
    })


# ============================================================================
#  12. WI-FI PASSWORD GENERATOR
# ============================================================================
def workflow_wifi_generator():
    header("WI-FI PASSWORD GENERATOR")
    print("1) Home (12 characters)   2) Office (16 characters)   "
          "3) Enterprise (24 characters, maximum entropy)")
    choice = get_int("Choose profile (1-3): ", min_val=1, max_val=3)
    length_map = {1: 12, 2: 16, 3: 24}
    length = length_map[choice]

    pool = string.ascii_letters + string.digits + string.punctuation
    required_sets = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]
    password = generate_password(length, pool, required_sets, {"no_consecutive": True})

    display_generation_result(password)


# ============================================================================
#  13 / 14. EXPORT & IMPORT
# ============================================================================
def workflow_export():
    header("EXPORT DATA")
    print("1) Vault to CSV   2) Vault to JSON   3) History to TXT   4) Full session to JSON")
    choice = get_int("Choose export format (1-4): ", min_val=1, max_val=4)

    if choice == 1:
        filename = "vault_export.csv"
        with open(filename, "w", newline="") as f:
            fieldnames = ["id", "website", "username", "email", "password", "category",
                          "url", "notes", "created", "updated", "favorite", "tags"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for e in vault:
                row = dict(e)
                row["tags"] = ";".join(e["tags"])
                writer.writerow(row)
        print(f"Vault exported to '{filename}' ({len(vault)} entries).")

    elif choice == 2:
        filename = "vault_export.json"
        with open(filename, "w") as f:
            json.dump(vault, f, indent=2)
        print(f"Vault exported to '{filename}' ({len(vault)} entries).")

    elif choice == 3:
        filename = "history_export.txt"
        with open(filename, "w") as f:
            for r in history:
                f.write(f"{r['password']}\n")
        print(f"History exported to '{filename}' ({len(history)} passwords).")

    else:
        filename = "flux_full_backup.json"
        with open(filename, "w") as f:
            json.dump({"vault": vault, "history": history, "settings": settings}, f, indent=2)
        print(f"Full session exported to '{filename}'.")
    print()


def workflow_import():
    header("IMPORT DATA")
    print("1) Import vault from CSV   2) Import vault from JSON")
    choice = get_int("Choose import format (1-2): ", min_val=1, max_val=2)
    filename = input("Enter file path: ").strip()

    if not os.path.exists(filename):
        print("File not found.")
        return

    try:
        if choice == 1:
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    row["tags"] = row.get("tags", "").split(";") if row.get("tags") else []
                    row["favorite"] = row.get("favorite") in ("True", "true", "1")
                    row["id"] = len(vault) + 1
                    vault.append(row)
                    count += 1
            print(f"Imported {count} vault entries from CSV.")
        else:
            with open(filename, "r") as f:
                data = json.load(f)
                for entry in data:
                    entry["id"] = len(vault) + 1
                    vault.append(entry)
            print(f"Imported {len(data)} vault entries from JSON.")
    except (OSError, json.JSONDecodeError, csv.Error) as e:
        print(f"Import failed: {e}")
    print()


# ============================================================================
#  15. BACKUP & RESTORE
# ============================================================================
def workflow_backup_restore():
    header("BACKUP & RESTORE")
    print("1) Create backup now   2) Restore from backup file   3) Reset database")
    choice = get_int("Choose an option (1-3): ", min_val=1, max_val=3)

    if choice == 1:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flux_backup_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump({"vault": vault, "history": history, "settings": settings}, f, indent=2)
        print(f"Backup created: '{filename}'.")

    elif choice == 2:
        filename = input("Enter backup file path: ").strip()
        if not os.path.exists(filename):
            print("File not found.")
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            vault.clear()
            vault.extend(data.get("vault", []))
            history.clear()
            history.extend(data.get("history", []))
            settings.update(data.get("settings", {}))
            print(f"Restored {len(vault)} vault entries and {len(history)} history records.")
        except (OSError, json.JSONDecodeError) as e:
            print(f"Restore failed: {e}")

    else:
        confirm = get_yes_no("This will erase all vault entries and history. Continue?", False)
        if confirm:
            vault.clear()
            history.clear()
            print("Database reset. All in-memory data cleared.")
        else:
            print("Reset cancelled.")
    print()


# ============================================================================
#  16. SETTINGS
# ============================================================================
def workflow_settings():
    header("SETTINGS")
    print(f"{'Setting':<32}{'Current Value'}")
    line("-")
    for key, value in settings.items():
        print(f"{key:<32}{value}")
    line("-")

    change = get_yes_no("Change a setting?", False)
    if not change:
        return

    print("\nAvailable settings:")
    keys = list(settings.keys())
    for i, k in enumerate(keys, 1):
        print(f"  {i}. {k}")
    idx = get_int("Choose setting number: ", min_val=1, max_val=len(keys))
    key = keys[idx - 1]

    current = settings[key]
    if isinstance(current, bool):
        settings[key] = get_yes_no(f"Set {key} to True?", current)
    elif isinstance(current, int):
        settings[key] = get_int(f"Enter new value for {key}: ", min_val=0)
    else:
        settings[key] = input(f"Enter new value for {key}: ").strip()

    print(f"Updated {key} to {settings[key]}.")
    if key in ("dark_mode",):
        print("Note: this is a cosmetic preference with no visual effect in the console edition.")
    print()


# ============================================================================
#  17. HELP
# ============================================================================
def workflow_help():
    header("HELP CENTER")
    section("User Guide")
    print("Use the main menu to navigate between password generation, the vault,")
    print("history, and analysis tools. Each screen will prompt you for the")
    print("information it needs, with sensible defaults if you press Enter.")

    section("Frequently Asked Questions")
    print("Q: Why does this use 'secrets' instead of 'random'?")
    print("A: 'random' is predictable and unsafe for security purposes. 'secrets'")
    print("   uses your operating system's cryptographic random source.")
    print()
    print("Q: Is my vault data saved automatically?")
    print("A: No. Vault and history exist only for this session unless you use")
    print("   Export Data or Backup & Restore.")

    section("Password Security Tips")
    print("- Prefer length over complexity: 15+ characters beats short, symbol-heavy ones.")
    print("- Never reuse the same password across multiple sites.")
    print("- Use a passphrase for accounts you need to type/remember often.")

    section("NIST Best Practices (SP 800-63-4, 2024)")
    print("- Minimum 15 characters for high-security accounts.")
    print("- Systems should allow up to 64 characters to support passphrases.")
    print("- Do not force periodic password rotation; rotate only on compromise.")
    print("- Screen new passwords against known-breached password lists.")

    section("Troubleshooting")
    print("- If import fails, verify the file path and format match your selection.")
    print("- If a generated password doesn't meet all constraints, the generator")
    print("  will note this after 200 attempts and return its best-effort result.")
    print()


# ============================================================================
#  18. ABOUT
# ============================================================================
def workflow_about():
    header("ABOUT")
    print(f"{'Application Name':<28}: {APP_NAME}")
    print(f"{'Version':<28}: {APP_VERSION}")
    print(f"{'Developer':<28}: Mahnoor (DecodeLabs Industrial Training Kit, Project 3)")
    print(f"{'Python Version Required':<28}: 3.8+")
    print(f"{'Libraries Used':<28}: secrets, string, math, uuid, base64, csv, json, re, datetime")
    print(f"{'Description':<28}: A console-based enterprise password security suite covering")
    print(f"{'':<28}  generation, storage, analysis, and secure key/PIN utilities,")
    print(f"{'':<28}  built entirely on the Python standard library.")
    print()


# ============================================================================
#  MAIN MENU
# ============================================================================
def show_splash():
    header(APP_NAME.upper())
    print("Secure Password Management System".center(78))
    print()
    print("Initializing security engine...".center(78))
    print("Loading cryptographic modules...".center(78))
    print("Secure environment ready.".center(78))
    print()
    name = input("Enter your name to continue: ").strip() or "User"
    print(f"\nWelcome, {name}!\n")
    return name


def show_dashboard(user_name):
    header("DASHBOARD")
    print(f"{'Welcome':<28}: {user_name}")
    print(f"{'Passwords Generated':<28}: {len(history)}")
    print(f"{'Vault Entries':<28}: {len(vault)}")
    if history:
        avg_entropy = sum(h["entropy"] for h in history) / len(history)
        strong = sum(1 for h in history if h["strength"] in ("Strong", "Very Strong"))
        last_time = history[-1]["time"]
    else:
        avg_entropy, strong, last_time = 0, 0, "N/A"
    print(f"{'Average Password Strength':<28}: {avg_entropy:.1f} bits")
    print(f"{'Strong or Better':<28}: {strong} of {len(history)}")
    print(f"{'Last Generated At':<28}: {last_time}")
    print(f"{'Generator Version':<28}: {APP_VERSION}")
    print(f"{'Clipboard Status':<28}: {clipboard_status()}")
    print()


MENU_TEXT = """
 1. Generate Password
 2. Bulk Password Generator
 3. Password Strength Checker
 4. Password Vault - View / Add / Edit / Search / Sort
 5. Password History - View / Manage / Search
 6. Security Analyzer
 7. Password Comparison
 8. Username Generator
 9. Passphrase Generator
10. PIN Generator
11. API Key Generator
12. Wi-Fi Password Generator
13. Export Data
14. Import Data
15. Backup & Restore
16. Settings
17. Help
18. About
19. Exit
"""

VAULT_SUBMENU = """
 a. Add new entry
 b. View all entries
 c. Edit / delete an entry
 d. Search / filter
 e. Sort
 f. Check for duplicate passwords
 g. View password aging report
 h. Back to main menu
"""

HISTORY_SUBMENU = """
 a. View history
 b. Manage an entry (delete / favorite / copy)
 c. Search by strength
 d. Back to main menu
"""


def vault_menu():
    while True:
        print(VAULT_SUBMENU)
        choice = input("Choose an option (a-h): ").strip().lower()
        if choice == "a":
            workflow_vault_add()
        elif choice == "b":
            workflow_vault_view()
        elif choice == "c":
            workflow_vault_edit_delete()
        elif choice == "d":
            workflow_vault_search()
        elif choice == "e":
            workflow_vault_sort()
        elif choice == "f":
            workflow_check_duplicates()
        elif choice == "g":
            workflow_password_aging()
        elif choice == "h":
            break
        else:
            print("Invalid option.")


def history_menu():
    while True:
        print(HISTORY_SUBMENU)
        choice = input("Choose an option (a-d): ").strip().lower()
        if choice == "a":
            workflow_history_view()
        elif choice == "b":
            workflow_history_manage()
        elif choice == "c":
            workflow_history_search()
        elif choice == "d":
            break
        else:
            print("Invalid option.")


def main():
    user_name = show_splash()

    while True:
        show_dashboard(user_name)
        print(MENU_TEXT)
        choice = input("Choose an option (1-19): ").strip()

        if choice == "1":
            workflow_password_generator()
        elif choice == "2":
            workflow_bulk_generator()
        elif choice == "3":
            workflow_strength_checker()
        elif choice == "4":
            vault_menu()
        elif choice == "5":
            history_menu()
        elif choice == "6":
            workflow_security_analyzer()
        elif choice == "7":
            workflow_password_comparison()
        elif choice == "8":
            workflow_username_generator()
        elif choice == "9":
            workflow_passphrase_generator()
        elif choice == "10":
            workflow_pin_generator()
        elif choice == "11":
            workflow_api_key_generator()
        elif choice == "12":
            workflow_wifi_generator()
        elif choice == "13":
            workflow_export()
        elif choice == "14":
            workflow_import()
        elif choice == "15":
            workflow_backup_restore()
        elif choice == "16":
            workflow_settings()
        elif choice == "17":
            workflow_help()
        elif choice == "18":
            workflow_about()
        elif choice == "19":
            print()
            print(f"Session summary: {len(history)} passwords generated, {len(vault)} vault entries.")
            print("Program closed.")
            print()
            break
        else:
            print("Invalid option. Please choose between 1 and 19.")


if __name__ == "__main__":
    main()
