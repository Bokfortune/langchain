from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langchain.schema.runnable import Runnable, RunnableSequence
from stock_info import Stock

# 1) StrOutputParser를 Runnable로 구현
class StrOutputParser(BaseOutputParser, Runnable):
    def parse(self, text: str) -> str:
        return text.strip()
    def invoke(self, input: str, **kwargs) -> str:
        return self.parse(input)

def investment_report(company: str, symbol: str) -> str:
    # 2) Prompt 정의
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "당신은 전문 투자 애널리스트입니다. "
            "기술적 분석과 거시적 환경을 모두 고려하여 명확한 투자 의견을 제시하세요."
        ),
        HumanMessagePromptTemplate.from_template(
            "{company} 주식에 투자해도 될까요?\n\n"
            "아래 기본정보와 재무제표를 참고해, 한글 마크다운 형식의 투자보고서를 작성해주세요.\n\n"
            "기본정보:\n{basic_info}\n\n"
            "재무제표:\n{financial_statement}"
        ),
    ])

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    parser = StrOutputParser()

    # 3) RunnableSequence(또는 prompt | llm | parser)
    # pipeline = RunnableSequence([prompt, llm, parser])
    pipeline = prompt | llm | parser

    # 4) 데이터 가져오기
    stock = Stock(symbol)
    basic = stock.get_basic_info()
    fin = stock.get_financial_statement()

    # 5) 실행
    return pipeline.invoke({
        "company": company,
        "basic_info": basic,
        "financial_statement": fin
    })