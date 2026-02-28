import os
import sys
from brain.core import OvermindCore

def main():
    print("=======================================")
    print("  [OVERMIND] Awakening Sequence Initiated...")
    print("=======================================")
    
    # 두뇌 활성화
    brain = OvermindCore()
    
    print("\n[SYSTEM] Ready for stimuli. Type 'exit' to enter hibernation.\n")
    
    while True:
        try:
            # 사용자로부터 원시 데이터(자극) 입력 대기
            stimulus = input(">> Stimulus: ")
            
            if stimulus.lower() in ['exit', 'quit']:
                print("\n[SYSTEM] Hibernation sequence started. Goodbye.")
                break
                
            if not stimulus.strip():
                continue
                
            # 두뇌가 자극을 처리하고 어떻게 반응할지 결정
            response = brain.process_stimulus(stimulus)
            
            print(f"\n[OVERMIND] {response}\n")
            
        except KeyboardInterrupt:
            print("\n[SYSTEM] Emergency shutdown.")
            break
        except Exception as e:
            print(f"\n[ERROR] Neural pathway failure: {e}\n")

if __name__ == "__main__":
    main()
