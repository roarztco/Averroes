from schemas import LearnerState, EvaluationResult, AdaptationDecision


def apply_progress(
    state: LearnerState,
    evaluation: EvaluationResult,
    decision: AdaptationDecision
):
    # Save mastery scores
    for item in evaluation.mastery:
        state.mastery[item.concept] = item.score

    # Save current weaknesses
    state.weaknesses = evaluation.weaknesses

    # Remember why the state changed
    state.last_evaluation = evaluation
    state.last_adaptation = decision

    # Advance only when the Adaptation Agent recommends it
    if decision.decision == "ADVANCE":

        if state.current_module not in state.completed_modules:
            state.completed_modules.append(state.current_module)

        current_index = state.curriculum_path.index(state.current_module)

        if current_index + 1 < len(state.curriculum_path):
            state.current_module = state.curriculum_path[current_index + 1]
        else:
            state.current_module = None