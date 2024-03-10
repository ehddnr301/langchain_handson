from fastapi import FastAPI, Depends

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI()


@app.get("/sentences/{sentence}")
def chat_bot(sentence: str):
    prompt = PromptTemplate.from_template(
        """
        이제부터 너는 음식 추천가로써 문장의 내용을 보고 어떤 음식분류를 추천해주면 될지 말해줘 한식, 중식, 일식, 패스트푸드 중 하나를 골라줘.

        > 문장:{sentence}
    """
    )
    model = ChatOpenAI()

    chain = prompt | model

    res = chain.invoke({"sentence": sentence})

    return res.content
