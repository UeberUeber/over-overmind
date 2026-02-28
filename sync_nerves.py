import os
import sys
import subprocess
from datetime import datetime

try:
    import yaml
except ImportError:
    print("[System] pyyaml 패키지가 필요합니다. 설치를 시도합니다...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEDULES_FILE = os.path.join(BASE_DIR, "autonomic", "schedules.yaml")

# 오버마인드 크론 식별자 (기존 사용자 크론과 섞이지 않도록 블록 지정)
CRON_START_MARKER = "# === OVERMIND NERVES START ==="
CRON_END_MARKER = "# === OVERMIND NERVES END ==="

def load_schedules():
    if not os.path.exists(SCHEDULES_FILE):
        print(f"[Nerve Sync] {SCHEDULES_FILE} 파일이 없습니다.")
        return []
    with open(SCHEDULES_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get("nerves", []) if data else []

def build_cron_lines(nerves):
    lines = [CRON_START_MARKER]
    lines.append(f"# 마지막 신경망 동기화: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    for n in nerves:
        if n.get("active"):
            name = n.get("name")
            cron_expr = n.get("cron_expr", "0 * * * *")
            command = n.get("command")
            
            # 절대 경로 기반 실행 보장: 작업 디렉터리로 이동 후 명령 실행, 출력은 로그 파일로 저장
            full_command = f"cd {BASE_DIR} && {command} >> {BASE_DIR}/cron_output.log 2>&1"
            
            lines.append(f"# [Nerve: {name}] {n.get('description', '')}")
            lines.append(f"{cron_expr} {full_command}")
    lines.append(CRON_END_MARKER)
    return lines

def update_crontab(cron_lines):
    print("[Nerve Sync] 기존 OS 크론 설정 읽는 중...")
    try:
         # crontab -l 실행시 crontab이 아예 없으면 returncode가 1이 됨
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout if result.returncode == 0 else ""
    except Exception:
        current_crontab = ""
        
    lines = current_crontab.split('\n')
    new_lines = []
    in_block = False
    
    # 기존 오버마인드 블록 제거
    for line in lines:
        if line == CRON_START_MARKER:
            in_block = True
            continue
        if line == CRON_END_MARKER:
            in_block = False
            continue
        if not in_block and line.strip() != "":  # 빈 줄 방지
            new_lines.append(line)
            
    # 새 오버마인드 블록 추가
    if cron_lines:
        new_lines.extend(cron_lines)
    
    new_lines.append("") # 마직막 줄바꿈
    new_crontab_content = "\n".join(new_lines)
    
    print("[Nerve Sync] 크론 설정 덮어쓰는 중...")
    process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=new_crontab_content)
    
    if process.returncode == 0:
        print("[System] 신경망 동기화 완료: 생체 주기가 OS(crontab)에 안전하게 각인되었습니다.")
    else:
        print(f"[Error] OS(crontab) 각인 실패: {stderr}")

if __name__ == "__main__":
    print("=== 오버마인드: 신경망 동기화(Nerve Sync) ===")
    print("[Brain] 자율 스케줄 설계도를 읽습니다...")
    nerves = load_schedules()
    if not nerves:
         print("[System] 활성화된 신경망이 없어 동기화를 종료합니다.")
    else:
         cron_lines = build_cron_lines(nerves)
         update_crontab(cron_lines)
