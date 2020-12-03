from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def start_survey():
    """define title and inst. variables / render start survey html """

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", 
    title = title,
    instructions = instructions)


@app.route("/questions/<int:q_num>")
def show_question(q_num):
    """ takes current question as param and renders html based on question """
    question = survey.questions[q_num]

    return render_template('question.html', 
    question = question)


@app.route("/action")