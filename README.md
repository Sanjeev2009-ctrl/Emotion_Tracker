# 🎯 Emotional Tone & Stress Analyzer - Simplified Version

A clean, minimal student wellness app for CBSE Class 12 CS Project.

---

## 📁 Project Structure

```
emostress_simple/
│
├── 📄 main.py                          ~220 lines | Complete Application
├── 💾 emotions.db                      Auto-created | SQLite Database  
├── 📋 README.md                        This file | Setup Instructions
│
└── 📂 daily_reports/                   Auto-created | Report Storage
    ├── emotion_report_2024-12-08.txt  Today's report
    ├── emotion_report_2024-12-09.txt  Tomorrow's report
    └── emotion_report_2024-12-10.txt  And so on...
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 **8 Emotions** | Energetic, Motivated, Neutral, Tired, Sad, Angry, Stressed, Overwhelmed |
| 📊 **Pie Chart** | Real-time emotion distribution visualization |
| 💡 **Smart Analysis** | Keyword-based text analysis for mood detection |
| 🌓 **Theme Toggle** | Switch between Light and Dark modes |
| 💾 **SQLite DB** | Local storage with parameterized queries |
| 📄 **Daily Reports** | Beautiful formatted .txt reports |
| 🗑️ **Clear Data** | One-click database reset |

---

## 🚀 Quick Start

### Installation

```bash
# Install matplotlib (for charts)
pip install matplotlib

# Run the application
python main.py
```

### First Run
The app automatically creates:
- `emotions.db` - Your mood database
- `daily_reports/` - Folder for saving reports

---

## 📖 How to Use

### 1️⃣ Quick-Tap Entry
Click any of the **8 colorful emotion buttons** to log instantly.

### 2️⃣ Text Entry
Type how you're feeling in the text box and click **"Analyze My Mood"**.

### 3️⃣ Save Report
Click **"📄 Save Report"** to export today's emotions to a formatted text file.

### 4️⃣ Clear Data
Click **"🗑️ Clear Data"** to reset the database (asks for confirmation).

### 5️⃣ View Chart
The **pie chart** on the right updates automatically showing your emotion distribution.

---

## 🎓 CBSE Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| **Python Functions** | `analyze_text()`, `save_entry()`, `get_entries()` |
| **Classes & Objects** | `EmotionApp` class with methods |
| **SQLite Database** | CREATE TABLE, INSERT, SELECT with parameterized queries |
| **SQL Injection Prevention** | Using `?` placeholders in queries |
| **File Handling** | Writing formatted reports to `.txt` files |
| **Tkinter GUI** | Frames, Buttons, Labels, Text widgets |
| **Data Visualization** | Matplotlib pie charts |
| **Date/Time Handling** | `datetime` module for timestamps |

---

## 📝 Database Schema

```sql
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    emotion TEXT,
    stress INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Sample Data
| id | text | emotion | stress | timestamp |
|----|------|---------|--------|-----------|
| 1 | "I have exams tomorrow!" | Stressed | 80 | 2024-12-08 14:30:00 |
| 2 | "[Quick: Motivated]" | Motivated | 20 | 2024-12-08 15:45:00 |

---

## 🎨 UI Design

- **Header**: App title + Action buttons (Save Report, Clear Data, Theme Toggle)
- **Left Panel**: Emotion buttons grid + Text input + Result display
- **Right Panel**: Live-updating pie chart
- **Status Bar**: Shows database and report folder locations
- **Theme**: Dark mode (default) with Light mode option

---

## 📊 Sample Daily Report

```
╔══════════════════════════════════════════════════════════╗
║        EMOTIONAL TONE & STRESS ANALYZER                 ║
║              Daily Report - 2024-12-08                  ║
╚══════════════════════════════════════════════════════════╝

📊 SUMMARY
────────────────────────────────────────────────────────────
  Total Entries      : 8
  Average Stress     : 45/100
  Dominant Emotion   : Motivated

📝 TODAY'S ENTRIES
────────────────────────────────────────────────────────────
  1. [09:30] Energetic (Stress: 15)
  2. [12:00] Motivated (Stress: 20)
  3. [15:30] Stressed (Stress: 80)
     "Exam tomorrow and I haven't studied!"

📈 EMOTION BREAKDOWN
────────────────────────────────────────────────────────────
  Motivated    ████░░░░░░ 4
  Stressed     ███░░░░░░░ 3
  Neutral      █░░░░░░░░░ 1
```

---

## 🎯 For CBSE Viva

### Questions You Can Answer:

**Q: How does the keyword matching work?**
> We use a dictionary of keywords for each emotion. The `analyze_text()` function splits the input text, converts to lowercase, and counts matches for each emotion. The emotion with the most matches wins.

**Q: How do you prevent SQL injection?**
> We use parameterized queries with `?` placeholders. For example: `cursor.execute("INSERT INTO entries VALUES (?, ?, ?)", (text, emotion, stress))`. This prevents malicious SQL from being executed.

**Q: What is the purpose of `init_db()`?**
> It creates the database and table if they don't exist. Uses `CREATE TABLE IF NOT EXISTS` to avoid errors on subsequent runs.

**Q: How does the pie chart update?**
> The `update_chart()` method queries the database for emotion counts, creates a matplotlib pie chart, and embeds it in the Tkinter frame using `FigureCanvasTkAgg`.

---

## 🔧 Troubleshooting

**No charts showing?**
```bash
pip install matplotlib
```

**Database locked error?**
- Close the app completely and restart
- Check if `emotions.db` exists and is not corrupted

**Want to start fresh?**
- Click the "🗑️ Clear Data" button
- Or manually delete `emotions.db`

---

## 📦 What Gets Created

### On First Run:
- `emotions.db` (0 KB initially, grows with entries)
- `daily_reports/` folder

### When You Click "Save Report":
- `daily_reports/emotion_report_YYYY-MM-DD.txt`

### Auto-backup:
- Simply copy the entire `emostress_simple/` folder!

---

## 🎓 Credits

**Project**: Emotional Tone & Stress Analyzer  
**Purpose**: CBSE Class 12 Computer Science Practical  
**Concepts**: Python, SQLite, Tkinter, Data Visualization  
**Lines of Code**: ~220 (all explained and understandable!)  

---

## 📄 License

This is an educational project for CBSE Class 12 Computer Science.  
Feel free to modify and enhance!

---

**Built with ❤️ using Python, Tkinter, SQLite, and Matplotlib**
