from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from logger.logging import logger
from exception.exception_handling import CustomException
import sys

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global handler for CustomException
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"Unhandled application error: {exc}")
    return JSONResponse(status_code=500, content={"error": str(exc)})

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        logger.info(f"Received query: {query.question}")
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        logger.info(f"Graph saved to {os.path.abspath('my_graph.png')}")

        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        logger.info("Query processed successfully")
        return {"answer": final_output}
    except Exception as e:
        logger.exception("Error while processing /query")
        raise CustomException(e, sys)