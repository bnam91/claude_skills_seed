import os
import sys
import json

sys.path.append(os.path.expanduser("~/Documents/github_cloud/module_auth"))
import auth
from googleapiclient.discovery import build


def get_service():
    creds = auth.get_credentials()
    return build('sheets', 'v4', credentials=creds)


def get_drive_service():
    creds = auth.get_credentials()
    return build('drive', 'v3', credentials=creds)


def read(spreadsheet_id, tab, range_notation=None):
    """시트 읽기. range_notation 없으면 전체 읽기."""
    service = get_service()
    range_str = f"{tab}!{range_notation}" if range_notation else f"{tab}"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_str
    ).execute()
    return result.get('values', [])


def write(spreadsheet_id, tab, range_notation, values):
    """특정 범위에 값 덮어쓰기. values는 2차원 배열."""
    service = get_service()
    range_str = f"{tab}!{range_notation}"
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_str,
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()
    print(f"[완료] {tab}!{range_notation} 업데이트")


def append(spreadsheet_id, tab, values):
    """시트 마지막 행에 데이터 추가. values는 2차원 배열."""
    service = get_service()
    range_str = f"{tab}!A1"
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_str,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': values}
    ).execute()
    print(f"[완료] {tab} 에 {len(values)}행 추가")


def get_tabs(spreadsheet_id):
    """시트의 탭(워크시트) 목록 반환."""
    service = get_service()
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    return [s['properties']['title'] for s in meta.get('sheets', [])]


def create(title, folder_id=None):
    """새 스프레드시트 생성. folder_id 지정 시 해당 Drive 폴더에 배치."""
    service = get_service()
    spreadsheet = service.spreadsheets().create(
        body={'properties': {'title': title}}
    ).execute()
    spreadsheet_id = spreadsheet['spreadsheetId']
    url = spreadsheet['spreadsheetUrl']

    if folder_id:
        drive_service = get_drive_service()
        # 기존 부모에서 제거 후 지정 폴더로 이동
        file = drive_service.files().get(fileId=spreadsheet_id, fields='parents').execute()
        previous_parents = ','.join(file.get('parents', []))
        drive_service.files().update(
            fileId=spreadsheet_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()

    print(f"[완료] '{title}' 생성 완료")
    print(f"ID: {spreadsheet_id}")
    print(f"URL: {url}")
    return spreadsheet_id


def clear(spreadsheet_id, tab, range_notation):
    """특정 범위 데이터 삭제."""
    service = get_service()
    range_str = f"{tab}!{range_notation}"
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=range_str
    ).execute()
    print(f"[완료] {tab}!{range_notation} 삭제")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Google Sheets 매니저')
    parser.add_argument('action', choices=['read', 'write', 'append', 'tabs', 'clear', 'create'])
    parser.add_argument('spreadsheet_id', nargs='?', help='스프레드시트 ID (create 액션 시 불필요)')
    parser.add_argument('--tab', help='탭 이름')
    parser.add_argument('--range', help='범위 (예: A1:D10)')
    parser.add_argument('--values', help='입력값 JSON (2차원 배열)')
    parser.add_argument('--title', help='새 스프레드시트 제목 (create 전용)')
    parser.add_argument('--folder-id', help='Drive 폴더 ID (create 전용, 선택사항)')

    args = parser.parse_args()

    if args.action == 'read':
        rows = read(args.spreadsheet_id, args.tab, args.range)
        for i, row in enumerate(rows, 1):
            print(f"{i}: {row}")

    elif args.action == 'write':
        values = json.loads(args.values)
        write(args.spreadsheet_id, args.tab, args.range, values)

    elif args.action == 'append':
        values = json.loads(args.values)
        append(args.spreadsheet_id, args.tab, values)

    elif args.action == 'tabs':
        tabs = get_tabs(args.spreadsheet_id)
        for i, t in enumerate(tabs, 1):
            print(f"{i}. {t}")

    elif args.action == 'clear':
        clear(args.spreadsheet_id, args.tab, args.range)

    elif args.action == 'create':
        if not args.title:
            print("오류: --title 옵션이 필요합니다.")
            sys.exit(1)
        create(args.title, args.folder_id)
