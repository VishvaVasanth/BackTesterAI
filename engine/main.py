import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict

# Internal custom module imports
from parser import parse_strategy_rules
from backtester import run_vectorized_backtest

app = FastAPI()

# Switch to the free Groq environment configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

class BacktestPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    prompt: str
    ticker: str
    startDate: str = Field(..., alias="start_date")
    endDate: str = Field(..., alias="end_date")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("\n🚨 --- FAILED PAYLOAD VALIDATION LOG --- 🚨")
    print(f"Error Details: {exc.errors()}")
    print("-----------------------------------------\n")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "message": "Payload format mismatched Pydantic schema validation inputs."}
    )


@app.post("/api/v1/backtest")
async def process_backtest(payload: BacktestPayload):
    try:
        # Pass the Groq API key downward instead of OpenAI
        structured_strategy = parse_strategy_rules(payload.prompt, GROQ_API_KEY)

        structured_strategy.ticker = payload.ticker

        results = run_vectorized_backtest(
            structured_strategy,
            payload.startDate,
            payload.endDate
        )
        return results
    except Exception as e:
        print("\n💥 --- PYTHON ENGINE CRASH STACK TRACE --- 💥")
        traceback.print_exc()
        print("-------------------------------------------\n")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)