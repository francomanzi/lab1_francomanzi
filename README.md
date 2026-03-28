# lab1_francomanzi
Python application that calculates a student's final academic standing based on a pre-existing CSV file of course grades.

# Grade Evaluator — ALU Individual Coding Lab

**Course:** Introduction to Python Programming and Databases  
**Year:** BSE Year 1 | Trimester 2  

---

## Project Overview

This project contains two tools:

| File | Purpose |
|------|---------|
| `grade-evaluator.py` | Reads a `grades.csv` file and produces a full academic standing report |
| `organizer.sh` | Archives the current `grades.csv` with a timestamp and prepares a fresh one |
| `grades.csv` | Sample student grade data (included for testing) |

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.7 + | Uses only standard library (`csv`, `sys`, `os`) |
| Bash | 4.0 + | Available by default on Linux/macOS |

---

## 1 — Running the Grade Evaluator

```bash
python3 grade-evaluator.py
```

The script will prompt you for the CSV filename:

```
Enter the name of the CSV file to process (e.g., grades.csv): grades.csv
```

### Expected CSV format

```
assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20
```

**Rules enforced automatically:**

- Every `score` must be between **0 and 100** (inclusive).  
- `weight` column must total **100%** across all rows.  
- Formative weights must sum to exactly **60%**.  
- Summative weights must sum to exactly **40%**.

### Sample output (with the included grades.csv)

```
══════════════════════════════════════════════════════════════
   AFRICAN LEADERSHIP UNIVERSITY — GRADE EVALUATOR
══════════════════════════════════════════════════════════════
  Source file : grades.csv
  Assignments : 5

[1] Validating Scores …
    ✔  All scores are within the valid range (0–100).

[2] Validating Weights …
    ✔  Total weight     : 100%
    ✔  Formative weight : 60%
    ✔  Summative weight : 40%

[3] Assignment Breakdown
  Assignment                               Group         Score  Weight  Weighted
  ──────────────────────────────────────────────────────────────────────────────
  Quiz                                     Formative     85.0%   20.0%     17.00
  Group Exercise                           Formative     40.0%   20.0%      8.00
  Functions and Debugging Lab              Formative     45.0%   20.0%      9.00
  Midterm Project - Simple Calculator      Summative     70.0%   20.0%     14.00
  Final Project - Text-Based Game          Summative     60.0%   20.0%     12.00
  ──────────────────────────────────────────────────────────────────────────────
  TOTALS                                                          100%    60.00

[4] Category Summary
  Formative  score :  56.67%   (passing threshold: ≥ 50%)
  Summative  score :  65.00%   (passing threshold: ≥ 50%)
  Overall    grade :  60.00%
  GPA (0–5.0 scale):   3.00

══════════════════════════════════════════════════════════════
   FINAL DECISION
══════════════════════════════════════════════════════════════

  ✅  STATUS : PASSED

  📋 RESUBMISSION ELIGIBLE (failed formative, highest weight = 20.0%):
       • Group Exercise  (score: 40.0%,  weight: 20.0%)
       • Functions and Debugging Lab  (score: 45.0%,  weight: 20.0%)

══════════════════════════════════════════════════════════════
```

### Calculation walkthrough

| Assignment | Score | Weight | Contribution |
|---|---|---|---|
| Quiz | 85% | 20% | 17.00 |
| Group Exercise | 40% | 20% | 8.00 |
| Functions and Debugging Lab | 45% | 20% | 9.00 |
| Midterm Project | 70% | 20% | 14.00 |
| Final Project | 60% | 20% | 12.00 |
| **Total** | | **100%** | **60.00** |

- **Overall grade** = 60 / 100 = **60%**  
- **GPA** = (60 / 100) × 5.0 = **3.00**  
- **Formative average** = (85×20 + 40×20 + 45×20) / 60 = 3400/60 = **56.67%** → PASS ≥ 50%  
- **Summative average** = (70×20 + 60×20) / 40 = 2600/40 = **65.00%** → PASS ≥ 50%  
- **Final status** = **PASSED** (both categories cleared 50%)

### Resubmission logic

Both *Group Exercise* (40%) and *Functions and Debugging Lab* (45%) failed (scored below 50%)  
and share the **highest weight** among failed formatives (20% each), so **both** are flagged.

---

## 2 — Running the Organizer Script

```bash
chmod +x organizer.sh   # make executable (first run only)
./organizer.sh
```

### What it does, step by step

1. **Checks** that `grades.csv` exists; exits with an error if it does not.  
2. **Creates** an `archive/` directory if one does not already exist.  
3. **Generates** a timestamp in `YYYYMMDD-HHMMSS` format.  
4. **Moves** `grades.csv` → `archive/grades_<timestamp>.csv`.  
5. **Creates** a new empty `grades.csv` (with header) ready for the next batch.  
6. **Appends** a log entry to `organizer.log` (entries accumulate across runs).

### Sample output

```
[INFO]  Created directory: archive/
[INFO]  Archived 'grades.csv' → 'archive/grades_20251105-170000.csv'
[INFO]  Created fresh 'grades.csv' (ready for the next batch).
[INFO]  Logged operation to 'organizer.log'.

==============================================
  ARCHIVAL COMPLETE
==============================================
  Timestamp    : 20251105-170000
  Original file: grades.csv
  Archived to  : archive/grades_20251105-170000.csv
  Log file     : organizer.log
==============================================
```

### organizer.log format

Each line represents one archival run:

```
[20251105-170000]  original='grades.csv'  archived='archive/grades_20251105-170000.csv'
[20251106-083012]  original='grades.csv'  archived='archive/grades_20251106-083012.csv'
```

---

## Error Handling Reference

| Scenario | Behaviour |
|---|---|
| `grades.csv` not found | Clear error message + non-zero exit |
| CSV file completely empty | Error: "file appears to be completely empty" |
| CSV has header but no data rows | Error: "contains a header but no grade data" |
| Invalid score (< 0 or > 100) | Lists every offending row, then exits |
| Weight totals don't match rules | Lists every violated rule, then exits |
| `grades.csv` missing when running `organizer.sh` | Error message + exit (nothing is moved) |

---

## Repository Structure

```
lab_<github_username>/
├── grade-evaluator.py   # Python grade evaluation script
├── organizer.sh         # Bash archival script
├── grades.csv           # Sample grade data
└── README.md            # This file
```
