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
    """generates start page for survey"""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """redirects to first question page upon pressing start button"""

    return redirect("/questions/0")


@app.get("/questions/<int:number>")
def question(number):
    """displays question based on its url parameter number"""

    question = survey.questions[number]
    return render_template("question.html", question=question)


@app.post("/answer")
def handle_answer():
    """handles question submission, redirects to thank you
    page when all questions have been answered"""

    responses.append(request.form["answer"])

    if len(responses) == len(survey.questions):
        return redirect('/thankyou')

    return redirect(f"/questions/{len(responses)}")


@app.get('/thankyou')
def thank_user():
    """thanks user for completing survey and shows responses"""

    return render_template("completion.html", questions=survey.questions, responses=responses)