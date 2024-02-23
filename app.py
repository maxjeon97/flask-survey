from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSE_KEY = "response"

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



@app.get("/")
def start_survey():
    """Generates start page for survey"""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """Redirects to first question page upon pressing start button"""

    session[RESPONSE_KEY] = []

    return redirect("/questions/0")


@app.get("/questions/<int:number>")
def handle_question(number):
    """displays question based on its url parameter number"""

    responses = session.get(RESPONSE_KEY)

    if responses is None:
        return redirect("/")

    if len(responses) == len(survey.questions):
        flash("You already completed this survey!")
        return redirect('/thank-you')

    if number != len(responses):
        flash("Answer the questions in order!")

        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[number]
    return render_template("question.html", question=question)


@app.post("/answer")
def handle_answer():
    """handles question submission, redirects to thank you
    page when all questions have been answered"""

    responses = session[RESPONSE_KEY]
    responses.append(request.form["answer"])
    session[RESPONSE_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thank-you')

    return redirect(f"/questions/{len(responses)}")


@app.get('/thank-you')
def thank_user():
    """thanks user for completing survey and shows responses"""

    responses = session.get(RESPONSE_KEY)

    if responses is None:
        flash("You haven't answered any of the questions!")
        return redirect("/")

    if len(responses) != len(survey.questions):
        flash("You haven't completed the survey!")
        return redirect(f"/questions/{len(responses)}")

    return render_template("completion.html", questions=survey.questions, responses=responses)