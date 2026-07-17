import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

# 1. Define the structural output schema the backtester engine expects
class TradingStrategy(BaseModel):
    ticker: str = Field(description="The stock or crypto ticker symbol, upper-case (e.g. AAPL, BTC-USD)")
    indicator_1: str = Field(description="The primary technical indicator (e.g. SMA_50, EMA_20, RSI)")
    indicator_2: str = Field(description="The secondary technical indicator or condition (e.g. SMA_200, price, value_30)")
    condition: str = Field(description="The execution trigger rule logic (e.g. crosses_above, crosses_below, greater_than, less_than)")

def parse_strategy_rules(user_prompt: str, api_key: str) -> TradingStrategy:
    """
    Leverages a free Groq LLM model via LangChain to convert a natural language
    trading string into a structured data model layout for backtesting equations.
    """
    # 2. Instantiate the pure Groq client instance mapping
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key,
        temperature=0.0
    )

    # 3. Set up the output validator schema structural configurations
    parser = PydanticOutputParser(pydantic_object=TradingStrategy)

    # 4. Craft explicit template rules instructing the model on constraints
    template = """
    You are an expert algorithmic trading system parser.
    Your task is to convert plain-English trading strategies into a structured layout parameters JSON object.

    User Rule input: {input}

    Formatting Instructions:
    {format_instructions}

    Provide ONLY raw JSON code output matching schema properties. Do not reply with regular conversational text introduction metadata wrapper blocks.
    """

    prompt = ChatPromptTemplate.from_template(
        template=template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 5. Build and execute the functional compiler chain line
    chain = prompt | llm | parser
    return chain.invoke({"input": user_prompt})