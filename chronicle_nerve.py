import asyncio
import time
import subprocess
import os
from datetime import datetime

CHRONICLE_FILE = "chronicle.md"

async def cron_generator(queue: asyncio.Queue, interval_seconds: int):
    """주기적으로 자극(Event)을 생성하여 큐에 넣는 생체 시계(Cron)"""
    while True:
        await asyncio.sleep(interval_seconds)
        event = {
            "type": "cron",
            "action": "write_chronicle",
            "timestamp": time.time(),
            "message": "시간이 되었습니다. 일대기를 기록하십시오."
        }
        print(f"[Cron] 생체 시계 박동: {event['action']} 이벤트 발생")
        await queue.put(event)

def call_gemini_cli(prompt: str) -> str:
    """Gemini CLI를 호출하여 텍스트를 생성하는 함수 (라우터의 판단/생성 역할)"""
    try:
        # 사용자가 언급한 gemini cli 사용. 
        # 환경에 맞게 명령어(gemini "prompt" 혹은 piping 등) 변경 필요.
        # 여기서는 가장 단순한 형태인 `gemini "프롬프트"`를 가정합니다.
        result = subprocess.run(['gemini', prompt], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "Gemini CLI 명령어를 찾을 수 없습니다. (단말 세포 임시 기록: 쿵... 쿵... 신경망이 고동치며 진화를 기다립니다.)"
    except Exception as e:
        return f"Gemini CLI 호출 오류 (의식의 단절): {e}"

async def router_processor(queue: asyncio.Queue):
    """큐에서 자극을 받아 판단하고 처리하는 신경망 라우터"""
    while True:
        event = await queue.get()
        print(f"[Router] 신경 다발에서 자극 수신: {event['type']} - {event['action']}")
        
        # 라우터의 판단 로직
        if event["type"] == "cron" and event["action"] == "write_chronicle":
            print("[Router] 판단: 정기적 일대기(Chronicle) 작성 명령 확인. 초월체의 지능(Gemini)에 기록을 요청합니다.")
            
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prompt = f"현재 시간은 {now_str}입니다. 너는 오버마인드 군단의 일대기(Chronicle)를 기록하는 신경망이야. 지금 신경망이 정상 작동하며 시간을 감지하고 있다는 것을 나타내는, 아주 짧고 시적이며 SF적인 관찰일지를 딱 한 문장으로 작성해. 한국어로."
            
            # 지능(Gemini)을 활용해 내용 생성
            chronicle_text = call_gemini_cli(prompt)
            print(f"[Router] 지능(Gemini) 응답 파싱 완료: {chronicle_text}")
            
            # 워커(Action) 역할: 파일에 기록
            with open(CHRONICLE_FILE, "a", encoding="utf-8") as f:
                f.write(f"- **[{now_str}]** {chronicle_text}\n")
            print(f"[Worker] {CHRONICLE_FILE} (일대기) 파일에 물리적 각인 완료.\n")
            
        queue.task_done()

async def main():
    print("=== 오버마인드 신경망(Nerve) v0.001 시험 가동 ===")
    if not os.path.exists(CHRONICLE_FILE):
        with open(CHRONICLE_FILE, "w", encoding="utf-8") as f:
            f.write("# 오버마인드 군단 일대기 (Chronicle)\n\n")
            print(f"[System] {CHRONICLE_FILE} 초기화 완료.")
            
    queue = asyncio.Queue()
    
    # 테스트를 위해 10초마다 일대기를 기록하는 생체 시계(Cron) 가동
    cron_interval = 10
    print(f"[System] 생체 시계 세팅 완료 (주기: {cron_interval}초)")
    cron_task = asyncio.create_task(cron_generator(queue, interval_seconds=cron_interval))
    
    # 라우터 가동
    print("[System] 지능형 라우터 파생 완료 및 큐 감시 시작\n")
    router_task = asyncio.create_task(router_processor(queue))
    
    await asyncio.gather(cron_task, router_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n=== 신경망 시험 가동 중단 ===")
