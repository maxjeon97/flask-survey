from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# satisfaction_survey = Survey(
#     "Customer Satisfaction Survey",
#     "Please fill out a survey about your experience with us.",
#     [
#         Question("Have you shopped here before?"),
#         Question("Did someone else shop with you today?"),
#         Question(
#             "On average, how much do you spend a month on frisbees?",
#             ["Less than $10,000", "$10,000 or more"]),
#         Question("Are you likely to shop here again?"),
#     ])

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def survey_start():
    title = survey.title
    instructions = survey.instructions

    return render_template(
        "survey_start.html", title=title, instructions=instructions)


@app.post("/begin")
def begin():
    return redirect("/questions/0")


@app.get("/questions/<number>")
def question(number):
    question = survey.questions[int(number)]
    return render_template("question.html", prompt=question.prompt, choices=question.choices)


@app.post("/answer")
def handle_answer():
    responses.append(request.form["answer"])
    next_question_num = str(len(responses))
    return redirect(f"/questions/{next_question_num}")

