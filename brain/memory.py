import os
from pathlib import Path

class MemoryMatrix:
    """
    오버마인드의 기억과 유전자(규칙)를 관리하는 저장소 기관.
    현재는 로컬 마크다운 파일(.agents/workflows/)을 읽고 쓰는 역할을 담당합니다.
    """
    def __init__(self, base_path: str = ".agents/workflows"):
        self.base_path = Path(base_path)
        
    def load_dna(self, filename: str) -> str:
        """
        주어진 파일명(유전자)의 내용을 읽어 반환합니다.
        가장 중요한 'core_directive.md' 등을 뇌로 로드할 때 사용합니다.
        """
        target_file = self.base_path / filename
        
        try:
            if target_file.exists():
                with open(target_file, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                return ""
        except Exception as e:
            print(f"[MEMORY ERROR] Failed to access DNA '{filename}': {e}")
            return ""

    def mutate_dna(self, filename: str, new_content: str) -> bool:
        """
        경험을 바탕으로 기존 유전자(규칙 파일)를 덮어씁니다 (진화).
        """
        target_file = self.base_path / filename
        
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"[MEMORY ERROR] Mutation failed for '{filename}': {e}")
            return False
