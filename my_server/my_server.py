from fastapi import FastAPI

from dotenv import load_dotenv

from langchain.output_parsers.enum import EnumOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from my_variables import MY_FOODS, Foods


load_dotenv()

app = FastAPI()


@app.get("/foods/{food}")
async def find_food(food: str):

    return MY_FOODS.get(food, "분류불가입니다.")


@app.get("/sentences/{sentence}")
def chat_bot(sentence: str):

    parser = EnumOutputParser(enum=Foods)

    prompt = PromptTemplate.from_template(
        """
        이제부터 너는 음식 추천가로써 문장의 내용을 보고 어떤 음식분류를 추천해주면 될지 말해줘. 분류 다음에 오는 분류중 하나를 골라서 말해줘.

        > 문장:{sentence}

        분류: {options}
    """
    ).partial(options=parser.get_format_instructions())
    model = ChatOpenAI()

    chain = prompt | model | parser

    res = chain.invoke({"sentence": sentence})

    return res.value
