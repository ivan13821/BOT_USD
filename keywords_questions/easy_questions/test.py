from keywords_questions.easy_questions.main import EasyQuestions
from fastapi import FastAPI
from pydantic import BaseModel


router = FastAPI()



class Question(BaseModel):
   question: str






@router.get("/get/")
async def home(question: Question):
   
   answer = EasyQuestions.generate_easy_answer(question.question)
   
   return answer