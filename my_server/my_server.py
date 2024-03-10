from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from langchain.output_parsers.enum import EnumOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.docarray import DocArrayInMemorySearch
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from my_variables import MY_FOODS, Foods
from db import SessionLocal, engine, Base
from models import UserAnswerTable

load_dotenv()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/foods/{food}")
async def find_food(food: str):

    return MY_FOODS.get(food, "분류불가입니다.")


@app.get("/sentences/{sentence}")
def chat_bot(sentence: str, db: Session = Depends(get_db)):
    is_good_data = UserAnswerTable.get_is_good(db, 1)
    vectorstore = DocArrayInMemorySearch.from_texts(
        (
            [
                f"문장: {r.__dict__['sentence']} / {r.__dict__['recommended_foodtype']}"
                for r in is_good_data
            ]
            if is_good_data
            else ["문장: 따뜻한 국물요리가 먹고싶어 / 한식"]
        ),
        embedding=OpenAIEmbeddings(),
    )
    retriever = vectorstore.as_retriever()

    parser = EnumOutputParser(enum=Foods)

    prompt = PromptTemplate.from_template(
        """
        이제부터 너는 음식 추천가로써 문장의 내용을 보고 어떤 음식분류를 추천해주면 될지 {context}를 참고하여 말해줘. 목록중 하나를 골라서 말해줘.

        > 문장:{sentence}

        목록: {options}
    """
    ).partial(options=parser.get_format_instructions())

    model = ChatOpenAI(model="gpt-4")

    setup_and_retrieval = RunnableParallel(
        {"context": retriever, "sentence": RunnablePassthrough()}
    )

    chain = setup_and_retrieval | prompt | model | parser

    res = chain.invoke(sentence)

    return res.value


@app.get("/satisfy")
def satisfy(
    is_good: int,
    sentence: str,
    recommended_foodtype: str,
    db: Session = Depends(get_db),
):
    user_answer = UserAnswerTable(
        is_good=is_good,
        sentence=sentence,
        recommended_foodtype=recommended_foodtype,
    )
    db.add(user_answer)
    db.commit()
    db.refresh(user_answer)
    return user_answer
