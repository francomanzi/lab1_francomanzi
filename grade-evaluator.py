import csv
import sys
import os

FORMATIVE_WEIGHT_TARGET  = 60
SUMMATIVE_WEIGHT_TARGET  = 40
TOTAL_WEIGHT_TARGET      = 100
PASSING_THRESHOLD        = 50
GPA_SCALE                = 5.0

def load_csv_data():
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()
    if not os.path.exists(filename):
        print(f"\n[ERROR] The file '{filename}' was not found.")
        sys.exit(1)
    assignments = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                print(f"\n[ERROR] '{filename}' appears to be completely empty.")
                sys.exit(1)
            for row_num, row in enumerate(reader, start=2):
                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group':      row['group'].strip(),
                    'score':      float(row['score']),
                    'weight':     float(row['weight'])
                })
    except Exception as e:
        print(f"\n[ERROR] Could not read '{filename}': {e}")
        sys.exit(1)
    if not assignments:
        print(f"\n[ERROR] '{filename}' contains a header but no grade data.")
        sys.exit(1)
    return assignments, filename

def validate_scores(data):
    valid = True
    for entry in data:
        if not (0 <= entry['score'] <= 100):
            print(f"  [SCORE ERROR] '{entry['assignment']}' has invalid score: {entry['score']}")
            valid = False
    return valid

def validate_weights(data):
    total     = sum(e['weight'] for e in data)
    formative = sum(e['weight'] for e in data if e['group'].lower() == 'formative')
    summative = sum(e['weight'] for e in data if e['group'].lower() == 'summative')
    valid = True
    if total != TOTAL_WEIGHT_TARGET:
        print(f"  [WEIGHT ERROR] Total weight is {total}% (must be {TOTAL_WEIGHT_TARGET}%).")
        valid = False
    if formative != FORMATIVE_WEIGHT_TARGET:
        print(f"  [WEIGHT ERROR] Formative weight is {formative}% (must be {FORMATIVE_WEIGHT_TARGET}%).")
        valid = False
    if summative != SUMMATIVE_WEIGHT_TARGET:
        print(f"  [WEIGHT ERROR] Summative weight is {summative}% (must be {SUMMATIVE_WEIGHT_TARGET}%).")
        valid = False
    return valid

def evaluate_grades(data, filename):
    print("\n" + "="*60)
    print("   AFRICAN LEADERSHIP UNIVERSITY - GRADE EVALUATOR")
    print("="*60)
    print(f"  Source file : {filename}")
    print(f"  Assignments : {len(data)}")
    print("-"*60)

    print("\n[1] Validating Scores ...")
    if not validate_scores(data):
        sys.exit(1)
    print("    OK  All scores are within the valid range (0-100).")

    print("\n[2] Validating Weights ...")
    if not validate_weights(data):
        sys.exit(1)
    print("    OK  All weights are correct (Total=100, Formative=60, Summative=40).")

    formative = [e for e in data if e['group'].lower() == 'formative']
    summative = [e for e in data if e['group'].lower() == 'summative']

    formative_avg = sum(e['score'] * e['weight'] for e in formative) / sum(e['weight'] for e in formative)
    summative_avg = sum(e['score'] * e['weight'] for e in summative) / sum(e['weight'] for e in summative)
    overall_grade = sum(e['score'] * e['weight'] for e in data) / TOTAL_WEIGHT_TARGET
    gpa           = (overall_grade / 100) * GPA_SCALE

    print("\n[3] Assignment Breakdown")
    print(f"  {'Assignment':<40} {'Group':<12} {'Score':>6} {'Weight':>7} {'Weighted':>9}")
    print("  " + "-"*76)
    for e in data:
        print(f"  {e['assignment']:<40} {e['group']:<12} {e['score']:>5.1f}% {e['weight']:>6.1f}%  {e['score']*e['weight']/100:>8.2f}")
    print("  " + "-"*76)
    print(f"  {'TOTALS':<40} {'':12} {'':>6} {'100%':>7} {overall_grade:>8.2f}")

    print("\n[4] Category Summary")
    print(f"  Formative  score : {formative_avg:>6.2f}%   (need >= {PASSING_THRESHOLD}%)")
    print(f"  Summative  score : {summative_avg:>6.2f}%   (need >= {PASSING_THRESHOLD}%)")
    print(f"  Overall    grade : {overall_grade:>6.2f}%")
    print(f"  GPA (0-5.0 scale): {gpa:>6.2f}")

    passed = formative_avg >= PASSING_THRESHOLD and summative_avg >= PASSING_THRESHOLD

    print("\n" + "="*60)
    print("   FINAL DECISION")
    print("="*60)
    if passed:
        print("\n  STATUS : PASSED")
    else:
        print("\n  STATUS : FAILED")
        if formative_avg < PASSING_THRESHOLD:
            print(f"  Reason : Formative score {formative_avg:.2f}% is below {PASSING_THRESHOLD}%")
        if summative_avg < PASSING_THRESHOLD:
            print(f"  Reason : Summative score {summative_avg:.2f}% is below {PASSING_THRESHOLD}%")

    failed_formative = [e for e in formative if e['score'] < PASSING_THRESHOLD]
    print()
    if failed_formative:
        max_w = max(e['weight'] for e in failed_formative)
        candidates = [e for e in failed_formative if e['weight'] == max_w]
        print(f"  RESUBMISSION ELIGIBLE (highest weight among failed = {max_w}%):")
        for c in candidates:
            print(f"    - {c['assignment']}  (score: {c['score']}%, weight: {c['weight']}%)")
    else:
        print("  RESUBMISSION : None required.")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    course_data, source_file = load_csv_data()
    evaluate_grades(course_data, source_file)
