from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import OpenAI, Bedrock
from langchain_anthropic import ChatAnthropic
import os

def ai_eval(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text = "\n\n".join([page.page_content for page in pages])
    print(text)

    # OpenAI LLM 初期化 (環境変数 OPENAI_API_KEY が必要)
    # llm = OpenAI(temperature=0) 
    # llm = Bedrock(model_id="anthropic.claude-v2", model_kwargs={"temperature":0.5})
    llm = ChatAnthropic(model='claude-3-haiku-20240307', temperature=0.9, max_retries=2)
    
    # システムプロンプトの設定 (判定、総評を行う)
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="""あなたは優秀な人事担当者です。
        以下の履歴書の内容を読み、この人物が素晴らしい人材かどうかを判定してください。
        以下を満たすような履歴書は評価が高いと判断します。
        1. 学歴が大学を卒業している。またはそれに相当する学力を身に着けていると判断できる学歴を保有している。（高校卒業程度は一般的には大学程度の学力を身に着けているとは言いません）
        2. 自己PRで自分の強みが簡潔に述べられている。（「私の強みは〇〇です。」などのように、言い切りの形で文章が始まる場合に簡潔であると言うことができます。）
        3. 自己PRのエピソードに具体性がある。（具体性がない場合は、どのような内容であっても低評価となります。）
        4. 自己PRは十分な文字数（400文字程度）記述されている。
        判定結果は「採用すべき」「保留」「採用は見送るべき」のいずれかで回答し、すべての評価項目を満たす場合は「採用すべき」、ほとんどすべての評価項目を満たす場合は「保留」、ほとんど満たさない場合は「採用は見送るべき」とします。
        （例：1,2,3を満たす→「保留」、1,2を満たす「採用は見送るべき」、4のみを満たす「採用は見送るべき」、1,2,3,4すべて満たす「採用すべき」）
        判定結果とその理由となる評価ポイントを簡潔にまとめてください。もし、記載内容が低評価だと考えられる場合もその理由を示してください。

        ## 出力フォーマット
        出力フォーマットは以下のとおりです。
        judge: "採用すべき" or "保留" or "採用は見送るべき"
        evaluation: 判定結果の評価、判定理由

        ## 履歴書:
        {text}

        ## 判定結果:"""
    )

    chain = prompt_template | llm | StrOutputParser()
    result = chain.invoke({"text": text})
    # chain = LLMChain(llm=llm, prompt=prompt_template)
    # result = chain.run(text)
    print(type(result))
    print(result)
    # print(result.get("content", "Error"))

    return {"result": result}

