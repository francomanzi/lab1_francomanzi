"""
grade-evaluator.py
African Leadership University — Intro to Python Programming & Databases
Individual Coding Lab | BSE Year 1 Trimester 2

Calculates a student's final academic standing from a grades CSV file.
Features:
  - Grade & weight validation
  - Weighted GPA calculation (0–5.0 scale)
  - Separate Formative / Summative pass/fail check (>= 50% each)
  - Resubmission recommendation for failed formative assignments
"""

import csv
import sys
import os


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
FORMATIVE_WEIGHT_TARGET  = 60   # Formative assignments must total 60%
SUMMATIVE_WEIGHT_TARGET  = 40   # Summative assignments must total 40%
TOTAL_WEIGHT_TARGET      = 100  # All weights combined must equal 100
PASSING_THRESHOLD        = 50   # Minimum % required in each category
GPA_SCALE                = 5.0  # Institutional GPA scale


# ─────────────────────────────────────────────
# 1. DATA LOADING
# ─────────────────────────────────────────────
def load_csv_data():
    """
    Prompts the user for a CSV filename, verifies it exists,
    and parses every row into a list of dictionaries with
    properly typed numeric fields.

    Returns:
        list[dict]: One dict per assignment with keys:
                    'assignment', 'group', 'score', 'weight'

    Exits with an error message if:
        - The file is not found
        - The file is empty / has no data rows
        - A numeric field cannot be converted
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    # ── File existence check ──────────────────
    if not os.path.exists(filename):
        print(f"\n[ERROR] The file '{filename}' was not found.")
        print("  → Make sure the file is in the current directory and try again.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # ── Empty-file guard ──────────────
            if reader.fieldnames is None:
                print(f"\n[ERROR] '{filename}' appears to be completely empty.")
                print("  → Please provide a file with a header row and at least one data row.")
                sys.exit(1)

            for row_num, row in enumerate(reader, start=2):   # row 1 = header
                try:
                    assignments.append({
                        'assignment': row['assignment'].strip(),
                        'group':      row['group'].strip(),
                        'score':      float(row['score']),
                        'weight':     float(row['weight'])
                    })
                except (ValueError, KeyError) as field_err:
                    print(f"\n[ERROR] Bad data on row {row_num}: {field_err}")
                    print(f"  → Row content: {dict(row)}")
                    sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] Could not read '{filename}': {e}")
        sys.exit(1)

    # ── No data rows at all ───────────────────
    if not assignments:
        print(f"\n[ERROR] '{filename}' contains a header but no grade data.")
        print("  → Add assignment rows and run the program again.")
        sys.exit(1)

    return assignments, filename


# ─────────────────────────────────────────────
# 2. VALIDATION HELPERS
# ─────────────────────────────────────────────
def validate_scores(data):
    """
    Checks that every assignment score is in the range [0, 100].

    Args:
        data (list[dict]): Parsed assignment records.

    Returns:
        bool: True if all scores are valid, False otherwise
              (prints each violation found).
    """
    valid = True
    for entry in data:
        score = entry['score']
        if not (0 <= score <= 100):
            print(f"  [SCORE ERROR] '{entry['assignment']}' has an invalid score: {score}")
            print(f"                Scores must be between 0 and 100.")
            valid = False
    return valid


def validate_weights(data):
    """
    Verifies the three weight rules:
        1. Total of all weights  == 100
        2. Formative weights sum == 60
        3. Summative weights sum == 40

    Args:
        data (list[dict]): Parsed assignment records.

    Returns:
        bool: True if all three rules pass, False otherwise.
    """
    total_weight      = sum(e['weight'] for e in data)
    formative_weight  = sum(e['weight'] for e in data if e['group'].lower() == 'formative')
    summative_weight  = sum(e['weight'] for e in data if e['group'].lower() == 'summative')

    valid = True

    if total_weight != TOTAL_WEIGHT_TARGET:
        print(f"  [WEIGHT ERROR] Total weight is {total_weight}% (must be exactly {TOTAL_WEIGHT_TARGET}%).")
        valid = False

    if formative_weight != FORMATIVE_WEIGHT_TARGET:
        print(f"  [WEIGHT ERROR] Formative weight is {formative_weight}% (must be exactly {FORMATIVE_WEIGHT_TARGET}%).")
        valid = False

    if summative_weight != SUMMATIVE_WEIGHT_TARGET:
        print(f"  [WEIGHT ERROR] Summative weight is {summative_weight}% (must be exactly {SUMMATIVE_WEIGHT_TARGET}%).")
        valid = False

    return valid


# ─────────────────────────────────────────────
# 3. CORE EVALUATION
# ─────────────────────────────────────────────
def evaluate_grades(data, filename):
    """
    Full grade evaluation pipeline:
        a) Score range validation
        b) Weight distribution validation
        c) Weighted-average calculation per category
        d) GPA calculation
        e) Pass / Fail determination (both categories must reach 50%)
        f) Resubmission recommendation

    Args:
        data     (list[dict]): Parsed and type-cast assignment records.
        filename (str):        Source filename (for display purposes).
    """

    # ── Pretty header ─────────────────────────
    print("\n" + "═" * 60)
    print("   AFRICAN LEADERSHIP UNIVERSITY — GRADE EVALUATOR")
    print("═" * 60)
    print(f"  Source file : {filename}")
    print(f"  Assignments : {len(data)}")
    print("─" * 60)

    # ── a) Score validation ───────────────────
    print("\n[1] Validating Scores …")
    scores_ok = validate_scores(data)
    if scores_ok:
        print("    ✔  All scores are within the valid range (0–100).")
    else:
        print("\n    Fix the scores above and re-run the program.")
        sys.exit(1)

    # ── b) Weight validation ──────────────────
    print("\n[2] Validating Weights …")
    weights_ok = validate_weights(data)
    if weights_ok:
        print(f"    ✔  Total weight     : 100%  (required: {TOTAL_WEIGHT_TARGET}%)")
        print(f"    ✔  Formative weight : {sum(e['weight'] for e in data if e['group'].lower()=='formative')}%"
              f"   (required: {FORMATIVE_WEIGHT_TARGET}%)")
        print(f"    ✔  Summative weight : {sum(e['weight'] for e in data if e['group'].lower()=='summative')}%"
              f"   (required: {SUMMATIVE_WEIGHT_TARGET}%)")
    else:
        print("\n    Fix the weights above and re-run the program.")
        sys.exit(1)

    # ── c) Weighted averages per category ─────
    #
    # Formula:  category_score = Σ(score_i × weight_i) / Σ(weight_i)
    # This gives a percentage score within that category.
    #
    formative_entries  = [e for e in data if e['group'].lower() == 'formative']
    summative_entries  = [e for e in data if e['group'].lower() == 'summative']

    formative_weighted_sum  = sum(e['score'] * e['weight'] for e in formative_entries)
    summative_weighted_sum  = sum(e['score'] * e['weight'] for e in summative_entries)

    formative_total_weight  = sum(e['weight'] for e in formative_entries)
    summative_total_weight  = sum(e['weight'] for e in summative_entries)

    formative_avg   = formative_weighted_sum  / formative_total_weight   # % within category
    summative_avg   = summative_weighted_sum  / summative_total_weight   # % within category

    # Overall grade = sum of all (score × weight) / 100
    overall_grade   = sum(e['score'] * e['weight'] for e in data) / TOTAL_WEIGHT_TARGET

    # GPA on a 5.0 scale
    gpa             = (overall_grade / 100) * GPA_SCALE

    # ── d) Assignment breakdown table ─────────
    print("\n[3] Assignment Breakdown")
    print(f"  {'Assignment':<40} {'Group':<12} {'Score':>6} {'Weight':>7} {'Weighted':>9}")
    print("  " + "─" * 76)
    for e in data:
        weighted_contribution = e['score'] * e['weight'] / 100
        print(f"  {e['assignment']:<40} {e['group']:<12} {e['score']:>5.1f}%"
              f" {e['weight']:>6.1f}%  {weighted_contribution:>8.2f}")
    print("  " + "─" * 76)
    print(f"  {'TOTALS':<40} {'':12} {'':>6} {'100%':>7} {overall_grade:>8.2f}")

    # ── e) Category summary ───────────────────
    print("\n[4] Category Summary")
    print(f"  Formative  score : {formative_avg:>6.2f}%   (passing threshold: ≥ {PASSING_THRESHOLD}%)")
    print(f"  Summative  score : {summative_avg:>6.2f}%   (passing threshold: ≥ {PASSING_THRESHOLD}%)")
    print(f"  Overall    grade : {overall_grade:>6.2f}%")
    print(f"  GPA (0–5.0 scale): {gpa:>6.2f}")

    # ── e) Pass / Fail logic ──────────────────
    formative_pass  = formative_avg  >= PASSING_THRESHOLD
    summative_pass  = summative_avg  >= PASSING_THRESHOLD
    overall_pass    = formative_pass and summative_pass

    # ── f) Resubmission recommendation ────────
    # Identify formative assignments scored below the passing threshold.
    failed_formative = [e for e in formative_entries if e['score'] < PASSING_THRESHOLD]

    resubmission_candidates = []
    if failed_formative:
        max_weight = max(e['weight'] for e in failed_formative)
        # All failed formatives that share that highest weight are candidates.
        resubmission_candidates = [e for e in failed_formative if e['weight'] == max_weight]

    # ── Final output ──────────────────────────
    print("\n" + "═" * 60)
    print("   FINAL DECISION")
    print("═" * 60)

    if overall_pass:
        print("\n  ✅  STATUS : PASSED")
    else:
        print("\n  ❌  STATUS : FAILED")
        reasons = []
        if not formative_pass:
            reasons.append(f"Formative score {formative_avg:.2f}% < {PASSING_THRESHOLD}%")
        if not summative_pass:
            reasons.append(f"Summative score {summative_avg:.2f}% < {PASSING_THRESHOLD}%")
        print(f"      Reason : {' | '.join(reasons)}")

    # ── Resubmission block ────────────────────
    print()
    if resubmission_candidates:
        print(f"  📋 RESUBMISSION ELIGIBLE (failed formative, highest weight = {max_weight}%):")
        for candidate in resubmission_candidates:
            print(f"       • {candidate['assignment']}"
                  f"  (score: {candidate['score']}%,  weight: {candidate['weight']}%)")
    else:
        print("  📋 RESUBMISSION : No failed formative assignments — none required.")

    print("\n" + "═" * 60 + "\n")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Step 1: Load and parse the CSV
    course_data, source_file = load_csv_data()

    # Step 2: Run the full evaluation pipeline
    evaluate_grades(course_data, source_file)
