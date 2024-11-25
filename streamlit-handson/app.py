import streamlit as st
import json
import pyperclip
import time

st.write("proposal recommneder")

# JSONファイルから提案データを読み込む
with open('proposals.json', 'r', encoding='utf-8') as f:
    proposals = json.load(f)

# 提案結果を保存するリスト
if "results" not in st.session_state:
    st.session_state.results = []

# 現在の表示状態を管理する変数
if "current_proposal" not in st.session_state:
    st.session_state.current_proposal = 0

# 現在の提案を表示
if st.session_state.current_proposal < len(proposals):

    # 進捗バーを表示
    progress_value = (st.session_state.current_proposal + 1) / len(proposals) 
    st.progress(progress_value)

    proposal = proposals[st.session_state.current_proposal]

    # カード形式で表示
    with st.expander(proposal["company"], expanded=True):  # 常に展開
        # st.write(proposal["text"])
        st.text_area("Recommendation:", proposal["text"], height=300, key=f"text_{st.session_state.current_proposal}")  # st.text_area を使用

        # 提案するかしないかの選択
        col1, col2 = st.columns(2)  # 2つのカラムを作成
        with col1:
            choice = st.radio(
                "提案しますか？",
                ("はい", "いいえ"),
                key=f"proposal_{st.session_state.current_proposal}",
                help="はいを選択すると文面がコピーされます",  # help引数を追加
            )

        # いいえを選択した場合、理由を入力するテキストエリアを表示
        # 理由入力
        with col2:
            if choice == "いいえ":
                reason = st.selectbox(  # selectboxに変更
                    "理由",
                    ("的外れ", "時期尚早", "交渉不可", "その他"),
                    key=f"reason_{st.session_state.current_proposal}",
                )
                if reason == "その他":  # 「その他」を選択した場合のみテキスト入力
                    reason = st.text_input(
                        "その他の理由", key=f"other_reason_{st.session_state.current_proposal}"
                    )
            elif choice == "その他":  # 「その他」を選択した場合のみテキスト入力
                reason = st.text_input("理由", key=f"reason_{st.session_state.current_proposal}")
            else:
                reason = ""
        
        # 確定ボタン
        if st.button("確定", key=f"confirm_{st.session_state.current_proposal}"):
            # 結果をリストに追加
            st.session_state.results.append({"company": proposal["company"], "choice": choice, "reason": reason})
            if choice == "はい":
                pyperclip.copy(proposal["text"])
            # 次の提案へ
            st.session_state.current_proposal += 1
            
            # JavaScriptを実行してスクロール位置をトップに戻す
            st.components.v1.html(
                """
                window.scrollTo(0, 0);
                """
            )
            time.sleep(1)
            st.rerun()

# 全ての提案が完了したら結果を表示
if st.session_state.current_proposal == len(proposals):
    st.header("入力結果")
    st.write("入力ありがとうございます")
    for result in st.session_state.results:
        st.write(f"{result['company']}：{result['choice']}")
        if result["reason"]:
            st.write(f"  理由：{result['reason']}")
