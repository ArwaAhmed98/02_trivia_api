import os
from flask import Flask, request, abort, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


  #     '''
def create_app(test_config=None):

      # create and configure the app
      app = Flask(__name__)
      setup_db(app)
  
      CORS(app, resources={'/': {'origins': '*'}})

      
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
            
            response.headers.add('Access-Control-Allow-Headers','Content-Type,authorization,True')
            response.headers.add('Acess-Control-Allow-Methods' , 'GET,POST,PATCH,DELETE,OPTIONS')
            return response


      @app.route('/categories')
      def ret_all_avaiabe_categories():
            
          
            Catgreory =Category.query.order_by(Category.type).all()
            formatted_catg={Catg.id:Catg.type for Catg in Catgreory}
            
            if len(Catgreory) == 0: 
              
              abort(404) # WE DID NOT FIND ANY CATEGORY , 404 => NOT FOUND
            return jsonify({
              'success':True,
              'categories':formatted_catg
            })
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
              'categories' : formatted_catg
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
                'deleted':question_id
              })
            except:
              abort(422)
    
      @app.route('/questions' , methods=['POST'])
      def post_new_question():
            
              # Get item from the POST body
            body = request.get_json()
            
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
            if body is None:
                response = Response("{'error': 'Question is  not added - " + body + "'}", status=422
                                    , mimetype='application/json')
                return response #422  // Unprocessable Entity 
            else:
                  
                  
                  
                    
                # Return response  IF IT ADDED TRUELY 
                  return jsonify ({
                  'success':True,
                  'questions':current_Q,
                  'total_questions':len(Question.query.all()),
                  'question_created': Question.query.order_by(Question.id.desc()).first().format(),
                  'question_created': Question.query.first().format()
                   })
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
                          'questions':current_Q,
                          'total_questions' : len(Question.query.all())
                        })
      

      @app.route('/categories/<int:catg_id>/questions')
      def ret_Q_On_Catgoery(catg_id):
            casted=str(catg_id)
            #cast the function parameter to string to compare and filter
            questions=Question.query.filter(Question.category == casted).all 
           
            return jsonify ({
              'sucess':True,
              'questions': [question.format() for question in questions], #return e a lit of questions and format 
              'total_questions':len(questions),
              'current_category': catg_id # the parameter of the function as we choose by the category id
            })

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
                    #generate    for me a random question that is not in the previous ones and filter by the selected catg_id 
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

      