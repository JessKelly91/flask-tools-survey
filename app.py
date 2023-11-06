from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


responses = []

@app.route('/')
def show_start():
   """
   Show survey title/instructions/start button
   Start button will reroute to survey questions
   """

   return render_template('start.html', survey = satisfaction_survey)

@app.route('/start_survey')
def start_survey():
   """Clear current responses and redirect to first question"""

   responses = []

   return redirect("/questions/0")
    

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def show_questions(question_id):
   """retrieves questions from survey instance and displays current question on screen
   """
   #handle the click of continue button
   if request.method == "POST":
      #append the current answer to the responses list
      if question_id < len(satisfaction_survey.questions):
         answer = request.form['answer']
         responses.append(answer)

         #go to next question
         question_id += 1 
         return redirect(f'/questions/{question_id}')

   #make sure question_id is within valid range + display
   if 0 <= question_id < len(satisfaction_survey.questions):
      question = satisfaction_survey.questions[question_id]
      return render_template('questions.html', question = question, question_id = question_id, survey = satisfaction_survey)
   elif question_id >= len(satisfaction_survey.questions):
      return redirect("/thanks")

@app.route('/thanks')
def complete_survey():
   """Show thank you page."""

   return render_template("thanks.html", survey = satisfaction_survey)