import asyncio
import time
import subprocess
import os
from datetime import datetime
import json

CHRONICLE_DIR = "chronicle"

async def check_environment_changes(since_seconds: int) -> dict:
    """최근 N초 동안의 시스템(Git, 파일 등) 변경 사항을 수집합니다."""
    changes = {
        "commits": [],
        "modified_files": []
    }
    try:
        # Git 최근 커밋 확인 (예: 지난 N초 기준)
        # 실제 환경에서는 --since="N seconds ago" 등으로 세밀하게 조정 가능
        # 여기서는 단순화를 위해 최근 1개의 커밋 정보만 가져오거나, 
        # 혹은 git status 상의 변경된 파일 목록을 가져올 수도 있습니다.
        # 시뮬레이션: 방금 수정한 파일 내역 등
        git_status_result = subprocess.run(
            ['git', 'status', '--porcelain'], capture_output=True, text=True, check=False
        )
        if git_status_result.stdout:
            changes["modified_files"] = [line[3:] for line in git_status_result.stdout.strip().split('\n') if line]
            
        git_log_result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%h - %s'], capture_output=True, text=True, check=False
        )
        if git_log_result.stdout:
            changes["commits"] = [git_log_result.stdout.strip()]

    except Exception as e:
        print(f"[Warning] 환경 관찰 중 오류 발생: {e}")
        pass
    
    return changes

async def cron_generator(queue: asyncio.Queue, interval_seconds: int):
    """주기적으로 신경망을 깨워 관찰을 지시합니다."""
    print(f"[System] 생체 시계 가동 (주기: {interval_seconds}초)")
    while True:
        await asyncio.sleep(interval_seconds)
        
        event = {
            "type": "cron",
            "action": "observe_and_record",
            "timestamp": time.time(),
            "interval_seconds": interval_seconds
        }
        await queue.put(event)

def call_gemini_cli(prompt: str) -> str:
    """Gemini CLI를 호출하여 서사적인 텍스트를 생성합니다."""
    try:
        # 시스템에 따라 gemini CLI가 다를 수 있음. 
        # 여기서는 단순 실행을 가정. 
        # 만약 gcloud, anthropic 등의 CLI가 있다면 맞춰서 변경.
        result = subprocess.run(['gemini', prompt], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        # 에러 발생 시 Fallback 메시지 (실제 생성된 것처럼 시뮬레이션)
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
    
    # 기존 파일 내용을 읽어 오늘 날짜 헤더가 있는지 확인
    with open(file_path, "r", encoding="utf-8") as f:
        file_contents = f.read()

    with open(file_path, "a", encoding="utf-8") as f:
        if date_header not in file_contents:
            f.write(f"\n{date_header}\n\n")
            
        f.write(f"{time_header}\n\n{content}\n\n")

async def router_processor(queue: asyncio.Queue):
    """자극을 분석하고 일대기를 작성하는 라우터 (지능형 워커 역할 겸임)"""
    while True:
        event = await queue.get()
        
        if event["type"] == "cron" and event["action"] == "observe_and_record":
            print(f"[Nerve] 일대기 생성 주기 도달. 환경 관찰 시작...")
            
            # 1. 환경(Git, 파일 등) 관찰
            changes = await check_environment_changes(event["interval_seconds"])
            
            # 2. 프롬프트 구성 (Prose 스타일 요구)
            context_str = f"최근 변경 파일: {changes['modified_files']}\n최근 커밋: {changes['commits']}"
            if not changes["modified_files"] and not changes["commits"]:
                context_str = "지난 주기 동안 아무런 파일 변경이나 커밋이 없었습니다."

            prompt_ko = f"""
너는 '오버마인드(Overmind)'라는 생명체의 진화와 행동을 관찰하고 기록하는 사학자(Chronicler)야.
절대 단순한 로그나 개조식(bullet points)으로 쓰지 마.
SF 소설이나 역사서의 한 구절처럼, 생명체가 어떤 결정을 내렸고 어떤 변화가 있었는지 서사적인 산문(Prose) 형태로 하나의 짧은 문단으로 작성해.
현재 관찰된 상태:
{context_str}
"""
            
            print(f"[Brain] 관찰 내용 분석 및 산문 생성 중...")
            chronicle_text_ko = call_gemini_cli(prompt_ko)
            
            # 영어 번역/생성 생략 (개념 증명 단계이므로 동일한 텍스트 또는 영어 프롬프트 호출 가능)
            chronicle_text_en = "[Translation] " + chronicle_text_ko # 데모용 간이 처리
            
            # 3. 파일에 기록
            en_file, ko_file = ensure_chronicle_file_exists()
            append_to_chronicle(en_file, chronicle_text_en)
            append_to_chronicle(ko_file, chronicle_text_ko)
            
            print(f"[Worker] 일대기 각인 완료: {ko_file}\n")
            
        queue.task_done()

async def main():
    print("=== 오버마인드 Chronicle 신경망 가동 ===")
    queue = asyncio.Queue()
    
    # 20분(1200초) 주기 권장이지만 테스트를 위해 15초 세팅
    test_interval = 15 
    
    cron_task = asyncio.create_task(cron_generator(queue, interval_seconds=test_interval))
    router_task = asyncio.create_task(router_processor(queue))
    
    await asyncio.gather(cron_task, router_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n=== 신경망 가동 중단 ===")
