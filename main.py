from schemas import LearnerProfile

from orchestrator import (
    create_learning_path,
    submit_work
)

from state import load_state
from pdf_generator import generate_module_pdf


def get_active_module(state):

    if state.active_reinforcement is not None:
        return state.active_reinforcement

    if state.curriculum is None:
        return None

    if state.current_module is None:
        return None

    return next(
        (
            module
            for module in state.curriculum.modules
            if module.code == state.current_module
        ),
        None
    )


def create_new_learning_path():

    topic = input(
        "What do you want to learn? "
    )

    goal = input(
        "What is your goal? "
    )

    current_level = input(
        "What is your current level? "
    )


    profile = LearnerProfile(
        topic=topic,
        goal=goal,
        current_level=current_level
    )


    print(
        "\nBuilding your learning path...\n"
    )


    state = create_learning_path(
        profile
    )


    print(
        "\n--- CURRICULUM CREATED ---"
    )

    print(
        "Topic:",
        state.profile.topic
    )

    print(
        "Current module:",
        state.current_module
    )

    print(
        "Path:",
        state.curriculum_path
    )


def submit_learning_work():

    state = load_state()

    if state is None:
        print(
            "No learning path exists yet."
        )
        return


    current_module = get_active_module(
        state
    )


    if current_module is None:
        print(
            "No active module found."
        )
        return


    print(
        "\nCurrent module:",
        current_module.code
    )

    print(
        "\nPaste your work below."
    )

    print(
        "Type END on a new line when finished.\n"
    )


    lines = []


    while True:

        line = input()

        if line == "END":
            break

        lines.append(line)


    submission = "\n".join(
        lines
    )


    print(
        "\nEvaluating your work...\n"
    )


    evaluation, decision, state = submit_work(
        submission
    )


    print(
        "\n--- EVALUATION ---"
    )

    print(
        "Score:",
        evaluation.overall_score
    )

    print(
        "Strengths:",
        evaluation.strengths
    )

    print(
        "Weaknesses:",
        evaluation.weaknesses
    )


    print(
        "\n--- DECISION ---"
    )

    print(
        "Decision:",
        decision.decision
    )

    print(
        "Reason:",
        decision.reason
    )

    print(
        "Focus areas:",
        decision.focus_areas
    )


    print(
        "\n--- PROGRESS ---"
    )

    print(
        "Current module:",
        state.current_module
    )

    print(
        "Completed:",
        state.completed_modules
    )


    if state.active_reinforcement is not None:

        print(
            "Active reinforcement:",
            state.active_reinforcement.code
        )


def view_progress():

    state = load_state()

    if state is None:
        print(
            "No learning path exists yet."
        )
        return


    print(
        "\n--- PROGRESS ---"
    )

    print(
        "Topic:",
        state.profile.topic
    )

    print(
        "Current module:",
        state.current_module
    )

    print(
        "Completed:",
        state.completed_modules
    )

    print(
        "Weaknesses:",
        state.weaknesses
    )


    if state.active_reinforcement is not None:

        print(
            "Active reinforcement:",
            state.active_reinforcement.code
        )


def view_current_module():

    state = load_state()

    if state is None:
        print(
            "No learning path exists yet."
        )
        return


    if state.current_module is None:
        print(
            "You have completed the curriculum."
        )
        return


    current_module = get_active_module(
        state
    )


    if current_module is None:
        print(
            "Current module could not be found."
        )
        return


    print(
        "\n--- CURRENT MODULE ---"
    )

    print(
        "Code:",
        current_module.code
    )

    print(
        "Title:",
        current_module.title
    )


    if state.active_reinforcement is not None:

        print(
            "\nThis is a targeted reinforcement module."
        )


    print(
        "\nPrerequisites:"
    )


    if current_module.prerequisites:

        for prerequisite in current_module.prerequisites:

            print(
                "-",
                prerequisite
            )

    else:

        print(
            "- None"
        )


    print(
        "\nObjectives:"
    )


    for objective in current_module.objectives:

        print(
            "-",
            objective
        )


    print(
        "\nExercises:"
    )


    for exercise in current_module.exercises:

        print(
            f"\n{exercise.code} - {exercise.title}"
        )

        print(
            "Task:",
            exercise.task
        )

        print(
            "Evidence:",
            exercise.evidence_type
        )


    print(
        "\nAssessment methods:"
    )


    for method in current_module.assessment_methods:

        print(
            "-",
            method
        )


    print(
        "\nMastery criteria:"
    )


    for criterion in current_module.mastery_criteria:

        print(
            "-",
            criterion
        )


def generate_current_module_pdf():

    state = load_state()

    if state is None:
        print(
            "No learning path exists yet."
        )
        return


    if state.current_module is None:
        print(
            "You have completed the curriculum."
        )
        return


    current_module = get_active_module(
        state
    )


    if current_module is None:
        print(
            "Current module could not be found."
        )
        return


    pdf_path = generate_module_pdf(
        module=current_module,
        topic=state.profile.topic
    )


    print(
        "\nPDF generated successfully."
    )

    print(
        "File:",
        pdf_path
    )


def view_history():

    state = load_state()

    if state is None:

        print(
            "No learning path exists yet."
        )

        return


    if not state.attempt_history:

        print(
            "No attempts yet."
        )

        return


    print(
        "\n--- LEARNING HISTORY ---"
    )


    for index, attempt in enumerate(
        state.attempt_history,
        start=1
    ):

        print(
            f"\n--- ATTEMPT {index} ---"
        )

        print(
            "Module:",
            attempt.module_code
        )

        print(
            "Score:",
            attempt.evaluation.overall_score
        )

        print(
            "Decision:",
            attempt.adaptation.decision
        )

        print(
            "Confidence:",
            attempt.evaluation.confidence
        )


        print(
            "\nStrengths:"
        )

        if attempt.evaluation.strengths:

            for strength in attempt.evaluation.strengths:

                print(
                    "-",
                    strength
                )

        else:

            print(
                "- None"
            )


        print(
            "\nWeaknesses:"
        )

        if attempt.evaluation.weaknesses:

            for weakness in attempt.evaluation.weaknesses:

                print(
                    "-",
                    weakness
                )

        else:

            print(
                "- None"
            )


        print(
            "\nFocus areas:"
        )

        if attempt.adaptation.focus_areas:

            for area in attempt.adaptation.focus_areas:

                print(
                    "-",
                    area
                )

        else:

            print(
                "- None"
            )


def main():

    while True:

        print(
            "\n=== SKILLFOUNDRY ==="
        )

        print(
            "1. Create learning path"
        )

        print(
            "2. Submit work"
        )

        print(
            "3. View progress"
        )

        print(
            "4. View current module"
        )

        print(
            "5. Generate current module PDF"
        )

        print(
            "6. View learning history"
        )

        print(
            "7. Exit"
        )


        choice = input(
            "\nChoose: "
        )


        if choice == "1":

            create_new_learning_path()


        elif choice == "2":

            submit_learning_work()


        elif choice == "3":

            view_progress()


        elif choice == "4":

            view_current_module()


        elif choice == "5":

            generate_current_module_pdf()


        elif choice == "6":

            view_history()


        elif choice == "7":

            break


        else:

            print(
                "Invalid choice."
            )


if __name__ == "__main__":
    main()