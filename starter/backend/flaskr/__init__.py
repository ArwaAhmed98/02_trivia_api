import os
from flask import Flask, request, abort, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
QUESTIONS_PER_PAGE = 10
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
            response.headers.add('Acess-Control-Allow-Headers' , 'Content-Type,Authorization,true')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
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
                  'questions':current_Q,
                  'total_questions':len(Question.query.all()),
                  'question_created': Question.query.order_by(Question.id.desc()).first().format() })
                  #get the last record in the database by id  
      @app.route('/questions/search',methods=['POST','GET'])
      def search_for_Question():
            body=request.get_json()
            x=body.get('searchTerm')
            if x is None:
                  abort(422) # WE ARE NOT ABLE TO PROCESS THE REQUEST
            
            selection = Question.query.filter(Question.questions.ilike('%{}%'.f(search_term))).all()
                  #Search in our database with the sent search term
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
              'questions':curr_Q,
              'total_questions':len(Question.query.all())
            })
      @app.route('/quizzes' , methods = ['POST'])
      def get_Q_Play ():
            try:
              body = request.get_json()
              previous = body.get('previous_questions')
              category =body.get('quiz_category')
              if (previous or category is None): #if one of them or both is none , abort 422
                    abort(422) #WE ARE NOT ABLE TO PROCESS THE REQUEST
              if  category['type'] == 'click' :
                    available_questions = Question.query.filter(
                            Question.id.notin_((previous_questions))).all()
              else:
                    available_questions = Question.query.filter_by(
                            category=category['id']).filter(Question.id.notin_((previous_questions))).all()
                    random_question = random.choice(questions) #to generate a random question
                    new_question = available_questions[random_question].format() if len(available_questions) > 0 else None
                    return jsonify({
                        'success': True,
                        'question': new_question
                    })
            except:
              abort(422)     
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
      @app.errorhandler(500)
      def unprocessable(error):
            return jsonify({
                "success": False, 
                "error": 500,
                "message": "Internal server error"
                }), 500
      @app.errorhandler(400)
      def unprocessable(error):      
            return jsonify({
                "success": False, 
                "error": 400,
                "message": "Bad request"
                }), 400
      return app

      