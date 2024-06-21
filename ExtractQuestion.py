import asyncio
from edsl import Question
from edsl import QuestionFreeText, QuestionList, Scenario, Survey, QuestionYesNo, QuestionMultipleChoice
from edsl.questions import QuestionBase

def generate_edsl_code(question_text: str) -> QuestionBase:
    s = Scenario({'question': question_text})

    q_text = QuestionFreeText(
        question_text="""This is a survey question: '{{question}}'.
                        Please extract the question text. """, 
        question_name="question_text"
    )

    q_type = QuestionMultipleChoice(
        question_text="""This is a survey question: '{{question}}'.
                        What is the question type?""",
        question_options=["linear_scale", "multiple_choice", "free_text", "numerical", "checkbox"],
        question_name="question_type"
    )

    q_name = QuestionFreeText(
        question_text="""This is a survey question: '{{question}}'.
                        The question could have a unique identifier or key - probably a string or number.
                        If it has one, please extract it.
                        Just return the key itself. """,
        question_name="question_name"
    )

    q_is_linear = QuestionYesNo(
        question_text="""This is a survey question: '{{question}}'.
                        Is this a linear scale question (with numerical values, possibly with labels)?""",
        question_name="is_linear_scale"
    )

    q_options = QuestionList(
        question_text="""This is a survey question: '{{question}}'.
                        If it is a multiple choice question, please extract the options.
                        If it looks like a linear scale question, only extract the numbers.""",
        question_name="question_options"
    )

    survey = Survey([q_text, q_type, q_name, q_is_linear, q_options])
    print("Survey created")
    print("Running survey")
    job = survey.by(s)
    results = job.run(cache = None)
    print("Survey run")
    question_params = results.select('answer.*').to_dicts()[0]
    question_params.pop('is_linear_scale')
    if question_params['question_type'] == 'free_text':
        _ = question_params.pop('question_options')
    q = Question(**question_params)
    return q

