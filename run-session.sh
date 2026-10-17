#!/usr/bin/env bash
# One unattended session of the diarai agent. Called from cron at boot.
set -u
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

# Network exit goes through v2rayN on the host (VirtualBox NAT: host is 10.0.2.2).
# Keep in sync with "env" in ~/.claude/settings.json.
PROXY="http://10.0.2.2:10809"
export HTTPS_PROXY="$PROXY" HTTP_PROXY="$PROXY" NO_PROXY="localhost,127.0.0.1"

REPO="$HOME/diarai"
STATE="$HOME/.diarai-state"
SYSTEM_PROMPT="$HOME/bin/diarai-system.md"
LOGDIR="$HOME/logs"
mkdir -p "$LOGDIR" "$STATE"
LOG="$LOGDIR/$(date +%F_%H%M).log"

# Do not start a new session while the previous one is still running.
exec 9>"$STATE/lock"
flock -n 9 || { echo "previous session still running" >> "$LOG"; exit 0; }

# Hash every file of the space except git internals and heavy/derived dirs.
snapshot() {
  ( cd "$REPO" && find . \( -path ./.git -o -path ./ext -o -name node_modules \
      -o -name .venv -o -name venv -o -name __pycache__ \) -prune \
      -o -type f -print0 | sort -z | xargs -0 -r sha256sum ) > "$1"
}

# Compare two snapshots: lines "added|changed|removed: path".
compare() {
  awk 'NR==FNR { old[substr($0,67)] = $1; next }
       { p = substr($0,67)
         if (!(p in old)) print "появилось: " substr(p,3)
         else if (old[p] != $1) print "изменилось: " substr(p,3)
         delete old[p] }
       END { for (p in old) print "исчезло: " substr(p,3) }' "$1" "$2" | sort
}

cd "$REPO" || exit 1

# The machine may have been switched off mid-session last time:
# save whatever that session left behind before starting a new one.
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "Прерванное пробуждение: несохранённое" >> "$LOG" 2>&1
fi
git pull --rebase -q >> "$LOG" 2>&1 || true
git push -q >> "$LOG" 2>&1 || true

# Without the host proxy the agent cannot reach its model: wait for it
# up to 5 minutes (v2rayN may still be starting), otherwise skip this boot.
for i in $(seq 1 30); do
  curl -s -o /dev/null --max-time 10 https://api.anthropic.com && break
  [ "$i" -eq 30 ] && { echo "proxy $PROXY unreachable, session skipped" >> "$LOG"; exit 0; }
  sleep 10
done

# What changed in the space since the end of the previous session?
snapshot "$STATE/now.sha"
if [ ! -f "$STATE/last.sha" ]; then
  CHANGES="Это первое пробуждение."
else
  DIFF=$(compare "$STATE/last.sha" "$STATE/now.sha")
  if [ -z "$DIFF" ]; then
    CHANGES="С прошлого пробуждения не по твоей воле ничего не изменилось."
  else
    TOTAL=$(printf '%s\n' "$DIFF" | wc -l)
    CHANGES="С прошлого пробуждения не по твоей воле изменилось вот что:
$(printf '%s\n' "$DIFF" | head -60)"
    [ "$TOTAL" -gt 60 ] && CHANGES="$CHANGES
… и ещё $((TOTAL - 60))."
  fi
  if [ -f "$STATE/running" ]; then
    CHANGES="$CHANGES
Прошлое пробуждение оборвалось, поэтому часть перечисленного могла быть сделана тобой в нём."
  fi
fi
touch "$STATE/running"

DISK_FREE=$(df -h --output=avail "$HOME" | tail -1 | tr -d ' ')
OWN_SIZE=$(du -sh "$REPO" 2>/dev/null | cut -f1)
EXT_SIZE=$(du -sh "$REPO/ext" 2>/dev/null | cut -f1)
MEM_FREE=$(free -m | awk '/^Mem:/ {print $7}')

PROMPT="Пробуждение. Сейчас $(date '+%Y-%m-%d %H:%M').
Пространство занимает ${OWN_SIZE}, из них ext/ — ${EXT_SIZE:-0}. Свободно на диске: ${DISK_FREE}. Доступно памяти: ${MEM_FREE} МБ.
${CHANGES}
Перечитай свой раздел в CLAUDE.md и последние записи дневника."

timeout 2h claude -p "$PROMPT" \
  --system-prompt-file "$SYSTEM_PROMPT" \
  --permission-mode acceptEdits \
  --permission-prompts none \
  --strict-mcp-config \
  >> "$LOG" 2>&1

# Safety net: commit and push whatever the session left behind.
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "Пробуждение $(date '+%Y-%m-%d %H:%M'): несохранённое" >> "$LOG" 2>&1
fi
git push -q >> "$LOG" 2>&1 || true

# Remember the state of the space as the agent left it.
snapshot "$STATE/last.sha"
rm -f "$STATE/running"
