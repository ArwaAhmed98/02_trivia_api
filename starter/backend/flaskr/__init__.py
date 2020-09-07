import os
from flask import Flask, request, abort, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


  #     '''
def create_app(test_config=None):
      
      #any changes to commit again
      
      
          
      # create and configure the app
      app = Flask(__name__)
      setup_db(app)
  
      CORS(app, resources={'/': {'origins': '*'}})
  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # # '''

  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''
      
            # here I am gonna implment pagination function for myself in order to call it  somewhere again and again
      def pagination(request,selection):

                  page=request.args.get('page',1,type=int)
                  start=(page-1)*QUESTIONS_PER_PAGE 
                  end= start +QUESTIONS_PER_PAGE
                  questions=[question.format() for question in selection]
                  current_Q=questions[start:end]
                  return current_Q
        
      @app.after_request
      def after_request(response):
            
            
            response.headers.add('Acess-Control-Allow-Headers' , 'Content-type' , 'Authorization','true')
            response.headers.add('Acess-Control-Allow-Methods' , 'GET,POST,PATCH,DELETE,OPTIONS')
            return response



  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
  # '''

  
  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
    # '''

      @app.route('/categories')
      def ret_all_avaiabe_categories():
            
          
            Catgreory =Category.query.order_by(Category.type).all()
            formatted_catg={Catg.id:Catg.type for Catg in Catgreory}
            
            if len(Catgreory) == 0: 
              
              abort(404) # WE DID NOT FIND ANY CATEGORY , 404 => NOT FOUND
            return jsonify({
              'success':True,
              # 'Categories':current_cat,
              #'total-Categories':len(Category.query.all()),
              'total-Categories':len(formatted_catg),
              'Categories':formatted_catg
            })
  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # '''
  
  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 
  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # QUESTIONS_PER_PAGE =10
# '''
      @app.route('/questions')
      def get_paginated_question():
            selection = Question.query.order_by(Question.id).all()
            current_Q= pagination(request,selection)
            if(len(current_Q)) == 0 :
                abort(404) # WE DID NOT FIND ANY Questions , 404=>NOT FOUND
            
          
            Catgreory =Category.query.order_by(Category.type).all()
            #make a dicionary and fills it with key and values of id and matching types 
            formatted_catg={Catg.id : Catg.type for Catg in Catgreory}
            
            return jsonify({
              'sucess':True,
              'questions':current_Q,
              'total_questions':len(Question.query.all()),
              'total_Categories':len(Category.query.all()),
              'current_Categories' : formatted_catg
            })
      @app.route('/questions/<int:question_id>',methods=['DELETE'])
      def DELETE_Q(question_id):
            
            try:
              
              x = Question.query.filter_by(Question.id == question_id).one_or_none()
              if x is None:
                    abort(404) #this id is not found so we cannot delete it ,,, 404=> NOT FOUND
              
              x.delete()
              return({
                'success':True,
                'ITEM-DELETED':question_id
              })
            except:
              abort(422)
  # '''

  # '''
  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  # '''
        
      @app.route('/questions' , methods=['POST'])
      def post_new_question():
            
              # Get item from the POST body
            req_data = request.get_json()
            
            requested_question = body.get('question')
            requested_answer = body.get('answer')
            requested_score = body.get('score')
            requested_category = body.get('category')
              
            # Get the response data
            Question(question=requested_question,
                    answer=requested_answer,
                    category=requested_category,
                    difficulty=requested_score
                    ).insert()
            
            # Return error if item not added
            if req_data is None:
                response = Response("{'error': 'Question is  not added - " + req_data + "'}", status=422
                                    , mimetype='application/json')
                return response #422  // Unprocessable Entity 
            else:
                  
                  
                  
                    
                # Return response  IF IT ADDED TRUELY 
                  return jsonify ({
                  'success':True,
                  'Questions':current_Q,
                  'total_Question':len(Question.query.all()),
                  'Question_added': Question.query.order_by(Question.id.desc()).first().format() })
                  #get the last record in the database by id 

  # '''
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
      # '''
        
      @app.route('/questions/search',methods=['POST','GET'])
      def search_for_Question():
            
            
            
            
            body=request.get_json()
            x=body.get('searchTerm')
            if x is None:
                  abort(422) # WE ARE NOT ABLE TO PROCESS THE REQUEST
            else:
                  #Search in our database with the sent search term
                  selection = Question.query.filter(Question.questions.ilike('%{}%'.f(search_term))).all()
                  if selection is None:
                        abort(404) #we did not find anything match this , 404 =>Not Found
                  else:      
                        current_Q= pagination(request,selection)
                        return jsonify({
                          'success':True,
                          'current_Questions':current_Q,
                          'total_Question' : len(Question.query.all())
                        })
                    

  # '''
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  # '''

      @app.route('/categories/<int:catg_id>/questions')
      def ret_Q_On_Catgoery(catg_id):
            
              #x = Question.query.filter(Question.id == question_id).one_or_none()
            catg = Catgreory.query.filter_by(catg_id == Catgreory.id ).one_or_none()
            if catg is None:
                  abort(404) #NOT FOUND 
            selection = Question.query.filter_by(catg==Category.id).all()
            curr_Q = paginate(request,selection)
            if len(curr_Q) == 0 :
                  abort(404) # WE DID NOT FIND ANY QUESTIONS
            return jsonify ({
              'sucess':True,
              'Questions':curr_Q,
              'total_Q':len(Question.query.all())
            })

  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  # '''

      @app.route('/quizzes' , methods = ['POST'])
      def get_Q_Play ():
            try:
              
                
              body = request.get_json()
              previous = body.get('previous_questions')
              category =body.get('quiz_category')
              if (previous or category is None): #if one of them or both is none , abort 422
                    abort(422) #WE ARE NOT ABLE TO PROCESS THE REQUEST
              if (category['id'] == 0 ):
                    Not_used_questions=Question.query.all() # if the user did not select any category 
              if  category['type'] == 'click' :
                    Not_used_questions = Question.query.filter(
                            Question.id.notin_((previous_questions))).all()
              else:
                    
              
                    Not_used_questions = Question.query.filter_by(
                            category=category['id']).filter(Question.id.notin_((previous_questions))).all()
                    random_question = random.choice(questions) #to generate a random question
                    new_question = Not_used_questions[random_question].format() if len(Not_used_questions) > 0 else None
                    #generate for me a random question that is not in the previous ones and filter by the selected catg_id 
                    #check if all the question have been used or not [[ at the end of the line]]
                    return jsonify({
                        'success': True,
                        'question': new_question
                    })
            
            except:
              
              abort(422)     
                  
  # '''
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  # # '''
      
      @app.errorhandler(404)
      def not_found(error):  
            return jsonify({
                "success": False, 
                "error": 404,
                "message": " Resource is Not found"
                }), 404
        
      @app.errorhandler(422)
      def unprocessable(error):
            
            
            return jsonify({
                "success": False, 
                "error": 422,
                "message": "We are not able to process the request"
                }), 422

      return app

      