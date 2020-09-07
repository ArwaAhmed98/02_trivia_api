import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:123@localhost:5432/trivia"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            #give the attribuites of the class any values
        self.new_Q={ 
            'question' : 'How are you ? ',
            'answer' : 'Fine,Thanks',
          'difficulty': 1,
            'category': '1'}
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
    
        res=self.client().get('/questions')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        
    def test_404_sent_requesting_beyond_valid_page(self):
        res=self.client().get('/questions?page=1000') 
         #Check that 404 not found will pop up for a fake data 
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'Resource is Not found')

    def test_ret_all_avaiabe_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        self.asserEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_categories'])
        self.assertTruedata['categories']
    def test_failure_ret_all_avaiabe_categories(self):
        res=self.client().get('/categories/20000000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] ,'Resource is Not found')

    def test_add_question(self):
        Q_Before = len(Question.query.all())
        response = self.client().post('/questions' , json=self.new_Q)
        data=json.loads(response.data)
        Q_after=len(Question.query.all())
    
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(Q_Before - Q_after == 1)
    def test_failure_add_Q(self):
        
    #   Q_Before = len(Question.query.all())
        response = self.client().post('/questions' , json={})
        data=json.loads(response.data)
    #   Q_after=len(Question.query.all())
    
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'unprocessable')

    def test_delete_Q(self):
        queston = self.new_Q
        queston.insert()
        q_id=queston.id
        
        response = self.client().post('/questions/{}'.format(q_id))
        data=json.loads(response.data)
        queston=Question.query.filter(Question.id == queston.id).one_or_none()
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],str(queston.id)) #cast the question id into string in order to compare  
        self.assertEqual(queston,None)
        #ensure that queston which is gonna be deleted is none 
    def delete_Non_existing_ques(self):
           
        response = self.client().post('/questions/{}')
        data=json.loads(response.data)
        
    
        self.assertEqual(response.status_code,422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'unprocessable')
        
    def test_search_q(self):
        
        response = self.client().post('/questions/search' , json={ 'searchTerm' : 'How are you ?'})
        data=json.loads(response.data)
        
    
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        # self.assertTrue(len (data['questions'] ) != 0) 
        self.assertNotEqual(data['questions'],0)
    def test_404_search(self):
        
        response = self.client().post('/questions/search' , json={'searchTerm' : ''})
        data=json.loads(response.data)
        
    
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'] , 'Resource is Not found')
    def test_get_Q_Catgeroy(self):
        
        response = self.client().get('/categories/2/questions' )
        
        response = self.client().post('/questions/search' , json={'searchTerm' : ''})
        data=json.loads(response.data)
        
    
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    def test_404_get_Q_Category(self):
        
        response = self.client().get('/categories/ANYTHING/questions' )
        data=json.loads(response.data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'] , 'bad request')
    def test_quiz(self):
        prev = {'previous_questions' : [] , 'quiz_category':{'type':'Sports','id':3}}
        response = self.client().get('/quizzes' , json = prev)
        data=json.loads(response.data)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        
    def test_404_quiz(self):
        
        prev = {'previous_questions' : []}
        #Only emptr prev quistion => throw error
        response = self.client().get('/quizzes' , json = prev)
        data=json.loads(response.data)
        
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'] , 'bad request')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()