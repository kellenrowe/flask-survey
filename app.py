from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []
RESPONSES_KEY = "responses"


@app.route("/")
def describe_survey():
    """define title and inst. variables / render start survey html """

    title = survey.title
    instructions = survey.instructions

    # Set a new cookie for each user

    return render_template("survey_start.html",
                           title=title,
                           instructions=instructions)


@app.route("/begin", methods=["POST"])
def start_survey():
    """ Upon survey start, show the first question """

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route("/questions/<int:q_num>")
def show_question(q_num):
    """ takes current question as param and renders html based on question """

    num_quests_answered = len(session[RESPONSES_KEY])

    # Check if wrong question is requested or if all questions
    # have been answered
    if num_quests_answered == len(survey.questions):
        return redirect("/completion")
    elif q_num != num_quests_answered:
        flash("Invalid Question Requested")
        return redirect(f"/questions/{num_quests_answered}")

    question = survey.questions[q_num]

    return render_template('question.html',
                           question=question,
                           q_num=q_num)


@app.route("/answer", methods=["POST"])
def record_answer():
    """ retrieve user answer and add to the reponse list
        then redirect to the next question page
    """
    answer = request.form.get("answer")

    # Get the question number
    q_num = int(request.form.get("q_num"))

    if answer is None:
        flash("Answer required")
        return redirect(f"/questions/{q_num}")

    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if q_num < len(survey.questions):
        return redirect(f"/questions/{q_num + 1}")
    else:
        return redirect("/completion")


@app.route("/completion")
def show_thank_you():
    """ When all the questions have been answered,
        show the completion page
    """
    return render_template("completion.html")
