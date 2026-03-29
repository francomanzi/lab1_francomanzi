#!/usr/bin/env bash

SOURCE_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "[ERROR] '$SOURCE_FILE' not found. Nothing to archive."
    exit 1
fi

if [[ ! -d "$ARCHIVE_DIR" ]]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "[INFO]  Created directory: $ARCHIVE_DIR/"
else
    echo "[INFO]  Archive directory already exists: $ARCHIVE_DIR/"
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

mv "$SOURCE_FILE" "$ARCHIVED_PATH"
echo "[INFO]  Archived '$SOURCE_FILE' → '$ARCHIVED_PATH'"

echo "assignment,group,score,weight" > "$SOURCE_FILE"
echo "[INFO]  Created fresh '$SOURCE_FILE' (ready for the next batch)."

echo "[${TIMESTAMP}]  original='${SOURCE_FILE}'  archived='${ARCHIVED_PATH}'" >> "$LOG_FILE"
echo "[INFO]  Logged operation to '$LOG_FILE'."

echo ""
echo "=============================================="
echo "  ARCHIVAL COMPLETE"
echo "=============================================="
echo "  Timestamp    : $TIMESTAMP"
echo "  Original file: $SOURCE_FILE"
echo "  Archived to  : $ARCHIVED_PATH"
echo "  Log file     : $LOG_FILE"
echo "=============================================="
