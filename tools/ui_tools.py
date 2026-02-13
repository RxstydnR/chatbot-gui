from langchain_core.tools import tool
from typing import List

from pydantic import BaseModel, Field
from langgraph.types import Command, interrupt

class AskSingleChoiceArgs(BaseModel):
    question: str = Field(..., description="質問文")
    options: List[str] = Field(..., description="選択肢のリスト")
    allow_other: bool = Field(False, description="'その他'を許可するか")

@tool(
    description="ユーザーに1つだけ選択肢を選ばせる(radioボタン)。'その他'が必要な場合はallow_otherをTrueにする。",
    args_schema=AskSingleChoiceArgs,
)
def ask_single_choice(question: str, options: List[str], allow_other: bool = False):
    pass



class AskMultipleChoiceArgs(BaseModel):
    question: str = Field(..., description="質問文")
    options: List[str] = Field(..., description="選択肢のリスト")
    allow_other: bool = Field(False, description="'その他'を許可するか")

@tool(
    description="ユーザーに複数選択をさせる(checkbox)。'その他'が必要な場合はallow_otherをTrueにする。",
    args_schema=AskMultipleChoiceArgs,
)
def ask_multiple_choice(question: str, options: List[str], allow_other: bool = False):
    # human_response = interrupt({"query": question})
    # print(human_response)
    # return human_response["data"]
    pass



class AskFormInputArgs(BaseModel):
    question: str = Field(..., description="フォームのタイトル(質問文)")
    fields: List[str] = Field(..., description="入力項目名のリスト")

@tool(
    description="アカウント情報などの複数項目を一度に入力させる。fieldsは項目名のリスト。",
    args_schema=AskFormInputArgs,
)
def ask_form_input(question: str, fields: List[str]):
    pass



class AskDateInputArgs(BaseModel):
    question: str = Field(..., description="質問文")
    label: str = Field(..., description="日付入力のラベル")

@tool(
    description="日付を選択させる。", 
    args_schema=AskDateInputArgs
)
def ask_date_input(question: str, label: str):
    pass


UI_TOOLS = [
    ask_single_choice,
    ask_multiple_choice, 
    ask_form_input, 
    ask_date_input
    ]
