from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []

@app.route("/")
def start_survey():
    """define title and inst. variables / render start survey html """

    title = survey.title
    instructions = survey.instructions

    session["responses"] = []

    # Empty previous answers
    # responses.clear()

    return render_template("survey_start.html",
                           title=title,
                           instructions=instructions)


@app.route("/questions/<int:q_num>", methods=["POST", "GET"])
def show_question(q_num):
    """ takes current question as param and renders html based on question """

    num_quests_answered = len(session["responses"])

    if num_quests_answered == len(survey.questions):
        return redirect("/completion")
    elif q_num != num_quests_answered:
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

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    # Get the next question number
    q_num = int(request.form.get("q_num")) + 1

    if q_num < len(survey.questions):
        return redirect(f"/questions/{q_num}")
    else:
        return redirect("/completion")


@app.route("/completion")
def show_thank_you():
    """ When all the questions have been answered,
        show the completion page
    """
    
    return render_template("completion.html")
