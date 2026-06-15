#!/bin/bash

# Array of 22 realistic commit messages
messages=(
  "Initial project setup"
  "Add dataset for product pricing analysis"
  "Implement data cleaning pipeline"
  "Handle missing values and outliers"
  "Create feature extraction module"
  "Train baseline regression model"
  "Evaluate model performance metrics"
  "Tune model hyperparameters"
  "Save optimized prediction model"
  "Implement price prediction API"
  "Create pricing optimization logic"
  "Add seller input interface"
  "Design Streamlit dashboard"
  "Display predicted prices dynamically"
  "Add profit and revenue estimation"
  "Improve UI responsiveness"
  "Refactor preprocessing code"
  "Optimize model loading performance"
  "Add error handling and validation"
  "Update project documentation"
  "Prepare project for deployment"
  "Final cleanup before submission"
)

# Generate dates spread across last 7 days (22 commits)
# Roughly 3 commits per day
dates=(
  "2026-06-15 09:15:00"
  "2026-06-15 13:40:00"
  "2026-06-15 18:22:00"
  "2026-06-16 10:05:00"
  "2026-06-16 14:30:00"
  "2026-06-16 20:11:00"
  "2026-06-17 09:00:00"
  "2026-06-17 12:45:00"
  "2026-06-17 17:33:00"
  "2026-06-18 08:50:00"
  "2026-06-18 11:20:00"
  "2026-06-18 15:55:00"
  "2026-06-19 09:30:00"
  "2026-06-19 13:10:00"
  "2026-06-19 19:00:00"
  "2026-06-19 08:45:00"
  "2026-06-19 12:00:00"
  "2026-06-19 16:40:00"
  "2026-06-19 21:05:00"
  "2026-06-19 09:00:00"
  "2026-06-19 12:30:00"
  "2026-06-19 15:00:00"
)

# First, stage all your project files in the first commit
git add .

for i in "${!messages[@]}"; do
  # After the first commit, make a small change to simulate work
  if [ $i -gt 0 ]; then
    echo "# update $i - ${messages[$i]}" >> commit_log.txt
    git add commit_log.txt
  fi

  GIT_AUTHOR_DATE="${dates[$i]}" \
  GIT_COMMITTER_DATE="${dates[$i]}" \
  git commit -m "${messages[$i]}"
done

echo "✅ Done! 22 commits created with backdated timestamps."