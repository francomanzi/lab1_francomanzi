#!/usr/bin/env bash
# =============================================================================
# organizer.sh
# African Leadership University — Intro to Python Programming & Databases
# Individual Coding Lab | BSE Year 1 Trimester 2
#
# Purpose:
#   Archives the current grades.csv file with a timestamp, moves it to an
#   'archive/' directory, creates a fresh empty grades.csv, and logs each
#   operation to organizer.log.
#
# Usage:
#   chmod +x organizer.sh   # (first run only)
#   ./organizer.sh
# =============================================================================

set -euo pipefail   # Exit on error, treat unset vars as errors, propagate pipe failures

# ── Configuration ─────────────────────────────────────────────────────────────
SOURCE_FILE="grades.csv"          # The file to archive
ARCHIVE_DIR="archive"             # Destination directory for archived files
LOG_FILE="organizer.log"          # Cumulative log of every archival run

# ── 1. Verify the source file exists ──────────────────────────────────────────
if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "[ERROR] '$SOURCE_FILE' not found in the current directory."
    echo "        Nothing to archive. Exiting."
    exit 1
fi

# ── 2. Create the archive directory if it does not already exist ───────────────
if [[ ! -d "$ARCHIVE_DIR" ]]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "[INFO]  Created directory: $ARCHIVE_DIR/"
else
    echo "[INFO]  Archive directory already exists: $ARCHIVE_DIR/"
fi

# ── 3. Generate a timestamp (format: YYYYMMDD-HHMMSS) ─────────────────────────
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# ── 4. Build the new archived filename ────────────────────────────────────────
#   Strip the .csv extension, append the timestamp, then re-add the extension.
BASE_NAME="${SOURCE_FILE%.csv}"                           # → grades
ARCHIVED_NAME="${BASE_NAME}_${TIMESTAMP}.csv"             # → grades_20251105-170000.csv
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"           # → archive/grades_20251105-170000.csv

# ── 5. Move (rename + relocate) the source file to the archive ────────────────
mv "$SOURCE_FILE" "$ARCHIVED_PATH"
echo "[INFO]  Archived '$SOURCE_FILE' → '$ARCHIVED_PATH'"

# ── 6. Create a fresh, empty grades.csv (header only) for the next batch ──────
#   Writing the header row makes the file immediately usable.
echo "assignment,group,score,weight" > "$SOURCE_FILE"
echo "[INFO]  Created fresh '$SOURCE_FILE' (ready for the next batch)."

# ── 7. Log this operation to organizer.log ────────────────────────────────────
#   Each log entry is a single line: timestamp | original file | archived file
LOG_ENTRY="[${TIMESTAMP}]  original='${SOURCE_FILE}'  archived='${ARCHIVED_PATH}'"
echo "$LOG_ENTRY" >> "$LOG_FILE"
echo "[INFO]  Logged operation to '$LOG_FILE'."

# ── 8. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo "  ARCHIVAL COMPLETE"
echo "=============================================="
echo "  Timestamp    : $TIMESTAMP"
echo "  Original file: $SOURCE_FILE"
echo "  Archived to  : $ARCHIVED_PATH"
echo "  Log file     : $LOG_FILE"
echo "=============================================="
