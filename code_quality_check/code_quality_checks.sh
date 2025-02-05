#!/bin/bash

# Set default values if environment variables are not set
CODE_PATH="${CODE_PATH:-.}"
REPORT_PATH="${REPORT_PATH:-bandit_report.html}"
CHECK_CONFIG="${CHECK_CONFIG:-./code_quality_check/check_quality_config.yaml}"

# Run Bandit with high severity issues only and save the output as an HTML report
bandit -c "$CHECK_CONFIG" -r "$CODE_PATH" --severity-level high -f html -o "$REPORT_PATH"
RESULT=$?

# Check if the Bandit run was successful
if [ $RESULT -eq 0 ]; then
  echo "Bandit check completed successfully. Report saved to $REPORT_PATH."
else
  echo "Bandit check found high-severity issues. Report saved to $REPORT_PATH."
  exit 1
fi
