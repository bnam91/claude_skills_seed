# Claude Skills Seed — 직원 세팅 가이드

클론 후 아래 순서대로 세팅하면 돼.

---

## 1. 폴더 배치

```bash
# commands → Claude Code가 읽는 스킬 명령어
cp -r commands/* ~/.claude/commands/

# claude_skills → 스킬이 실행하는 Python 모듈
cp -r claude_skills ~/Documents/claude_skills
```

---

## 2. Google 인증 모듈 설치 (module_auth)

Gmail, Google Drive, Google Sheets 스킬이 공통으로 사용하는 인증 모듈이야.

1. 현빈에게 `module_auth` 폴더 받기
2. 아래 경로에 배치:
   ```
   ~/Documents/github_cloud/module_auth/
   ```
3. Google 인증 자격증명 파일(credentials.json)도 해당 폴더에 넣기

---

## 3. 개인 설정 파일 생성

### Gmail (`~/Documents/claude_skills/gmail_manager/config.json`)

사용할 Gmail 계정 목록 설정:

```json
{
  "accounts": [
    {
      "alias": "별칭",
      "email": "이메일주소@gmail.com"
    }
  ]
}
```

### Google Drive (`~/Documents/claude_skills/gdrive_manager/drives.json`)

접근할 드라이브 폴더 설정:

```json
{
  "drives": [
    {
      "alias": "폴더별칭",
      "folder_id": "구글드라이브_폴더_ID"
    }
  ]
}
```

### 입금요청 즐겨찾기 (`~/Documents/claude_skills/payment_request/favorites.json`)

자주 쓰는 입금처 설정:

```json
{
  "별칭": {
    "item": "품목명",
    "recipient": "수령인",
    "account": "은행 계좌번호 수령인",
    "business_id": ""
  }
}
```

---

## 4. Gmail 토큰 발급

설정 완료 후 Gmail 스킬을 처음 실행하면 브라우저에서 Google 로그인 화면이 뜸.
로그인하면 토큰이 자동 저장돼서 이후엔 자동 인증.

---

## 5. Python 패키지 설치

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

---

## 완료 확인

Claude Code에서 아래 스킬 호출해서 정상 동작하면 세팅 완료:

```
/reminder_manager
/calendar_manager
/gmail_manager
```
