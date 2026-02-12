from typing import Annotated, Optional, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    # 履歴を保持。add_messagesによりリストが自動更新される
    messages: Annotated[list, add_messages]
    # 現在アクティブなUIリクエスト（Tool Callオブジェクト）を保持
    # ui_request: Optional[dict]