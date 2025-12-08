"""
EMOTIONAL TONE & STRESS ANALYZER
================================
A student wellness tracking application using Python, Tkinter, and SQLite.

HOW THIS CODE WORKS (For CBSE Viva):
------------------------------------
1. DATABASE (CRUD Operations):
   - CREATE: save_entry() - INSERT new mood entries into database
   - READ:   get_counts(), get_all(), get_today() - SELECT entries from database
   - UPDATE: Not used (entries are immutable once created)
   - DELETE: clear_all() - DELETE all entries from database

2. ANALYSIS:
   - analyze() function checks text for keywords from each emotion
   - Returns the emotion with most keyword matches and its stress score

3. UI (Tkinter):
   - App class creates the window with tabs for different features
   - Each render_*() method creates the content for that tab

TO MODIFY THIS CODE:
- To add a new emotion: Add to EMOTIONS list, COLORS dict, STRESS dict, and WORDS dict
- To change database: Edit db_exec() function (line 35-36)
- To change analysis: Edit analyze() function (line 55-57)
- To change UI: Edit render_*() methods (lines 80-110)
"""

import tkinter as tk
from tkinter import messagebox
import sqlite3, os
from datetime import datetime, date
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    CHARTS = True
except: CHARTS = False

# === CONFIGURATION (Easy to modify) ===
DB = os.path.join(os.path.dirname(__file__), "emotions.db")  # Database file location
REPORTS = os.path.join(os.path.dirname(__file__), "daily_reports")  # Reports folder

EMOTIONS = ["Energetic", "Motivated", "Neutral", "Tired", "Sad", "Angry", "Stressed", "Overwhelmed"]
COLORS = {"Energetic":"#FF6B6B", "Motivated":"#4ECDC4", "Neutral":"#95A5A6", "Tired":"#9B59B6", "Sad":"#3498DB", "Angry":"#E74C3C", "Stressed":"#F39C12", "Overwhelmed":"#E91E63"}
STRESS = {"Energetic":15, "Motivated":20, "Neutral":35, "Tired":55, "Sad":65, "Angry":70, "Stressed":80, "Overwhelmed":95}
WORDS = {"Energetic":["energetic","excited","pumped","awesome","amazing"], "Motivated":["motivated","focused","goal","succeed","study"], "Neutral":["okay","fine","normal","alright","meh"], "Tired":["tired","exhausted","sleepy","sleep","fatigue"], "Sad":["sad","unhappy","crying","lonely","miss"], "Angry":["angry","mad","furious","hate","annoyed"], "Stressed":["stressed","exam","deadline","pressure","worried"], "Overwhelmed":["overwhelmed","cant","panic","help","breaking"]}

# === DATABASE FUNCTIONS (CRUD Operations) ===
# This is the core database function - all queries go through here
# Uses PARAMETERIZED QUERIES with ? to prevent SQL injection attacks
def db_exec(query, params=(), fetch=False):
    conn = sqlite3.connect(DB)                    # Connect to SQLite database file
    result = conn.execute(query, params).fetchall() if fetch else conn.execute(query, params)
    conn.commit()                                  # Save changes
    conn.close()                                   # Close connection
    return result if fetch else None

# CREATE - Makes the table if it doesn't exist
def init_db(): 
    db_exec("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, emotion TEXT, stress INTEGER, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")

# CREATE - Inserts a new entry (parameterized query prevents SQL injection)
def save_entry(text, emotion, stress): 
    db_exec("INSERT INTO entries (text, emotion, stress) VALUES (?, ?, ?)", (text, emotion, stress))

# READ - Gets count of each emotion for the pie chart
def get_counts(): 
    return dict(db_exec("SELECT emotion, COUNT(*) FROM entries GROUP BY emotion", fetch=True))

# READ - Gets all entries (max 50) for reports
def get_all(): 
    return db_exec("SELECT * FROM entries ORDER BY ts DESC LIMIT 50", fetch=True)

# READ - Gets only today's entries
def get_today(): 
    return db_exec("SELECT * FROM entries WHERE DATE(ts) = ?", (date.today().strftime("%Y-%m-%d"),), fetch=True)

# DELETE - Removes all entries from the table
def clear_all(): 
    db_exec("DELETE FROM entries")

