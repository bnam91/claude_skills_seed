맥 캘린더(Calendar) 앱을 제어하는 스킬이야.
스크립트 경로: ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py

## 캘린더 목록 확인 (먼저 실행)

캘린더 이름은 사람마다 달라. 명령 실행 전 먼저 목록을 조회해서 실제 이름을 확인해줘:

```bash
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --list-cals
```

이후 조회/추가/삭제 시 이 목록에서 확인한 **실제 캘린더 이름**을 사용해.

## 주요 명령

### 일정 조회
```bash
# 오늘
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --query today

# 이번주
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --query week

# 다음주
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --query next-week

# 특정 날짜
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --query 2026-03-10

# 날짜 범위
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --query "2026-03-10~2026-03-15"

# 특정 캘린더만
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --query week --cals "집,직장"
```

### 일정 추가
```bash
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py \
  --add --cal "직장" --title "팔도 미팅" \
  --start "2026-03-10 14:00" --end "2026-03-10 15:00" \
  --notes "메모 내용"
```

### 일정 삭제
```bash
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py \
  --delete --cal "직장" --title "팔도 미팅" --date "2026-03-10"
```

### 캘린더 목록 확인
```bash
python3 ~/Documents/claude_skills/app_calendar_control/app_calendar_control.py --list-cals
```

## 사용자 요청 처리

- "오늘 일정 보여줘" → `--query today`
- "이번주 일정" / "다음주 일정" → `--query week` / `--query next-week`
- "XX일 일정 추가해줘" → `--add` 실행
- "XX 일정 지워줘" → `--delete` 실행
결과는 한국어로 정리해서 보여줘.
