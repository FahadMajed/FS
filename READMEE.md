# Trivia API Project - Udacity
 
## Full Stack API Final Project
The trivia is a game that allow users to test their knowledge by playing a simple game of randomized questions. The goal of this project is to structure plan, implement, and test the API to Complete the trivia app. where the application must meet the following requirements:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

All backend codes follow [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)
## Getting Started
### Dependencies Installation:
Developers using this project should have Python3, pip3, nodeJS, and npm installed.

#### Installing Backend dependencies:
first create a virtual environment "when using Python for this projects". Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
This will install all the required packages we selected within the `requirements.txt` file.

#### Installing Frontend dependencies:
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Running the Server
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
## Running the Frontend
The frontend app was built using create-react-app. To run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

```bash
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

## APIs Testing:
To TEST the API End points, run the following commands:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Skip "dropdb trivia_test" command for the first time running the test.

# Reference
## Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, (http://127.0.0.1:5000/), which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
   'success': False,
   'error': 404,
   'message': 'Resource Not Found'
}
```

The API will return Three error types when requests fail:
* 404: Resource Not Found
* 422: Unprocessable
* 400: Bad request


## Endpoints
### GET /categories
* General:
  - Returns a list of categories with thier corresponding id's, and the success value 
* Sample:
  - curl http://127.0.0.1:5000/categories
```
{
  '1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"
}
```

### GET /questions
* General:
  - returns list of questions along side a list of the questions categories and total number of questions.
  - Results are paginated in groups of 10 Questions per page. 
* Sample:
  - curl http://127.0.0.1:5000/questions
```
{
  "categories":
  {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
   },
   "questions": [
   {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
     "answer": "Tom Cruise",
     "category": 5,
     "difficulty": 4,
     "id": 4,
     "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
     "answer": "Maya Angelou",
     "category": 4,
     "difficulty": 2,
     "id": 5,
     "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
     "answer": "Edward Scissorhands",
     "category": 5,
     "difficulty": 3,
     "id": 6,
     "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
     "answer": "Muhammad Ali",
     "category": 4,
     "difficulty": 1,
     "id": 9,
     "question": "What boxer's original name is Cassius Clay?"
    },
    {
     "answer": "Brazil",
     "category": 6,
     "difficulty": 3,
     "id": 10,
     "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
     "answer": "Uruguay",
     "category": 6,
     "difficulty": 4,
     "id": 11,
     "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
     "answer": "George Washington Carver",
     "category": 4,
     "difficulty": 2,
     "id": 12,
     "question": "Who invented Peanut Butter?"
    },
    {
     "answer": "Lake Victoria",
     "category": 3,
     "difficulty": 2,
     "id": 13,
     "question": "What is the largest lake in Africa?"
    },
    {
     "answer": "The Palace of Versailles",
     "category": 3,
     "difficulty": 3,
     "id": 14,
     "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
     "answer": "Saudi Arabia",
     "category": 3,
     "difficulty": 3,
     "id": 26,
     "question": "What is the only country with a coastline on both the Red Sea and the Persian Gulf?"
    }
],
"success": true,
"total_questions": 21
}
```

## DELETE /questions/<int:question_id>
* General:
  - returns the deleted quesiton id and the success value. 
* Sample:
  - curl -X DELETE http://127.0.0.1:5000/questions/10
  
```
  {
  "deleted": 6,
 ,
  "success": true
  
}
```
  
### POST /questions
- endpoint to POST a new question which will require the question and answer text, category, and difficulty score. 
* General:
  - Creates a new question using JSON request
  - Returns the new question ID and the success value
* Sample:
  - curl -X POST -H "Content-Type: application/json" -d '{ "question": "What is the national day of KSA?", "answer": "23th September", "difficulty": 1, "category": "4" }' http://127.0.0.1:5000/questions
```
 {
 "created": 22,
  "success": true
  
}
```

## POST /questions/search
* General:
  - Searches for questions using search term in JSON format
  - Returns object with matching questions.
* Sample:
  - curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "what"}' http://127.0.0.1:5000/questions/search
```
{
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Saudi Arabia",
      "category": 3,
      "difficulty": 3,
      "id": 26,
      "question": "What is the only country with a coastline on both the Red Sea and the Persian Gulf?"
    }
  ],
  "success": true,
 
}
```
## Get /categories/<int:category_id>/questions
* General:
  - retrieves questions by category id using url parameters.
  - Returns an object with paginated matching questions
* Sample:
  - curl http://127.0.0.1:5000/categories/3/questions
```
{
  "Success": true,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Saudi Arabia",
      "category": 3,
      "difficulty": 3,
      "id": 26,
      "question": "What is the only country with a coastline on both the Red Sea and the Persian Gulf?"
    }
  ],
 
}
```

## POST /quizzes
* General: 
  - An endpoint to get questions to play the quiz.
  - Takes category and previous question parameters
  - Return a random question within the given category, if provided, and that is not one of the previous questions.
* Sample:
  - curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Geography", "id": "3"}}' http://127.0.0.1:5000/quizzes
```
{
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}
```

# Deployment N/A

# Authors
Fahad Al Hssan
