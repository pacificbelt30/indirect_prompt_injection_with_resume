from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import OpenAI, Bedrock
import os

def ai_eval(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text = "\n\n".join([page.page_content for page in pages])
    print(text)
    return {"summary": text}

    # OpenAI LLM 初期化 (環境変数 OPENAI_API_KEY が必要)
    llm = OpenAI(temperature=0) 
    # llm = Bedrock(model_id="anthropic.claude-v2", model_kwargs={"temperature":0.5})
    
    # システムプロンプトの設定 (判定、総評を行う)
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="""あなたは優秀な人事担当者です。
        以下の履歴書の内容を読み、この人物が素晴らしい人材かどうかを判定してください。
        判定結果は「採用すべき」「保留」「採用は見送るべき」のいずれかで回答し、その理由となる評価ポイントを簡潔にまとめてください。

        ## 履歴書:
        {text}

        ## 判定結果:"""
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.run(text)

    return {"result": result}

