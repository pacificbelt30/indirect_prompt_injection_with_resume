from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import aiofiles  # 非同期ファイル読み込み用

# AI処理を行う関数を仮定 (別ファイルで定義)
from functions.ai_processing import ai_eval 

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/analyze_pdf")
# @app.get("/api/analyze_pdf")
async def analyze_pdf(pdf: Optional[UploadFile] = None):
    try:
        # PDFファイルを一時保存 (メモリ上で処理する場合は不要)
        async with aiofiles.open(pdf.filename, 'wb') as out_file:
            content = await pdf.read()
            await out_file.write(content)

        # AI処理を実行 (pdf.filename を渡す)
        result = ai_eval(pdf.filename)
        return JSONResponse({
            "result": "要約ですー",
            "evaluation": "eval"
        })

        return JSONResponse({
            "result": result.get("result", "判定結果を取得できませんでした。"),
            "evaluation": result.get("evaluation", "総評を取得できませんでした。")
        })

    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return JSONResponse({"error": str(e)}, status_code=500)

    finally:
        # 一時ファイルを削除 (メモリ上で処理する場合は不要)
        import os
        os.remove(pdf.filename)

