from agents.research_agent import research_agent
from agents.curriculum_agent import curriculum_agent
from agents.evaluator_agent import evaluator_agent
from agents.adaptation_agent import adaptation_agent

from schemas import (
    LearnerProfile,
    LearnerState,
    DomainResearch,
    CurriculumPlan,
    ModulePlan,
    EvaluationResult,
    AdaptationDecision,
    AttemptRecord,
)

from state import load_state, save_state
from progress import apply_progress


def create_learning_path(
    profile: LearnerProfile
) -> LearnerState:

    research_result = research_agent(
        f"""
        Research this learning goal.

        LEARNER PROFILE:

        {profile.model_dump_json(indent=2)}
        """,
        structured_output_model=DomainResearch
    )

    research = research_result.structured_output


    curriculum_result = curriculum_agent(
        f"""
        LEARNER PROFILE:

        {profile.model_dump_json(indent=2)}

        DOMAIN RESEARCH:

        {research.model_dump_json(indent=2)}

        Build the learner's curriculum.
        """,
        structured_output_model=CurriculumPlan
    )

    curriculum = curriculum_result.structured_output


    state = LearnerState(
        profile=profile,
        current_module=curriculum.current_module,
        curriculum_path=curriculum.path,
        curriculum=curriculum
    )

    save_state(state)

    return state


def create_reinforcement(
    current_module: ModulePlan,
    evaluation: EvaluationResult,
    decision: AdaptationDecision
) -> ModulePlan:

    reinforcement_result = curriculum_agent(
        f"""
        Create a targeted reinforcement module.

        CURRENT MODULE:

        {current_module.model_dump_json(indent=2)}

        EVALUATION:

        {evaluation.model_dump_json(indent=2)}

        ADAPTATION DECISION:

        {decision.model_dump_json(indent=2)}

        Focus only on the learner's weaknesses and focus areas.

        Do not regenerate the entire curriculum.

        If the current module code already ends with "-R",
        keep that same code instead of adding another "-R".
        """,
        structured_output_model=ModulePlan
    )

    return reinforcement_result.structured_output


def submit_work(
    submission: str
):

    state = load_state()

    if state is None:
        raise ValueError("No learner state found.")

    if state.curriculum is None:
        raise ValueError("No curriculum found.")

    if state.current_module is None:
        raise ValueError(
            "The learner has completed the curriculum."
        )


    if state.active_reinforcement is not None:

        current_module = state.active_reinforcement

    else:

        current_module = next(
            (
                module
                for module in state.curriculum.modules
                if module.code == state.current_module
            ),
            None
        )


    if current_module is None:
        raise ValueError(
            f"Current module {state.current_module} was not found."
        )


    evaluation_result = evaluator_agent(
        f"""
        CURRENT MODULE:

        {current_module.model_dump_json(indent=2)}

        LEARNER SUBMISSION:

        {submission}

        Evaluate this submission.
        """,
        structured_output_model=EvaluationResult
    )

    evaluation = evaluation_result.structured_output


    adaptation_result = adaptation_agent(
        f"""
        LEARNER PROFILE:

        {state.profile.model_dump_json(indent=2)}

        CURRENT MODULE:

        {current_module.model_dump_json(indent=2)}

        CURRENT CURRICULUM PATH:

        {state.curriculum_path}

        EVALUATION:

        {evaluation.model_dump_json(indent=2)}

        Decide what should happen next.
        """,
        structured_output_model=AdaptationDecision
    )

    decision = adaptation_result.structured_output


    attempt = AttemptRecord(
        module_code=current_module.code,
        submission=submission,
        evaluation=evaluation,
        adaptation=decision
    )

    state.attempt_history.append(
        attempt
    )


    apply_progress(
        state,
        evaluation,
        decision
    )


    if decision.decision == "REINFORCE":

        reinforcement = create_reinforcement(
            current_module,
            evaluation,
            decision
        )

        state.active_reinforcement = reinforcement


    elif decision.decision == "ADVANCE":

        state.active_reinforcement = None


    save_state(state)


    return evaluation, decision, state