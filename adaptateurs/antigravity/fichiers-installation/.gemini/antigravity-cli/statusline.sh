#!/bin/bash

input=$(cat)

RESET=$'\033[0m'
BOLD=$'\033[1m'

# Palette high-contrast de Claude
TEXT=$'\033[38;2;230;230;230m'       # #E6E6E6
SECONDARY=$'\033[38;2;160;160;160m'  # #A0A0A0
SUBTLE=$'\033[38;2;115;115;115m'     # #737373
ASSISTANT=$'\033[38;2;170;180;197m'  # #AAB4C5

# États dynamiques
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'
BLUE=$'\033[34m'


model=$(printf '%s' "$input" | jq -r \
  '.model.display_name // .model.id // "Gemini"')

effort=$(printf '%s' "$input" | jq -r \
  '.model.effort // empty')

context_used=$(printf '%s' "$input" | jq -r '
  .context_window.used_percentage
  | if . == null then empty else (floor | tostring) end
')

quota_5h=$(printf '%s' "$input" | jq -r '
  .quota["gemini-5h"].remaining_fraction
  | if . == null then empty else (. * 100 | floor | tostring) end
')

quota_weekly=$(printf '%s' "$input" | jq -r '
  .quota["gemini-weekly"].remaining_fraction
  | if . == null then empty else (. * 100 | floor | tostring) end
')

workspace=$(printf '%s' "$input" | jq -r '
  .workspace.current_dir // .workspace.project_dir // .cwd // empty
')

branch=""
workspace_name=""

if [ -n "$workspace" ]; then
    workspace_name=$(basename "$workspace")
    branch=$(git -C "$workspace" branch --show-current 2>/dev/null)
fi

output="${ASSISTANT}${model}${RESET}"

[ -n "$effort" ] && \
  output="$output ${SECONDARY}${effort}${RESET}"

if [ -n "$context_used" ]; then
    if [ "$context_used" -lt 40 ]; then
        context_color="$GREEN"
    elif [ "$context_used" -lt 70 ]; then
        context_color="$YELLOW"
    else
        context_color="$RED"
    fi

    output="$output ${SUBTLE}·${RESET} Context ${context_color}${context_used}% used${RESET}"
fi

[ -n "$quota_5h" ] && \
  output="$output ${SUBTLE}·${RESET} 5h ${quota_5h}%"

[ -n "$quota_weekly" ] && \
  output="$output ${SUBTLE}·${RESET} weekly ${quota_weekly}%"

[ -n "$branch" ] && \
  output="$output ${SUBTLE}·${RESET} ${BOLD}${BLUE}${branch}${RESET}"

[ -n "$workspace_name" ] && \
  output="$output ${SUBTLE}·${RESET} ${workspace_name}"

printf '%s\n' "$output"
