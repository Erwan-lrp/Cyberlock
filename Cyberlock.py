import tkinter as tk
import json, os, secrets, string, random, math

# ============================================================
#  CONFIGURATION
# ============================================================
VAULT_FILE  = "vault.json"
MASTER_FILE = "master.txt"
BG     = "#000000"
ACCENT = "#00ff9c"
FG     = "#e2e8f0"
DIM    = "#004d2e"
FONT   = "Consolas"

CODE_PREFIXES = ["[SYS]", "0x", ">>", "//", "def ", "import ", "$ sudo",
                 ">>>", "sys.", "[ROOT]", "EXEC>", "~/"]
CODE_WORDS    = ["access", "decrypt", "vault", "root", "kernel", "firewall",
                 "bypass", "payload", "hash", "encrypt", "breach", "node",
                 "server", "protocol", "socket", "token", "auth", "exploit",
                 "buffer", "stack", "memory", "pointer", "shell", "exec"]


# ============================================================
#  UTILITAIRES FICHIERS
# ============================================================
def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_text(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return None

def save_text(path, text):
    with open(path, "w") as f:
        f.write(text)

def generate_password(length=20):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=?"
    return "".join(secrets.choice(chars) for _ in range(length))


# ============================================================
#  GÉNÉRATION DE LIGNES DE CODE
# ============================================================
def random_code_line():
    line = random.choice(CODE_PREFIXES) + " "
    for _ in range(random.randint(3, 8)):
        line += random.choice(CODE_WORDS)
        line += random.choice(["()", ".", "=", "->", "::", "_", " ", "[]", "{}"])
    if random.random() > 0.4:
        line += " 0x" + "".join(random.choice("0123456789ABCDEF") for _ in range(8))
    return line.strip()[:100]

def random_hex_block():
    return " ".join(
        "".join(random.choice("0123456789ABCDEF") for _ in range(2))
        for _ in range(random.randint(8, 16))
    )

def random_binary_line():
    return "".join(random.choice("01") for _ in range(random.randint(40, 70)))


# ============================================================
#  WIDGETS RÉUTILISABLES
# ============================================================
def make_label(parent, text, size=18, bold=False, color=FG):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=(FONT, size, weight), fg=color, bg=BG)

def make_button(parent, text, command, bg=ACCENT, fg=BG, size=16, width=None):
    kwargs = dict(text=text, font=(FONT, size), bg=bg, fg=fg, command=command,
                  relief="flat", activebackground=ACCENT, activeforeground=BG,
                  cursor="hand2")
    if width:
        kwargs["width"] = width
    return tk.Button(parent, **kwargs)

def make_entry(parent, var, show="", width=35):
    return tk.Entry(parent, textvariable=var, show=show,
                    font=(FONT, 18), width=width,
                    bg="#0a1a0e", fg=ACCENT, insertbackground=ACCENT,
                    relief="flat", highlightthickness=1,
                    highlightcolor=ACCENT, highlightbackground=DIM)

def toggle_visibility(entry):
    entry.config(show="" if entry.cget("show") == "*" else "*")


