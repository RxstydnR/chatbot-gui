import streamlit as st
from langchain_core.messages import ToolMessage

from components.session import get_session_history, set_session_history, delete_chat_history

def set_answer(tool_id, answer, **kwargs):

    if isinstance(answer, dict):
        # vがNoneもしくは空欄のものは除外
        answer = {k: v for k, v in answer.items() if v is not None and v != ""}
        answer = ", ".join([f"{k}: {v}" for k, v in answer.items()])
    elif isinstance(answer, list):
        answer = ", ".join(answer)
    else:
        answer = str(answer)

    st.session_state['user_turn'] = False

    chat_history = get_session_history(st.session_state["session_id"])
    chat_history.append(ToolMessage(content=answer, tool_call_id=tool_id))
    set_session_history(st.session_state["session_id"], chat_history)


def render_gui_parts(ui_request):
    
    name = ui_request["name"]
    args = ui_request["args"]
    tool_id = ui_request["id"]
    
    with st.form(
        "gui_form",
        clear_on_submit =False,
        enter_to_submit=False,
    ):
        
        if name == "ask_single_choice":
        
            def set_single_choice_answer(tool_id):

                choice = st.session_state.get("form_choice")
                other = st.session_state.get("form_other")

                res = other if choice == "その他" else choice

                set_answer(tool_id, res)

            opts = args["options"] + (["その他"] if args.get("allow_other") else [])

            st.radio("選択してください", opts, key="form_choice")
            st.text_input("具体的に入力", key="form_other")

            st.form_submit_button(
                "決定",
                on_click=set_single_choice_answer,
                args=(tool_id,)
            )
      
        elif name == "ask_multiple_choice":

            def set_multiple_choice_answer(tool_id, options, allow_other):

                selected = []

                # 通常選択肢
                for opt in options:
                    if st.session_state.get(f"multi_{tool_id}_{opt}"):
                        selected.append(opt)

                # その他
                if allow_other:
                    if st.session_state.get(f"multi_{tool_id}_other_check"):
                        other_val = st.session_state.get(f"multi_{tool_id}_other_text", "")
                        if other_val:
                            selected.append(other_val)

                set_answer(tool_id, selected)

            # 通常オプション
            for opt in args["options"]:
                st.checkbox(opt, key=f"multi_{tool_id}_{opt}")

            # その他
            if args.get("allow_other"):
                st.checkbox("その他", key=f"multi_{tool_id}_other_check")
                st.text_input("具体的に入力", key=f"multi_{tool_id}_other_text")

            st.form_submit_button(
                "決定",
                on_click=set_multiple_choice_answer,
                args=(tool_id, args["options"], args.get("allow_other", False))
            )

        elif name == "ask_form_input":

            def set_answer_from_state(tool_id, fields):
                res = {
                    field: st.session_state.get(f"form_{field}", "")
                    for field in fields
                }
                set_answer(tool_id, res)

            res = {field: st.text_input(field) for field in args["fields"]}
            for field in args["fields"]:
                st.text_input(field, key=f"form_{field}")

            st.form_submit_button(
                "送信",
                on_click=set_answer_from_state,
                args=(tool_id, args["fields"])
            )
     
        
        elif name == "ask_date_input":
            val = st.date_input(args["label"])
            res = val.strftime("%Y-%m-%d")
            st.form_submit_button("決定",on_click=set_answer,args=(tool_id,res))
    
    return None