# === REPORT FUNCTION ===
def save_report():
    entries = get_today()
    if not entries: return None
    os.makedirs(REPORTS, exist_ok=True)
    emotions = [e[2] for e in entries]
    stresses = [e[3] for e in entries]
    report = f"EMOTIONAL TONE & STRESS ANALYZER - {date.today()}\n{'='*50}\nTotal: {len(entries)} | Avg: {sum(stresses)//len(stresses)}/100 | Dominant: {max(set(emotions), key=emotions.count)}\n\n"
    for i, e in enumerate(entries, 1): 
        report += f"{i}. [{e[4].split(' ')[1][:5] if ' ' in str(e[4]) else e[4]}] {e[2]} ({e[3]})\n"
    with open(os.path.join(REPORTS, f"report_{date.today()}.txt"), "w") as f: 
        f.write(report)
    return True

# === ANALYSIS FUNCTION ===
# Counts how many keywords from each emotion appear in the text
def analyze(text):
    lower = text.lower()
    scores = {emotion: sum(1 for word in WORDS[emotion] if word in lower) for emotion in EMOTIONS}
    best = max(scores, key=scores.get) if max(scores.values()) > 0 else "Neutral"
    return best, STRESS[best]

# === MAIN APPLICATION CLASS ===
class App:
    def __init__(self, root):
        self.root = root
        self.dark = False  # Theme toggle
        self.tab = 0       # Current tab (0=Quick, 1=Text, 2=Analytics, 3=Reports)
        self.root.title("Emotional Tone & Stress Analyzer")
        self.root.geometry("1050x720")
        init_db()
        self.build()

    # Theme colors - returns black/white color scheme based on mode
    def t(self): 
        if self.dark:
            return {"bg":"#0D1117","fg":"#E6EDF3","card":"#161B22","border":"#30363D","accent":"#FFFFFF","light":"#8B949E"}
        return {"bg":"#FFFFFF","fg":"#1A1A1A","card":"#F8F9FA","border":"#E8E8E8","accent":"#1A1A1A","light":"#6B7280"}

    # Helper to create consistent buttons
    def btn(self, parent, text, command, accent=False):
        c = self.t()
        return tk.Button(parent, text=text, font=("Segoe UI", 12, "bold" if accent else "normal"), bg=c["accent"] if accent else c["bg"], fg=c["bg"] if accent else c["light"], bd=0, relief=tk.FLAT, padx=24 if accent else 10, pady=10 if accent else 0, cursor="hand2", command=command)

    # Builds the entire UI
    def build(self):
        c = self.t()
        self.root.configure(bg=c["bg"])
        
        # Top banner
        tk.Frame(self.root, bg="#1A1A1A", height=32).pack(fill=tk.X)
        tk.Label(self.root, text="Track your emotional wellness →", font=("Segoe UI", 10), bg="#1A1A1A", fg="#9CA3AF").place(x=400, y=6)
        
        # Navigation bar
        nav = tk.Frame(self.root, bg=c["bg"], height=60)
        nav.pack(fill=tk.X, padx=50)
        nav.pack_propagate(False)
        tk.Label(nav, text="emotiontracker", font=("Segoe UI", 18, "bold"), bg=c["bg"], fg=c["fg"]).pack(side=tk.LEFT, pady=14)
        btns = tk.Frame(nav, bg=c["bg"])
        btns.pack(side=tk.RIGHT)
        self.btn(btns, "Save", self.save_r).pack(side=tk.LEFT, padx=12)
        self.btn(btns, "Clear", self.clear).pack(side=tk.LEFT, padx=12)
        tk.Button(btns, text="☀️" if self.dark else "🌙", font=("Segoe UI", 14), bg=c["bg"], fg=c["fg"], bd=0, cursor="hand2", command=self.toggle).pack(side=tk.LEFT, padx=8)
        
        tk.Frame(self.root, bg=c["border"], height=1).pack(fill=tk.X)
        
        # Hero section with large title
        hero = tk.Frame(self.root, bg=c["bg"])
        hero.pack(fill=tk.X, padx=50, pady=28)
        tk.Label(hero, text="Emotional\nwellness tracking.", font=("Georgia", 38), bg=c["bg"], fg=c["fg"], justify=tk.CENTER).pack()
        tk.Label(hero, text="Track your emotions. Understand your stress patterns.", font=("Segoe UI", 13), bg=c["bg"], fg=c["light"]).pack(pady=8)
        
        # Tab navigation
        tabs = tk.Frame(self.root, bg=c["bg"])
        tabs.pack(anchor="w", padx=50)
        for i, txt in enumerate(["Quick Entry", "Text Analysis", "Analytics", "Reports"]):
            lbl = tk.Label(tabs, text=txt, font=("Segoe UI", 12, "underline" if i==self.tab else "normal"), bg=c["bg"], fg=c["fg"] if i==self.tab else c["light"], cursor="hand2", padx=14)
            lbl.pack(side=tk.LEFT)
            lbl.bind("<Button-1>", lambda e, x=i: self.switch(x))
        
        tk.Frame(self.root, bg=c["border"], height=1).pack(fill=tk.X, padx=50, pady=(10,0))
        
        # Content area - changes based on selected tab
        self.cf = tk.Frame(self.root, bg=c["bg"])
        self.cf.pack(fill=tk.BOTH, expand=True, padx=50, pady=15)
        [self.render_quick, self.render_text, self.render_analytics, self.render_reports][self.tab]()

    def switch(self, i): 
        self.tab = i
        for w in self.root.winfo_children(): w.destroy()
        self.build()

    # TAB 1: Quick Entry with emotion buttons
    def render_quick(self):
        c = self.t()
        main = tk.Frame(self.cf, bg=c["card"], highlightbackground=c["border"], highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar with emotion buttons
        left = tk.Frame(main, bg=c["card"], width=150)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=18, pady=18)
        left.pack_propagate(False)
        tk.Label(left, text="Quick Entry", font=("Segoe UI", 11, "bold"), bg=c["card"], fg=c["light"]).pack(anchor="w", pady=(0,12))
        for e in EMOTIONS:
            tk.Button(left, text=f"● {e}", font=("Segoe UI", 11), bg=c["card"], fg=COLORS[e], bd=0, anchor="w", cursor="hand2", command=lambda x=e: self.quick(x)).pack(anchor="w", pady=3)
        
        tk.Frame(main, bg=c["border"], width=1).pack(side=tk.LEFT, fill=tk.Y, pady=18)
        
        # Center content area
        ct = tk.Frame(main, bg=c["bg"])
        ct.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=25, pady=18)
        tk.Label(ct, text="How are you feeling?", font=("Segoe UI", 16, "bold"), bg=c["bg"], fg=c["fg"]).pack(anchor="w")
        tk.Label(ct, text="Type your thoughts below", font=("Segoe UI", 11), bg=c["bg"], fg=c["light"]).pack(anchor="w", pady=(4,14))
        self.txt = tk.Text(ct, height=4, font=("Segoe UI", 12), bg=c["card"], fg=c["fg"], relief=tk.FLAT, highlightthickness=1, highlightbackground=c["border"], padx=12, pady=12)
        self.txt.pack(fill=tk.X)
        self.btn(ct, "Analyze", self.analyze_q, True).pack(anchor="w", pady=15)
        self.res = tk.Frame(ct, bg=c["bg"])
        self.res.pack(fill=tk.X)
        
        tk.Frame(main, bg=c["border"], width=1).pack(side=tk.LEFT, fill=tk.Y, pady=18)
        
        # Right panel with pie chart
        right = tk.Frame(main, bg=c["card"], width=240)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=18, pady=18)
        right.pack_propagate(False)
        tk.Label(right, text="Distribution", font=("Segoe UI", 12, "bold"), bg=c["card"], fg=c["fg"]).pack(anchor="w")
        self.chart = tk.Frame(right, bg=c["card"])
        self.chart.pack(fill=tk.BOTH, expand=True, pady=10)
        self.update_chart()

    # TAB 2: Text Analysis
    def render_text(self):
        c = self.t()
        main = tk.Frame(self.cf, bg=c["card"], highlightbackground=c["border"], highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True, padx=80, pady=25)
        tk.Label(main, text="Text Analysis", font=("Segoe UI", 18, "bold"), bg=c["card"], fg=c["fg"]).pack(pady=20)
        tk.Label(main, text="Enter detailed text for emotion analysis", font=("Segoe UI", 11), bg=c["card"], fg=c["light"]).pack()
        self.txt2 = tk.Text(main, height=6, font=("Segoe UI", 12), bg=c["bg"], fg=c["fg"], relief=tk.FLAT, highlightthickness=1, highlightbackground=c["border"], padx=15, pady=15, wrap=tk.WORD)
        self.txt2.pack(fill=tk.X, padx=35, pady=20)
        self.btn(main, "Analyze Text", self.analyze_t, True).pack(pady=(0,25))
        self.res2 = tk.Frame(main, bg=c["card"])
        self.res2.pack(fill=tk.X, padx=35, pady=(0,25))

    # TAB 3: Analytics with bar chart
    def render_analytics(self):
        c = self.t()
        main = tk.Frame(self.cf, bg=c["card"], highlightbackground=c["border"], highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True)
        tk.Label(main, text="Analytics", font=("Segoe UI", 18, "bold"), bg=c["card"], fg=c["fg"]).pack(pady=20)
        cf = tk.Frame(main, bg=c["card"])
        cf.pack(fill=tk.BOTH, expand=True, padx=35, pady=18)
        data = get_counts()
        if not data or not CHARTS:
            return tk.Label(cf, text="No data" if not data else "Install matplotlib", font=("Segoe UI", 12), bg=c["card"], fg=c["light"]).pack(pady=100)
        fig, ax = plt.subplots(figsize=(8, 5), facecolor=c["card"])
        ax.bar(data.keys(), data.values(), color=[COLORS[e] for e in data.keys()])
        ax.set_ylabel("Count", color=c["fg"], fontsize=12)
        ax.set_facecolor(c["card"])
        ax.tick_params(colors=c["fg"], labelsize=10)
        for s in ax.spines.values(): s.set_color(c["border"])
        FigureCanvasTkAgg(fig, cf).get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    # TAB 4: Reports
    def render_reports(self):
        c = self.t()
        main = tk.Frame(self.cf, bg=c["card"], highlightbackground=c["border"], highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True, padx=80, pady=25)
        tk.Label(main, text="Reports", font=("Segoe UI", 18, "bold"), bg=c["card"], fg=c["fg"]).pack(pady=20)
        self.btn(main, "Generate Today's Report", self.save_r, True).pack(pady=18)
        entries = get_all()
        tk.Label(main, text=f"Total Entries: {len(entries)}", font=("Segoe UI", 12), bg=c["card"], fg=c["light"]).pack(pady=10)
        lf = tk.Frame(main, bg=c["bg"])
        lf.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10,25))
        for e in entries[:10]:
            tk.Label(lf, text=f"● {e[2]} - {str(e[4]).split(' ')[0]} - Stress: {e[3]}", font=("Segoe UI", 11), bg=c["bg"], fg=c["fg"], anchor="w").pack(fill=tk.X, pady=3)

    # === ACTION METHODS ===
    def quick(self, e): 
        save_entry(f"[Quick: {e}]", e, STRESS[e])
        self.show(e, STRESS[e])
        self.update_chart()

    def analyze_q(self):
        text = self.txt.get("1.0", tk.END).strip()
        if text:
            e, s = analyze(text)
            save_entry(text, e, s)
            self.txt.delete("1.0", tk.END)
            self.show(e, s)
            self.update_chart()

    def analyze_t(self):
        text = self.txt2.get("1.0", tk.END).strip()
        c = self.t()
        if text:
            e, s = analyze(text)
            save_entry(text, e, s)
            self.txt2.delete("1.0", tk.END)
            for w in self.res2.winfo_children(): w.destroy()
            tk.Label(self.res2, text=f"Emotion: {e}", font=("Segoe UI", 16, "bold"), bg=c["card"], fg=COLORS[e]).pack(anchor="w")
            tk.Label(self.res2, text=f"Stress: {s}/100", font=("Segoe UI", 12), bg=c["card"], fg=c["fg"]).pack(anchor="w")

    def show(self, e, s):
        c = self.t()
        for w in self.res.winfo_children(): w.destroy()
        tk.Label(self.res, text=f"● {e}", font=("Segoe UI", 20, "bold"), bg=c["bg"], fg=COLORS[e]).pack(anchor="w", pady=(10,4))
        color = "#22C55E" if s < 40 else "#EAB308" if s < 70 else "#EF4444"
        tk.Label(self.res, text=f"Stress: {s}/100", font=("Segoe UI", 13), bg=c["bg"], fg=color).pack(anchor="w")

    def update_chart(self):
        for w in self.chart.winfo_children(): w.destroy()
        c = self.t()
        data = get_counts()
        if not CHARTS or not data:
            return tk.Label(self.chart, text="No data" if not data else "pip install matplotlib", font=("Segoe UI", 10), bg=c["card"], fg=c["light"]).pack(pady=50)
        fig, ax = plt.subplots(figsize=(2.4, 2.4), facecolor=c["card"])
        ax.pie(data.values(), labels=data.keys(), colors=[COLORS[e] for e in data.keys()], autopct='%1.0f%%', textprops={'fontsize':8, 'color':c["fg"]})
        ax.set_facecolor(c["card"])
        FigureCanvasTkAgg(fig, self.chart).get_tk_widget().pack()
        plt.close(fig)

    def save_r(self): 
        messagebox.showinfo("Report", "Saved to daily_reports folder!" if save_report() else "No entries today")
    
    def clear(self):
        if messagebox.askyesno("Clear", "Delete all data?"):
            clear_all()
            self.switch(self.tab)
    
    def toggle(self): 
        self.dark = not self.dark
        self.switch(self.tab)

# === RUN THE APP ===
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
