"""
Data models for structured business framework outputs
"""

from pydantic import BaseModel, Field
from typing import Optional


class LeanCanvasData(BaseModel):
    """Lean Canvas - 9 blocks structure (모든 필드는 한국어로 작성)"""
    problem: str = Field(description="고객이 직면한 상위 3가지 문제 (한국어로 작성)")
    solution: str = Field(description="해결책의 상위 3가지 기능 (한국어로 작성)")
    unique_value_prop: str = Field(description="당신이 다르고 구매할 가치가 있는 이유를 명확하게 전달하는 단일 메시지 (한국어로 작성)")
    unfair_advantage: str = Field(description="쉽게 복사하거나 구매할 수 없는 것 (한국어로 작성)")
    customer_segments: str = Field(description="타겟 고객과 사용자 (한국어로 작성)")
    key_metrics: str = Field(description="비즈니스가 어떻게 진행되고 있는지 알려주는 핵심 숫자 (한국어로 작성)")
    channels: str = Field(description="고객에게 도달하는 경로 (한국어로 작성)")
    cost_structure: str = Field(description="고객 획득 비용, 유통 비용, 호스팅, 인력 등 (한국어로 작성)")
    revenue_streams: str = Field(description="수익 모델, 고객 생애 가치, 수익, 총 마진 (한국어로 작성)")


class BusinessModelCanvasData(BaseModel):
    """Business Model Canvas - 9 blocks structure (모든 필드는 한국어로 작성)"""
    key_partners: str = Field(description="핵심 파트너/공급업체는 누구인가요? 어떤 핵심 자원을 그들로부터 획득하나요? (한국어로 작성)")
    key_activities: str = Field(description="가치 제안을 위해 필요한 핵심 활동은 무엇인가요? (한국어로 작성)")
    key_resources: str = Field(description="가치 제안을 위해 필요한 핵심 자원은 무엇인가요? (한국어로 작성)")
    value_propositions: str = Field(description="고객에게 제공하는 가치는 무엇인가요? 어떤 문제를 해결하나요? (한국어로 작성)")
    customer_relationships: str = Field(description="각 고객 세그먼트가 기대하는 관계 유형은 무엇인가요? (한국어로 작성)")
    channels: str = Field(description="고객에게 어떻게 도달하고 가치를 전달하나요? (한국어로 작성)")
    customer_segments: str = Field(description="가장 중요한 고객은 누구인가요? (한국어로 작성)")
    cost_structure: str = Field(description="비즈니스 모델에 내재된 가장 중요한 비용은 무엇인가요? (한국어로 작성)")
    revenue_streams: str = Field(description="고객이 어떤 가치에 대해 비용을 지불하나요? 어떻게 지불하나요? (한국어로 작성)")
