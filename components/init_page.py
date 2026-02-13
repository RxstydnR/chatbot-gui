import streamlit as st

SUGGESTIONS = {
    ":green[:material/receipt_long:] 確定申告の方法がわからない。": (
        "確定申告の方法がわかりません。会社員/自営業、収入の種類、控除、必要書類、提出方法（e-Tax/郵送/窓口）を前提に、手順をわかりやすく教えてください。"
    ),
    ":orange[:material/work:] 私に向いてる職業に転職したい。": (
        "私に向いてる職業に転職したいです。これまでの経験、得意不得意、価値観、希望条件を質問して、向いている職種候補と次のアクション（スキル・資格・職務経歴書）を提案してください。"
    ),
    ":violet[:material/school:] 何か習い事を始めたい。": (
        "何か習い事を始めたいです。目的（健康/趣味/仕事/交流）、予算、頻度、場所（オンライン/通学）、性格を聞いて、候補をいくつか提案してください。"
    ),
    ":red[:material/psychology:] 最近やる気が出ない。": (
        "最近やる気が出ません。生活リズム、ストレス要因、体調、目標の有無を確認して、無理のない改善策と小さな行動プランを提案してください。"
    ),
    ":blue[:material/travel_explore:] 旅行先で食べたフルーツが何だったか思い出したい。": (
        "旅行先で食べたフルーツが何だったか思い出したいです。覚えている特徴（見た目・色・味・食感・種の有無・香り・売られていた場所/国）から候補を絞ってください。"
    ),
}

@st.dialog("アプリ概要（GUI誘導型AIチャットボット）", width="small")
def show_disclaimer_dialog():
    st.caption("""
            このアプリは、Streamlit上で動作するGUI誘導型のAIチャットボットです。
            LangGraph/LangChainのエージェントが、選択肢や日付入力などのUIツールを通じて対話を進めます。
            会話履歴はセッション単位で管理され、画面にチャット形式で表示されます。
            サイドバーから履歴の削除やセッションの初期化が可能です。
        """)


def render_init_page():

    title_row = st.container(
        horizontal=False,
        horizontal_alignment="center",
        # vertical_alignment="bottom",
    )
    with title_row:
        st.space("large")
        st.image("https://streamlit.io/images/brand/streamlit-mark-dark.png",width=100)
        st.title(
            # ":material/cognition_2: Streamlit AI assistant", anchor=False, width="stretch"
            "AI assistant with GUI tools.",
            anchor=False,
            width="stretch",
            text_alignment="center",
        )

    with st.container():
        
        st.chat_input("Ask a question...", key="initial_question")

        st.pills(
            label="Examples",
            label_visibility="collapsed",
            options=SUGGESTIONS.keys(),
            key="selected_suggestion",
        )

        st.button(
            ":small[:gray[:material/app_registration: アプリ概要]]",
            type="tertiary",
            on_click=show_disclaimer_dialog,
        )