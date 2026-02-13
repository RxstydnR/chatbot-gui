MAIN_APP_CONTENTS_CSS = """
<style>

    /* アプリの幅 */
    .stAppViewBlockContainer {
            max-width: 80%;
    }

    /* 上部バーを透明に */
    header {
        background-color: transparent !important;
    }
        
    /* Streamlitコンテンツのスタイル調整 */
    .stApp {
        background: transparent !important;
    }
            
    .stAppViewMain {
        background-color: transparent !important;
    }
    .stMainBlockContainer {
        background-color: transparent !important;
        padding-top: 0rem; /* 上部の余白を削除 */
    }
    .stAppViewBlockContainer {
        background-color: transparent !important;
        padding-top: 0rem; /* 上部の余白を削除 */
    }
    
    /* フッターを透明に */
    footer {
        background-color: transparent !important;
    }

    /* チャットメッセージ内のすべてのテキスト要素を白色に */
    header,
    .stChatMessage p, 
    .stChatMessage span, 
    .stChatMessage div, 
    .stChatMessage h1, 
    .stChatMessage h2, 
    .stChatMessage h3, 
    .stChatMessage h4, 
    .stChatMessage h5, 
    .stChatMessage h6, 
    .stChatMessage li, 
    .stChatMessage a {
        color: rgba(0,0,0,0.95) !important;
    }
</style>
"""

# /* ヘッダーを非表示に */
# header {
#     visibility: hidden;
# } 

# チャット機能に関するCSS
CHAT_MESSAGE_CSS = """      
<style>                
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0) !important;
        margin: 10px 20px !important;
        border-radius: 20px !important;
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* ユーザーのアバターを非表示 */
    [data-testid="stChatMessageAvatarUser"] {
        display: none;
    }
    
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none;
    }
    
    .stChatInput {
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        background-color: #fff !important;
        color: #333;
        padding: 16px 10px !important;
    }

    .stChatInput *{
        border: none !important;
        background-color: #fff !important;
    }

    /* アイコンボタンっぽいものに適用するなら（例: 検索・音声） */
    .stChatInput button {
        border: none;
        border-radius: 50%;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        transition: background-color 0.2s;
        margin-right: .8em;
    }
    .stChatInput button:hover {
        background-color: #f0f0f0;
    }

    /* メッセージが表示されるときのアニメーション */
    @keyframes messageAppear {
        0% {
            opacity: 0;
            transform: translateY(12px) scale(0.98);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* すべてのメッセージ本文に適用（rerunのたびに再アニメーションされます） */
    [data-testid="stChatMessageContent"] {
        animation: messageAppear 0.01s ease-out both;
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
        margin-left: auto !important;
        background-color: rgba(30, 30, 30, 0.06) !important;
        border-radius: 15px !important;
        padding: 0.75rem 1rem !important;
        max-width: min(60%, 48rem);
        text-align: left;
        margin-right: .5rem !important;
    }

</style>
"""

# /* サイドバーのスタイリング */
SIDEBAR_CSS = """      
<style>                
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 250px;
        max-width: 250px;
    }
    [data-testid="stSidebar"] {
        background-color: rgb(240,244,250) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
"""