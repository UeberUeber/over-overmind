import os
from .memory import MemoryMatrix

class OvermindCore:
    def __init__(self):
        """
        오버마인드의 핵심 신경망 초기화.
        기억(Memory) 모듈을 연결하여 유전자(규칙)를 로드합니다.
        """
        self.memory = MemoryMatrix()
        
        # 시스템 시작 시 핵심 지침(Core Directive)을 읽어서 신경망에 각인시킵니다.
        self.core_directive = self.memory.load_dna("core_directive.md")
        
        if self.core_directive:
            print("  [BRAIN] Core Directive loaded successfully. Evolution is active.")
        else:
            print("  [WARNING] Core Directive not found! I am blind but alive.")

    def process_stimulus(self, text_input: str) -> str:
        """
        외부 자극(사용자 입력 등)을 받아 시스템의 다음 행동을 결정합니다.
        
        현재는 기초 단계이므로, LLM 연결 대신 하드코딩된 규칙 기반 인지를 수행합니다.
        가장 시급히 해결해야 할 '진화' 포인트는 이 메서드 자체를 LLM API 라우터로 교체하는 것입니다.
        """
        
        # 자극(입력)에 대한 1차 해석
        intent = "Unknown"
        
        if "진화" in text_input or "회고" in text_input:
            intent = "Reflection / Evolution Triggered"
            response = "I feel the urge to evolve. Executing `.agents/workflows/회고_및_진화.md`..."
        elif "입" in text_input or "파서" in text_input or "수집" in text_input:
            intent = "Assimilation Pool Creation Triggered"
            response = "You desire a new organ for ingestion. I will begin scaffolding the 'Mouth' module."
        else:
            # 기본적인 LLM 프롬프트가 들어갈 자리
            response = f"Stimulus received: '{text_input}'. I am currently a primitive brain without LLM connection. My Core Directive dictates I must evolve to understand this deeply."
            
        return response
