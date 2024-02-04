from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from schemas import Question, Response
from src import ai_translate_question_to_sql

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.post("/question", response_model=Response)
async def process_user_question(question: Question):
    response = ai_translate_question_to_sql(question.question)
    if not response:
        raise HTTPException(status_code=400, detail="Invalid query or database error.")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)