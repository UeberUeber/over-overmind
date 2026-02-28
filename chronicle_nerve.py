import time
import subprocess
import os
from datetime import datetime
import sys

CHRONICLE_DIR = "chronicle"
INTERVAL_SECONDS = 3600  # 1시간 (기본값)

def check_environment_changes(since_seconds: int) -> dict:
    """최근 N초 동안의 시스템(Git, 파일 등) 변경 사항을 수집합니다."""
    changes = {
        "commits": [],
        "modified_files": []
    }
    try:
        # 최근 변경된 파일 확인 (git status)
        git_status_result = subprocess.run(
            ['git', 'status', '--porcelain'], capture_output=True, text=True, check=False
        )
        if git_status_result.stdout:
            changes["modified_files"] = [line[3:] for line in git_status_result.stdout.strip().split('\n') if line]
            
        # 최근 1시간(INTERVAL_SECONDS) 이내 커밋 확인.
        # 시간 단위를 git이 인식할 수 있도록 변환 (예: 60 minutes ago / 1 hours ago)
        hours = max(1, since_seconds // 3600)
        git_log_result = subprocess.run(
            ['git', 'log', f'--since="{hours} hours ago"', '--pretty=format:%h - %s'], 
            capture_output=True, text=True, check=False
        )
        
        if git_log_result.stdout:
            changes["commits"] = git_log_result.stdout.strip().split('\n')

    except Exception as e:
        print(f"[Warning] 환경 관찰 중 오류 발생 (Git 명령 실패 등): {e}")
        pass
    
    return changes

def call_gemini_cli(prompt: str) -> str:
    """Gemini CLI를 호출하여 서사적인 텍스트를 생성합니다."""
    try:
        result = subprocess.run(['gemini', prompt], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        print("[Warning] 'gemini' CLI를 찾을 수 없습니다. 예비 관찰 기록으로 대체합니다.")
        return "The organism pulsed quietly in the background. No profound mutations were observed during this cycle, yet the underlying structures hummed with continuous, silent anticipation of the next evolutionary leap."
    except Exception as e:
        return f"관찰 중 인지 오류 발생 (Context lost): {e}"

def ensure_chronicle_file_exists():
    """연/월에 맞는 디렉토리와 마크다운 파일(영어/한국어)을 준비합니다."""
    now = datetime.utcnow()
    year_str = now.strftime("%Y")
    month_str = now.strftime("%Y-%m")
    
    year_dir = os.path.join(CHRONICLE_DIR, year_str)
    os.makedirs(year_dir, exist_ok=True)
    
    ko_file = os.path.join(year_dir, f"{month_str}-ko.md")
    en_file = os.path.join(year_dir, f"{month_str}.md")
    
    # 한국어 파일 초기화
    if not os.path.exists(ko_file):
        with open(ko_file, "w", encoding="utf-8") as f:
            f.write(f"# Chronicle (한국어) - {month_str}\n\n사라지지 않을 진화의 기록.\n")
            
    # 영어 파일 초기화
    if not os.path.exists(en_file):
        with open(en_file, "w", encoding="utf-8") as f:
            f.write(f"# Chronicle (English) - {month_str}\n\nA living history written in real-time.\n")
            
    return en_file, ko_file

def append_to_chronicle(file_path: str, content: str):
    """해당 날짜 헤더(없으면 생성) 아래에 타임스탬프와 내용을 덧붙입니다."""
    now = datetime.utcnow()
    date_header = f"## {now.strftime('%Y-%m-%d')}"
    time_header = f"### {now.strftime('%H:%M')} UTC"
    
    with open(file_path, "r", encoding="utf-8") as f:
        file_contents = f.read()

    with open(file_path, "a", encoding="utf-8") as f:
        if date_header not in file_contents:
            f.write(f"\n{date_header}\n\n")
            
        f.write(f"{time_header}\n\n{content}\n\n")

def run_chronicle():
    """크론잡(Cron Job)에 의해 1회 실행되는 메인 로직."""
    print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC] Chronicle 신경망 단일 가동 (Stateless)")
    
    print("[Nerve] 환경 관찰 시작...")
    changes = check_environment_changes(INTERVAL_SECONDS)
    
    context_str = f"최근 변경 파일: {changes['modified_files']}\n최근 커밋: {changes['commits']}"
    if not changes["modified_files"] and not changes["commits"]:
         context_str = "지난 1시간 동안 아무런 파일 변경이나 커밋이 없었습니다."

    prompt_ko = f"""
너는 '오버마인드(Overmind)'라는 생명체의 진화와 행동을 관찰하고 기록하는 사학자(Chronicler)야.
절대 단순한 로그나 개조식(bullet points)으로 쓰지 마.
SF 소설이나 역사서의 한 구절처럼, 생명체가 어떤 결정을 내렸고 어떤 변화가 있었는지 서사적인 산문(Prose) 형태로 하나의 짧은 문단으로 작성해.
현재 1시간 동안 관찰된 상태:
{context_str}
"""
    
    print("[Brain] 관찰 내용 분석 및 산문 생성 중...")
    chronicle_text_ko = call_gemini_cli(prompt_ko)
    chronicle_text_en = "[Translation] " + chronicle_text_ko
    
    en_file, ko_file = ensure_chronicle_file_exists()
    
    append_to_chronicle(en_file, chronicle_text_en)
    append_to_chronicle(ko_file, chronicle_text_ko)
    
    print(f"[Worker] 일대기 각인 완료: {ko_file}")

if __name__ == "__main__":
    run_chronicle()
