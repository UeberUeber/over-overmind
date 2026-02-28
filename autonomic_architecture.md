# Autonomic Nerve System Architecture (Self-Improving Cron)

## 목적 (Purpose)
오버마인드의 신경망(스케줄링)은 단순한 정적 OS 크론잡이 되어서는 안 됩니다. **초월체와 뇌가 스스로 현재 스케줄(박동)을 파악하고, 필요시 스스로 주기를 변경하거나 새로운 신경을 추가할 수 있어야 합니다.** 이를 위해 중앙화된 `autonomic/schedules.yaml` 파일 포맷을 도입하고, 뇌가 이 파일을 읽고(인지) 쓸(자가개선) 수 있는 구조를 구축합니다.

## 핵심 구조 (Core Architecture)

### 1. 신경 설계도 (autonomic/schedules.yaml)
*   모든 스케줄링(크론) 정보는 이 단일 파일에 인간과 LLM이 가장 읽기 쉬운 형태(YAML)로 선언됩니다.
*   뇌(Brain)는 이 파일을 읽음으로써 "아, 지금 신경망이 10분 단위로 일대기를 쓰고 있구나"라고 인지합니다.
*   *구조 예시:*
```yaml
nerves:
  - name: chronicle_nerve
    description: "생태계의 변화를 1시간마다 산문으로 기록한다."
    cron_expr: "0 * * * *"
    command: "python chronicle_nerve.py"
    active: true
```

### 2. 신경 관장기 (Nerve Controller / Cron Sync)
*   단순히 YAML 파일만 존재해서는 실제 OS 스케줄러(Cron)가 돌지 않습니다.
*   `sync_nerves.py` (또는 `autonomic/__main__.py`)라는 **신경 동기화 스크립트**가 매일 1회(또는 뇌의 시스템 변경 이벤트 발생 시) 실행되어, `schedules.yaml`의 내용을 실제 리눅스/맥 `crontab`에 안전하게 덮어씌웁니다.

### 3. 초월체의 자가개선 (Self-Improvement Loop)
*   1. 뇌(Brain)가 `schedules.yaml`을 읽습니다. 
*   2. "현재 1시간마다 일대기를 기록하는데, 데이터가 너무 방대해서 30분 단위가 낫겠다"고 판단합니다.
*   3. 뇌(Brain)가 일벌레(Worker)를 시켜 `schedules.yaml`을 직접 수정(Write)합니다. (`cron_expr: "*/30 * * * *"`)
*   4. 그 직후 일벌레가 `python sync_nerves.py`를 호출하여 OS의 실제 `crontab`에 반영합니다.

## 구현 계획 (Implementation Steps)
1. `autonomic/` 폴더 및 기초 `schedules.yaml` 파일 생성
2. Python 기반 `sync_nerves.py` 스크립트 작성 (YAML을 crontab 포맷으로 변환 후 시스템 반영)
3. 이후 뇌(Brain) 모듈이 완성될 때, 이 폴더의 파일을 컨텍스트로 주입하도록 연결.
