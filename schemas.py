from typing import Literal

from pydantic import BaseModel, Field


class LearnerProfile(BaseModel):
    topic: str
    goal: str
    current_level: str

    prior_knowledge: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class DomainResearch(BaseModel):
    domain_name: str
    domain_type: str

    prerequisites: list[str]
    core_areas: list[str]
    recommended_order: list[str]

    learning_methods: list[str]
    assessment_methods: list[str]

    sources: list[str]


class ExercisePlan(BaseModel):
    code: str
    title: str
    task: str
    evidence_type: str


class ModulePlan(BaseModel):
    code: str
    title: str

    prerequisites: list[str]
    objectives: list[str]

    exercises: list[ExercisePlan]

    assessment_methods: list[str]
    mastery_criteria: list[str]


class CurriculumPlan(BaseModel):
    topic: str

    path: list[str]
    modules: list[ModulePlan]

    current_module: str


class MasteryItem(BaseModel):
    concept: str
    score: float = Field(ge=0, le=1)
    evidence: str


class EvaluationResult(BaseModel):
    module_code: str
    overall_score: float = Field(ge=0, le=100)

    mastery: list[MasteryItem]

    strengths: list[str]
    weaknesses: list[str]
    evidence: list[str]

    confidence: Literal[
        "low",
        "medium",
        "high"
    ]


class AdaptationDecision(BaseModel):
    decision: Literal[
        "ADVANCE",
        "REINFORCE",
        "RETRY",
        "SKIP",
        "CHANGE_PATH"
    ]

    reason: str
    next_module: str | None = None

    focus_areas: list[str]
    path_changes: list[str] = Field(default_factory=list)


class AttemptRecord(BaseModel):
    module_code: str
    submission: str

    evaluation: EvaluationResult
    adaptation: AdaptationDecision


class LearnerState(BaseModel):
    profile: LearnerProfile

    current_module: str | None = None

    curriculum_path: list[str] = Field(default_factory=list)
    completed_modules: list[str] = Field(default_factory=list)

    mastery: dict[str, float] = Field(default_factory=dict)
    weaknesses: list[str] = Field(default_factory=list)

    curriculum: CurriculumPlan | None = None

    last_evaluation: EvaluationResult | None = None
    last_adaptation: AdaptationDecision | None = None

    active_reinforcement: ModulePlan | None = None

    attempt_history: list[AttemptRecord] = Field(default_factory=list)