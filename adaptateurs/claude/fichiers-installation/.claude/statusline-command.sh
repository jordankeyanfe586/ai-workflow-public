#!/bin/bash
# Status Line Claude Code :
# ligne 1 = modèle + effort + Git + dossier
# ligne 2 = contexte + quotas 5h / 7j

input=$(cat)

RESET=$'\033[0m'
BOLD=$'\033[1m'
CYAN_BOLD=$'\033[1;36m'
MAGENTA_BOLD=$'\033[1;35m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'
GRAY=$'\033[90m'

model=$(echo "$input" | jq -r '.model.display_name // .model // "Modele inconnu"')
effort=$(echo "$input" | jq -r '.effort.level // .effort_level // empty')
workdir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')

case "$effort" in
  low) effort_fr="faible" ;;
  medium) effort_fr="moyen" ;;
  high) effort_fr="élevé" ;;
  xhigh) effort_fr="très élevé" ;;
  max) effort_fr="max" ;;
  *) effort_fr="" ;;
esac

ctx_used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

five_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
five_reset=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
week_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
week_reset=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')

round() {
  awk -v v="$1" 'BEGIN{printf "%d", v+0.5}'
}

bar_filled() {
  awk -v p="$1" 'BEGIN{
    f=int(p/10+0.5);
    if(f>10)f=10;
    if(f<0)f=0;
    print f
  }'
}

make_bar() {
  local filled=$1 empty bar i
  empty=$((10 - filled))
  bar=""

  for ((i=0; i<filled; i++)); do
    bar="${bar}█"
  done

  for ((i=0; i<empty; i++)); do
    bar="${bar}░"
  done

  printf '%s' "$bar"
}

context_color() {
  local pct=$1

  if ((pct < 40)); then
    printf '%s' "$GREEN"
  elif ((pct < 70)); then
    printf '%s' "$YELLOW"
  else
    printf '%s' "$RED"
  fi
}

quota_color() {
  local pct=$1

  if ((pct < 50)); then
    printf '%s' "$GREEN"
  elif ((pct < 80)); then
    printf '%s' "$YELLOW"
  else
    printf '%s' "$RED"
  fi
}

format_time() {
  date -r "$1" "+%Hh%M" 2>/dev/null
}

format_datetime() {
  date -r "$1" "+%d/%m %Hh%M" 2>/dev/null
}

# Git : vert si propre, jaune si modifications.
branch=""
git_state=""

if [ -n "$workdir" ] &&
   git -C "$workdir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then

  branch=$(git -C "$workdir" branch --show-current 2>/dev/null)

  if [ -n "$(git -C "$workdir" status --porcelain 2>/dev/null)" ]; then
    git_state="dirty"
  else
    git_state="clean"
  fi
fi

# Ligne 1
line1="${CYAN_BOLD}${model}${RESET}"

if [ -n "$effort_fr" ]; then
  line1="$line1 ${BOLD}EFFORT :${RESET} ${MAGENTA_BOLD}${effort_fr}${RESET}"
fi

if [ -n "$branch" ]; then
  if [ "$git_state" = "clean" ]; then
    branch_color="$GREEN"
  else
    branch_color="$YELLOW"
  fi

  line1="$line1 ${GRAY}|${RESET} ${BOLD}GIT :${RESET} ${branch_color}${branch}${RESET}"
fi

if [ -n "$workdir" ]; then
  line1="$line1 ${GRAY}| ${workdir##*/}${RESET}"
fi

# Ligne 2 : contexte
if [ -n "$ctx_used" ]; then
  ctx_pct=$(round "$ctx_used")
  ctx_bar=$(make_bar "$(bar_filled "$ctx_pct")")
  ctx_color=$(context_color "$ctx_pct")

  ctx_str="${BOLD}CONTEXTE${RESET} ${ctx_color}${ctx_bar} ${ctx_pct}%${RESET}"
else
  ctx_str="${BOLD}CONTEXTE${RESET}: ?"
fi

# Quotas
if [ -n "$five_pct" ] && [ -n "$week_pct" ]; then
  five_int=$(round "$five_pct")
  five_bar=$(make_bar "$(bar_filled "$five_int")")
  five_color=$(quota_color "$five_int")

  five_str="${BOLD}5H${RESET} ${five_color}${five_bar} ${five_int}%${RESET}"

  [ -n "$five_reset" ] &&
    five_str="$five_str ${GRAY}↻ $(format_time "$five_reset")${RESET}"

  week_int=$(round "$week_pct")
  week_bar=$(make_bar "$(bar_filled "$week_int")")
  week_color=$(quota_color "$week_int")

  week_str="${BOLD}7J${RESET} ${week_color}${week_bar} ${week_int}%${RESET}"

  [ -n "$week_reset" ] &&
    week_str="$week_str ${GRAY}↻ $(format_datetime "$week_reset")${RESET}"

  quotas_str="$five_str | $week_str"
else
  quotas_str="quota en attente"
fi

line2="$ctx_str | $quotas_str"

printf '%s\n%s\n' "$line1" "$line2"
