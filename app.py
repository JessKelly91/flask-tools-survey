from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def show_start():
   """
   Show survey title/instructions/start button
   Start button will reroute to survey questions
   """

   return render_template('start.html', survey = satisfaction_survey)

@app.route('/start_survey', methods=["POST"])
def start_survey():
   """Clear current responses and redirect to first question"""

   session[RESPONSES_KEY] = []

   return redirect("/questions/0")

@app.route('/answer', methods=["POST"])
def handle_responses():
   """Saves responses and redirects to next questions/thank you page"""

   #extract answer from form
   answer = request.form['answer']
   
   #add answer to session
   responses = session[RESPONSES_KEY]
   responses.append(answer)
   session[RESPONSES_KEY] = responses

   if (len(responses) == len(satisfaction_survey.questions)):
      #survey is complete
      return redirect('/thanks')
   else:
      #otherwise move to next question
      return redirect(f'/questions/{len(responses)}')

   

@app.route('/questions/<int:question_id>')
def show_questions(question_id):
   """retrieves questions from survey instance and displays current question on screen
   """
   responses = session.get(RESPONSES_KEY)

   if (responses is None):
      #accessing page too soon
      return redirect('/')

   if question_id != len(responses):
      #trying to access questions out of order
      flash('Please complete the survey questions in order.')
      
      return redirect(f'/questions/{len(responses)}')
   
   if (len(responses) == len(satisfaction_survey.questions)):
      #survey is complete
      return redirect('/thanks')
   
   question = satisfaction_survey.questions[question_id]

   return render_template('questions.html', question_num = question_id, question = question, survey = satisfaction_survey)

@app.route('/thanks')
def complete_survey():
   """Show thank you page."""

   return render_template("thanks.html", survey = satisfaction_survey)