# ============================================================
#  FOND HACKER ANIMÉ (3 couches)
# ============================================================
class HackerBackground:
    def __init__(self, root):
        self.root    = root
        self.running = True
        self.canvas  = tk.Canvas(root, bg=BG, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()

        # Couche 1 : colonnes de hex tombants
        col_spacing = 22
        self.cols = []
        for x in range(0, sw + col_spacing, col_spacing):
            self.cols.append({
                "x":        x,
                "y":        random.randint(-sh, 0),
                "speed":    random.uniform(0.8, 2.8),
                "chars":    [random.choice("0123456789ABCDEF")
                             for _ in range(random.randint(6, 18))],
                "bright_idx": 0,
            })

        # Couche 2 : lignes de code larges
        self.code_lines = []
        for _ in range(20):
            kind = random.choice(["code", "hex", "binary"])
            self.code_lines.append({
                "x":     random.randint(0, sw),
                "y":     random.randint(-sh, 0),
                "speed": random.uniform(0.4, 1.2),
                "text":  self._rand_text(kind),
                "kind":  kind,
                "alpha": random.uniform(0.15, 0.45),
            })

        # Couche 3 : pixels clignotants
        self.sparks = []
        for _ in range(80):
            self.sparks.append({
                "x":   random.randint(0, sw),
                "y":   random.randint(0, sh),
                "life": random.randint(0, 20),
                "max":  random.randint(10, 30),
            })

        self._draw()

    def _rand_text(self, kind):
        if kind == "hex":    return random_hex_block()
        if kind == "binary": return random_binary_line()
        return random_code_line()

    def _green(self, brightness):
        v = max(0.0, min(1.0, brightness))
        return f"#{int(0*v):02x}{int(255*v):02x}{int(80*v):02x}"

    def _draw(self):
        if not self.running:
            return
        try:
            cv = self.canvas
            cv.delete("all")
            sh = self.root.winfo_height()
            sw = self.root.winfo_screenwidth()

            # Couche 1
            for col in self.cols:
                x, y0  = col["x"], col["y"]
                chars   = col["chars"]
                bright  = col["bright_idx"]
                for i, ch in enumerate(chars):
                    yi = y0 + i * 16
                    if yi < -16 or yi > sh + 16:
                        continue
                    if i == bright:
                        color = "#ccffdd"
                    elif i >= bright - 3:
                        color = self._green(0.75 - (bright - i) * 0.15)
                    else:
                        color = self._green(0.18)
                    cv.create_text(x, yi, text=ch, fill=color,
                                   font=(FONT, 11), anchor="center")
                col["y"] += col["speed"]
                col["bright_idx"] = (col["bright_idx"] + 1) % len(chars)
                if col["y"] > sh + len(chars) * 16:
                    col["y"]     = random.randint(-sh // 2, -60)
                    col["chars"] = [random.choice("0123456789ABCDEF")
                                    for _ in range(random.randint(6, 18))]
                    col["speed"] = random.uniform(0.8, 2.8)

            # Couche 2
            for ln in self.code_lines:
                color = self._green(ln["alpha"])
                cv.create_text(ln["x"], ln["y"], text=ln["text"],
                               fill=color, font=(FONT, 10), anchor="w")
                ln["y"] += ln["speed"]
                if ln["y"] > sh + 30:
                    ln.update(y=random.randint(-200, -20),
                               x=random.randint(0, sw),
                               text=self._rand_text(ln["kind"]),
                               speed=random.uniform(0.4, 1.2),
                               alpha=random.uniform(0.15, 0.45))

            # Couche 3
            for sp in self.sparks:
                sp["life"] += 1
                bright = math.sin(sp["life"] / sp["max"] * math.pi)
                if bright > 0.05:
                    color = self._green(bright * 0.7)
                    cv.create_rectangle(sp["x"], sp["y"],
                                        sp["x"] + 2, sp["y"] + 2,
                                        fill=color, outline="")
                if sp["life"] >= sp["max"]:
                    sp.update(x=random.randint(0, sw),
                               y=random.randint(0, sh),
                               life=0, max=random.randint(10, 30))
        except Exception:
            pass

        self.root.after(45, self._draw)

    def stop(self):
        self.running = False


# ============================================================
#  ÉCRAN DE CHARGEMENT HACKER
# ============================================================
class LoadingScreen:
    BOOT_MESSAGES = [
        "[INIT]   Chargement du noyau sécurisé...",
        "[SYS]    Vérification de l'intégrité système...",
        "[CRYPTO] Initialisation du module AES-256...",
        "[NET]    Isolation du réseau local...",
        "[MEM]    Allocation des buffers sécurisés...",
        "[VAULT]  Lecture du coffre chiffré...",
        "[AUTH]   Chargement du module d'authentification...",
        "[HASH]   Calcul des checksums...",
        "[SEC]    Activation du pare-feu interne...",
        "[OK]     Environnement sécurisé prêt.",
        "[BOOT]   Lancement de CyberLock...",
    ]

    def __init__(self, root, on_done):
        self.root    = root
        self.on_done = on_done
        self.win     = tk.Toplevel(root)
        self.win.attributes("-fullscreen", True)
        self.win.overrideredirect(True)
        self.win.configure(bg=BG)
        self._bg_running = True
        self._glitch_id  = None
        self._msg_id     = None
        self._build_ui()
        self._msg_idx = 0
        self._title_tick()
        self._next_message()

    def _build_ui(self):
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()

        # Fond animé binaire
        self.bg_canvas = tk.Canvas(self.win, bg=BG, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)
        self._bg_cols = [{
            "x": x, "y": random.randint(-sh, 0),
            "speed": random.uniform(1, 3),
            "chars": [random.choice("01") for _ in range(random.randint(4, 14))]
        } for x in range(0, sw, 28)]
        self._draw_bg()

        # Titre
        self.title_var = tk.StringVar(value="CYBERLOCK")
        tk.Label(self.win, textvariable=self.title_var,
                 font=(FONT, 72, "bold"), fg=ACCENT, bg=BG).pack(pady=(70, 5))
        tk.Label(self.win, text="[ SECURE PASSWORD VAULT v2.0 ]",
                 font=(FONT, 15), fg=DIM, bg=BG).pack(pady=(0, 30))

        # Zone terminal
        term = tk.Frame(self.win, bg="#050f07",
                         highlightthickness=1, highlightbackground=DIM)
        term.pack(padx=180, pady=8, fill="x")
        tk.Label(term, text="root@cyberlock:~$ boot --secure",
                 font=(FONT, 12), fg=DIM, bg="#050f07", anchor="w").pack(
                 fill="x", padx=14, pady=(7, 3))
        self.term_lines = []
        for _ in range(8):
            lbl = tk.Label(term, text="", font=(FONT, 11),
                           fg=ACCENT, bg="#050f07", anchor="w")
            lbl.pack(fill="x", padx=14, pady=1)
            self.term_lines.append(lbl)
        tk.Label(term, text="", bg="#050f07").pack(pady=3)

        # Barre de progression
        bar_row = tk.Frame(self.win, bg=BG)
        bar_row.pack(pady=25)
        tk.Label(bar_row, text="INITIALISATION  ",
                 font=(FONT, 13), fg=DIM, bg=BG).pack(side="left")
        self.bar_cv = tk.Canvas(bar_row, width=580, height=24,
                                 bg="#050f07", highlightthickness=1,
                                 highlightbackground=ACCENT)
        self.bar_cv.pack(side="left")
        self.bar_rect = self.bar_cv.create_rectangle(0, 0, 0, 24, fill=ACCENT, outline="")
        self.pct_var = tk.StringVar(value="  0%")
        tk.Label(bar_row, textvariable=self.pct_var,
                 font=(FONT, 13), fg=ACCENT, bg=BG, width=5).pack(side="left")

    def _draw_bg(self):
        if not self._bg_running:
            return
        try:
            cv = self.bg_canvas
            cv.delete("all")
            sh = self.win.winfo_height()
            for col in self._bg_cols:
                for i, ch in enumerate(col["chars"]):
                    yi = col["y"] + i * 18
                    if 0 <= yi <= sh:
                        cv.create_text(col["x"], yi, text=ch,
                                       fill="#003318", font=(FONT, 10))
                col["y"] += col["speed"]
                if col["y"] > sh + 14 * 18:
                    col["y"]     = random.randint(-sh // 2, -50)
                    col["chars"] = [random.choice("01")
                                    for _ in range(random.randint(4, 14))]
        except Exception:
            pass
        self.win.after(60, self._draw_bg)

    def _title_tick(self):
        glitch_chars = "!@#$%&?█▓▒░<>[]|"
        try:
            if random.random() < 0.3:
                t = "CYBERLOCK"
                p = random.randint(0, len(t) - 1)
                self.title_var.set(t[:p] + random.choice(glitch_chars) + t[p+1:])
                self.win.after(90, lambda: self.title_var.set("CYBERLOCK"))
            self._glitch_id = self.win.after(320, self._title_tick)
        except Exception:
            pass

    def _next_message(self):
        idx   = self._msg_idx
        total = len(self.BOOT_MESSAGES)
        if idx < total:
            # Défile les lignes
            for i in range(len(self.term_lines) - 1):
                self.term_lines[i].config(
                    text=self.term_lines[i+1].cget("text"),
                    fg=self.term_lines[i+1].cget("fg"))
            msg   = self.BOOT_MESSAGES[idx]
            color = "#00ff9c" if "[OK]" in msg or "[BOOT]" in msg else "#00cc7a"
            self.term_lines[-1].config(text=msg, fg=color)

            pct   = int((idx + 1) / total * 100)
            bar_w = int((idx + 1) / total * 580)
            self.bar_cv.coords(self.bar_rect, 0, 0, bar_w, 24)
            self.pct_var.set(f" {pct:3d}%")

            self._msg_idx += 1
            delay = 200 if idx < total - 2 else 500
            self._msg_id = self.win.after(delay, self._next_message)
        else:
            self.win.after(700, self._finish)

    def _finish(self):
        self._bg_running = False
        self.win.destroy()
        self.on_done()


# ============================================================
#  POPUP PERSONNALISÉE
# ============================================================
class Popup(tk.Toplevel):
    def __init__(self, root, title, message, kind="info", callback=None):
        super().__init__(root)
        self.configure(bg=BG)
        self.title("CyberLock")
        self.geometry("640x340")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grab_set()
        self.update_idletasks()
        x = (root.winfo_screenwidth()  - 640) // 2
        y = (root.winfo_screenheight() - 340) // 2 - 50
        self.geometry(f"+{x}+{y}")

        border = tk.Frame(self, bg=ACCENT, padx=2, pady=2)
        border.pack(fill="both", expand=True, padx=8, pady=8)
        inner  = tk.Frame(border, bg=BG)
        inner.pack(fill="both", expand=True)

        make_label(inner, title,   size=22, bold=True, color=ACCENT).pack(pady=(28, 10))
        make_label(inner, message, size=14).pack(pady=18, padx=40)

        btn_frame = tk.Frame(inner, bg=BG)
        btn_frame.pack(pady=22)

        def close(result=None):
            self.destroy()
            if callable(callback):
                callback(result)

        if kind == "yesno":
            make_button(btn_frame, "OUI", lambda: close(True),
                        bg="#00aa00", fg="white", size=17, width=12).pack(side="left", padx=40)
            make_button(btn_frame, "NON", lambda: close(False),
                        bg="#aa0000", fg="white", size=17, width=12).pack(side="left", padx=40)
        else:
            make_button(btn_frame, "OK", close, size=17, width=14).pack()


# ============================================================
#  APPLICATION PRINCIPALE
# ============================================================
class CyberLock:

    def __init__(self):
        self.vault           = load_json(VAULT_FILE)
        self.master_password = load_text(MASTER_FILE)

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)
        self.root.title("CyberLock")
        self.root.bind("<F11>", lambda e: self.root.attributes(
            "-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.hacker_bg = HackerBackground(self.root)

        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.place(relwidth=1, relheight=1)

        self.root.withdraw()
        self.root.after(100, self._start_loading)
        self.root.mainloop()

    def _start_loading(self):
        self.root.deiconify()
        LoadingScreen(self.root, self._show_master_screen)

    def _on_close(self):
        self.hacker_bg.stop()
        self.root.destroy()

    # ── Helpers ─────────────────────────────────────────────
    def clear(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    def popup(self, title, message, kind="info", callback=None):
        Popup(self.root, title, message, kind, callback)

    def copy(self, text):
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        lbl = make_label(self.main_frame, "✓ Copié dans le presse-papiers", size=13, color=ACCENT)
        lbl.pack()
        self.root.after(1800, lbl.destroy)

    # ── Écran mot de passe maître ────────────────────────────
    def _show_master_screen(self):
        self.clear()
        make_label(self.main_frame, "🔐 MOT DE PASSE MAÎTRE",
                   size=40, bold=True, color=ACCENT).pack(pady=(90, 35))

        if self.master_password is None:
            make_label(self.main_frame,
                       "Première utilisation — choisissez votre mot de passe maître",
                       size=14, color=DIM).pack(pady=(0, 15))

        self._pwd_var = tk.StringVar()
        row = tk.Frame(self.main_frame, bg=BG)
        row.pack(pady=15)
        entry = make_entry(row, self._pwd_var, show="*", width=30)
        entry.pack(side="left", padx=10)
        entry.focus_set()
        entry.bind("<Return>", lambda e: self._check_master())
        make_button(row, "👁️", lambda: toggle_visibility(entry),
                    bg=BG, fg=ACCENT, size=16).pack(side="left")

        self._bar_cv = tk.Canvas(self.main_frame, width=680, height=5,
                                  bg="#0a1a0e", highlightthickness=0)
        self._bar_cv.pack(pady=30)
        self._bar = self._bar_cv.create_rectangle(0, 0, 0, 5, fill=ACCENT, outline="")

        make_button(self.main_frame, "[ VALIDER ]", self._check_master, size=20).pack(pady=12)

    def _check_master(self):
        entered = self._pwd_var.get().strip()
        if not entered:
            return
        if self.master_password is None:
            self.master_password = entered
            save_text(MASTER_FILE, entered)
            self._animate_bar(self._screen_granted)
        elif entered == self.master_password:
            self._animate_bar(self._screen_granted)
        else:
            self._animate_bar(self._screen_denied)

    def _animate_bar(self, next_fn, w=0):
        if w <= 680:
            self._bar_cv.coords(self._bar, 0, 0, w, 5)
            self.root.after(4, lambda: self._animate_bar(next_fn, w + 14))
        else:
            next_fn()

    def _screen_granted(self):
        self.clear()
        f = tk.Frame(self.main_frame, bg="#001a0a")
        f.place(relwidth=1, relheight=1)
        make_label(f, "▓▓▓  ACCÈS AUTORISÉ  ▓▓▓",
                   size=52, bold=True, color=ACCENT).pack(expand=True)
        self.root.after(900, self._show_main_screen)

    def _screen_denied(self):
        self.clear()
        f = tk.Frame(self.main_frame, bg="#1a0000")
        f.place(relwidth=1, relheight=1)
        make_label(f, "▓▓▓  ACCÈS REFUSÉ  ▓▓▓",
                   size=52, bold=True, color="#ff3333").pack(expand=True)
        self.root.after(1100, self._show_master_screen)

    # ── Écran principal ──────────────────────────────────────
    def _show_main_screen(self):
        self.clear()
        hdr = tk.Frame(self.main_frame, bg=BG)
        hdr.pack(fill="x", padx=80, pady=(16, 4))
        make_label(hdr, "🔐 CYBERLOCK", size=36, bold=True, color=ACCENT).pack(side="left")
        count = len(self.vault)
        make_label(hdr, f"{count} compte{'s' if count != 1 else ''} stocké{'s' if count != 1 else ''}",
                   size=13, color=DIM).pack(side="right", padx=10)

        tk.Frame(self.main_frame, bg=ACCENT, height=1).pack(fill="x", padx=80, pady=(0, 8))

        self._listbox = tk.Listbox(
            self.main_frame, font=(FONT, 17),
            bg="#050f07", fg=ACCENT,
            selectbackground=ACCENT, selectforeground=BG,
            height=12, borderwidth=0,
            highlightthickness=1, highlightcolor=DIM, highlightbackground=DIM)
        self._listbox.pack(fill="both", expand=True, padx=80, pady=5)
        self._listbox.bind("<Double-Button-1>", self._view_entry)
        self._refresh_list()

        row = tk.Frame(self.main_frame, bg=BG)
        row.pack(pady=16)
        for i, (lbl, cmd) in enumerate([
            ("[ + ] Ajouter",    self._add_form),
            ("[ - ] Supprimer",  self._delete_entry),
            ("[ * ] Maître",     self._change_master),
            ("[ # ] Générateur", self._show_generator),
        ]):
            make_button(row, lbl, cmd, width=18, size=14).grid(row=0, column=i, padx=10)

    def _refresh_list(self):
        self._listbox.delete(0, tk.END)
        for site in sorted(self.vault.keys()):
            self._listbox.insert(tk.END, f"  {site}")

    # ── Voir un compte ───────────────────────────────────────
    def _view_entry(self, _event=None):
        try:
            site = self._listbox.get(self._listbox.curselection()[0]).strip()
        except Exception:
            return
        data = self.vault.get(site, {})
        if not data:
            return

        self.clear()
        make_label(self.main_frame, f"🔑 {site.upper()}",
                   size=28, bold=True, color=ACCENT).pack(pady=(40, 15))
        tk.Frame(self.main_frame, bg=ACCENT, height=1).pack(fill="x", padx=120, pady=(0, 20))

        for field_name, field_key, masked in [
            ("Nom d'utilisateur", "username", False),
            ("Mot de passe",      "password", True),
        ]:
            make_label(self.main_frame, field_name, size=15, color=DIM).pack(pady=(12, 4))
            row = tk.Frame(self.main_frame, bg=BG)
            row.pack(pady=4)
            val = data.get(field_key, "")

            if masked:
                dv = tk.StringVar(value="●" * len(val))
                tk.Label(row, textvariable=dv, font=(FONT, 17),
                         fg=ACCENT, bg="#050f07", width=38, anchor="center",
                         padx=10, pady=6).pack(side="left")
                def _tog(v=val, d=dv):
                    d.set(v if d.get().startswith("●") else "●" * len(v))
                make_button(row, "👁️",       _tog,               bg=BG, fg=ACCENT, size=14).pack(side="left", padx=6)
                make_button(row, "📋 Copier", lambda v=val: self.copy(v), bg=BG, fg=ACCENT, size=14).pack(side="left", padx=6)
            else:
                tk.Label(row, text=val, font=(FONT, 17), fg=ACCENT,
                         bg="#050f07", width=38, anchor="center",
                         padx=10, pady=6).pack(side="left")
                make_button(row, "📋 Copier", lambda v=val: self.copy(v),
                            bg=BG, fg=ACCENT, size=14).pack(side="left", padx=6)

        make_button(self.main_frame, "← Retour", self._show_main_screen,
                    bg=BG, fg=ACCENT, size=17).pack(pady=50)

    # ── Ajouter un compte ────────────────────────────────────
    def _add_form(self):
        self.clear()
        make_label(self.main_frame, "[ + ] AJOUTER UN COMPTE",
                   size=30, bold=True, color=ACCENT).pack(pady=(45, 8))
        tk.Frame(self.main_frame, bg=ACCENT, height=1).pack(fill="x", padx=120, pady=(0, 18))

        site_v, user_v, pwd_v = tk.StringVar(), tk.StringVar(), tk.StringVar()

        make_label(self.main_frame, "Site / Service",   size=15, color=DIM).pack(pady=(14, 4))
        make_entry(self.main_frame, site_v, width=42).pack()
        make_label(self.main_frame, "Nom d'utilisateur", size=15, color=DIM).pack(pady=(14, 4))
        make_entry(self.main_frame, user_v, width=42).pack()
        make_label(self.main_frame, "Mot de passe",      size=15, color=DIM).pack(pady=(14, 4))

        row = tk.Frame(self.main_frame, bg=BG)
        row.pack(pady=4)
        pwd_entry = make_entry(row, pwd_v, show="*", width=32)
        pwd_entry.pack(side="left")
        make_button(row, "👁️",      lambda: toggle_visibility(pwd_entry), bg=BG, fg=ACCENT, size=15).pack(side="left", padx=6)
        make_button(row, "Générer", lambda: pwd_v.set(generate_password()), bg=DIM, fg=ACCENT, size=13).pack(side="left", padx=6)

        def save():
            site = site_v.get().strip()
            if not site:
                self.popup("ERREUR", "Le nom du site est obligatoire !")
                return
            if site in self.vault:
                self.popup("ERREUR", "Ce site existe déjà !")
                return
            self.vault[site] = {"username": user_v.get().strip(), "password": pwd_v.get().strip()}
            save_json(VAULT_FILE, self.vault)
            self.popup("SUCCÈS", f"Compte « {site} » ajouté !", callback=self._show_main_screen)

        row2 = tk.Frame(self.main_frame, bg=BG)
        row2.pack(pady=28)
        make_button(row2, "[ ENREGISTRER ]", save,                   size=17).pack(side="left", padx=20)
        make_button(row2, "← Retour",        self._show_main_screen, bg=BG, fg=ACCENT, size=15).pack(side="left", padx=20)

    # ── Supprimer un compte ──────────────────────────────────
    def _delete_entry(self):
        try:
            site = self._listbox.get(self._listbox.curselection()[0]).strip()
        except Exception:
            self.popup("ATTENTION", "Sélectionne un site à supprimer.")
            return

        def confirm(yes):
            if yes:
                del self.vault[site]
                save_json(VAULT_FILE, self.vault)
                self._refresh_list()
                self.popup("SUPPRIMÉ", f"« {site} » supprimé avec succès.")

        self.popup("CONFIRMATION",
                   f"Supprimer « {site} » ?\nCette action est irréversible.",
                   kind="yesno", callback=confirm)

    # ── Modifier le mot de passe maître ─────────────────────
    def _change_master(self):
        self.clear()
        make_label(self.main_frame, "[ * ] MOT DE PASSE MAÎTRE",
                   size=28, bold=True, color=ACCENT).pack(pady=(45, 8))
        tk.Frame(self.main_frame, bg=ACCENT, height=1).pack(fill="x", padx=120, pady=(0, 18))

        old_v, new_v, cfm_v = tk.StringVar(), tk.StringVar(), tk.StringVar()
        err = tk.Label(self.main_frame, text="", fg="#ff4444", bg=BG, font=(FONT, 13))
        err.pack(pady=6)

        for lbl_text, var in [("Ancien mot de passe", old_v),
                               ("Nouveau mot de passe", new_v),
                               ("Confirmer", cfm_v)]:
            make_label(self.main_frame, lbl_text, size=14, color=DIM).pack(pady=(12, 4))
            make_entry(self.main_frame, var, show="*", width=36).pack()

        def validate():
            if old_v.get() != self.master_password:
                err.config(text="Ancien mot de passe incorrect"); return
            if not new_v.get():
                err.config(text="Le nouveau mot de passe ne peut pas être vide"); return
            if new_v.get() != cfm_v.get():
                err.config(text="Les nouveaux mots de passe ne correspondent pas"); return
            self.master_password = new_v.get()
            save_text(MASTER_FILE, new_v.get())
            self.popup("SUCCÈS", "Mot de passe maître modifié !", callback=self._show_main_screen)

        row = tk.Frame(self.main_frame, bg=BG)
        row.pack(pady=28)
        make_button(row, "[ MODIFIER ]", validate,             size=17).pack(side="left", padx=20)
        make_button(row, "← Retour",     self._show_main_screen, bg=BG, fg=ACCENT, size=15).pack(side="left", padx=20)

    # ── Générateur ───────────────────────────────────────────
    def _show_generator(self):
        self.clear()
        make_label(self.main_frame, "[ # ] GÉNÉRATEUR DE MOT DE PASSE",
                   size=28, bold=True, color=ACCENT).pack(pady=(45, 8))
        tk.Frame(self.main_frame, bg=ACCENT, height=1).pack(fill="x", padx=120, pady=(0, 18))

        length_v = tk.IntVar(value=20)
        make_label(self.main_frame, "Longueur :", size=15, color=DIM).pack(pady=(10, 4))
        tk.Scale(self.main_frame, from_=8, to=48, variable=length_v, orient="horizontal",
                 bg="#050f07", fg=ACCENT, troughcolor="#0a1a0e", highlightthickness=0,
                 length=560, font=(FONT, 12)).pack(pady=4)

        result_v = tk.StringVar()
        tk.Entry(self.main_frame, textvariable=result_v, font=(FONT, 20),
                 width=46, state="readonly", readonlybackground="#050f07",
                 fg=ACCENT, justify="center", relief="flat",
                 highlightthickness=1, highlightbackground=DIM).pack(pady=28)

        row = tk.Frame(self.main_frame, bg=BG)
        row.pack(pady=5)
        make_button(row, "[ GÉNÉRER ]", lambda: result_v.set(generate_password(length_v.get())), size=17).pack(side="left", padx=14)
        make_button(row, "📋 Copier",   lambda: self.copy(result_v.get()),                       size=17).pack(side="left", padx=14)
        make_button(row, "← Retour",   self._show_main_screen, bg=BG, fg=ACCENT, size=15).pack(side="left", padx=14)


# ============================================================
if __name__ == "__main__":
    CyberLock()