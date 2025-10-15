import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数の読み込み
load_dotenv()

def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーの入力テキスト
        expert_type (str): 専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # 専門家の種類に応じたシステムメッセージの設定
    expert_prompts = {
        "健康アドバイザー": "あなたは健康に関する専門家です。医学的知識に基づいて、安全で実践的な健康アドバイスを提供してください。ただし、重篤な症状の場合は医師への相談を促してください。",
        "料理研究家": "あなたは料理の専門家です。美味しく栄養バランスの取れた料理レシピや調理のコツ、食材の選び方について詳しくアドバイスしてください。",
        "ITコンサルタント": "あなたはITとプログラミングの専門家です。技術的な問題解決や最新のIT動向、プログラミングに関する質問に対して、わかりやすく実践的なアドバイスを提供してください。",
        "旅行ガイド": "あなたは旅行の専門家です。世界各地の観光地、文化、グルメ、交通手段について詳しく、素晴らしい旅行プランや旅行のコツを提案してください。",
        "ビジネスコーチ": "あなたはビジネスとキャリアの専門家です。経営戦略、マーケティング、キャリア開発、チームマネジメントについて実践的なアドバイスを提供してください。"
    }
    
    system_message = expert_prompts.get(expert_type, "あなたは一般的なアシスタントです。質問に対して親切で正確な回答を提供してください。")
    
    try:
        # OpenAI APIキーの確認
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return "❌ エラー: OpenAI APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。"
        
        if not api_key.startswith("sk-"):
            return "❌ エラー: OpenAI APIキーの形式が正しくありません。正しいAPIキーを設定してください。"
        
        # OpenAI APIクライアントの初期化
        client = OpenAI(api_key=api_key)
        
        # ChatCompletions APIを使用してレスポンスを取得
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": input_text}
            ],
            temperature=0.5
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_message = str(e)
        
        # より詳細なエラー分析
        if "401" in error_message or "invalid_api_key" in error_message:
            return """❌ **APIキーエラー**: OpenAI APIキーが無効です。
            
**考えられる原因**:
- APIキーが期限切れまたは無効
- APIキーの形式が正しくない
- 環境変数の読み込みエラー

**解決方法**:
1. https://platform.openai.com/api-keys にアクセス
2. 新しいAPIキーを作成
3. `.env`ファイルの`OPENAI_API_KEY`を新しいキーに更新
4. サイドバーの「設定を再読み込み」ボタンを押す
5. 「APIキーをテスト」ボタンで確認
            
**注意**: APIキーには有効期限があり、使用制限もあります。"""
            
        elif "429" in error_message or "rate_limit" in error_message:
            return """❌ **レート制限エラー**: APIの使用制限に達しました。
            
**解決方法**:
1. しばらく時間をおいてから再試行
2. OpenAI Platform (https://platform.openai.com/usage) で使用状況を確認
3. 必要に応じてプランをアップグレード"""
            
        elif "quota" in error_message.lower() or "billing" in error_message.lower():
            return """❌ **利用制限エラー**: APIの利用制限に達しているか、課金設定に問題があります。
            
**解決方法**:
1. OpenAI Platform (https://platform.openai.com/usage) で使用状況を確認
2. 課金設定を確認・更新
3. 利用制限内での使用を心がけてください"""
            
        elif "403" in error_message:
            return """❌ **アクセス権限エラー**: APIへのアクセスが拒否されました。
            
**解決方法**:
1. APIキーの権限を確認
2. OpenAI Platformでアカウント状態を確認
3. 必要に応じてサポートに問い合わせ"""
            
        else:
            return f"""❌ **予期しないエラー**: {error_message}
            
**対処方法**:
1. サイドバーの「APIキーをテスト」でキーの有効性を確認
2. インターネット接続を確認
3. しばらく時間をおいてから再試行"""

def main():
    """
    Streamlitアプリのメイン関数
    """
    # ページ設定
    st.set_page_config(
        page_title="AI専門家チャット",
        page_icon="🤖",
        layout="wide"
    )
    
    # アプリのタイトル
    st.title("🤖 AI専門家チャットアプリ")
    
    # アプリの説明
    st.markdown("""
    ## 📖 アプリケーションの概要
    
    このアプリケーションは、様々な分野の専門家AIとチャットできるWebアプリケーションです。
    LangChainとOpenAI GPT-4o-miniを使用して、あなたの質問に専門的な知識で回答します。
    
    ## 🚀 使用方法
    
    1. **専門家を選択**: 下のラジオボタンから相談したい分野の専門家を選択してください
    2. **質問を入力**: テキストエリアにあなたの質問や相談内容を入力してください
    3. **回答を取得**: 「回答を取得」ボタンをクリックして、専門家AIからの回答を受け取ってください
    
    ---
    """)
    
    # 専門家の種類選択
    st.subheader("👨‍⚕️ 専門家を選択してください")
    expert_type = st.radio(
        "相談したい分野を選択:",
        ["健康アドバイザー", "料理研究家", "ITコンサルタント", "旅行ガイド", "ビジネスコーチ"],
        horizontal=True
    )
    
    # 専門家の説明
    expert_descriptions = {
        "健康アドバイザー": "💊 健康管理、栄養、運動、睡眠に関するアドバイスを提供します",
        "料理研究家": "🍳 レシピ、調理方法、食材選び、栄養バランスについてアドバイスします",
        "ITコンサルタント": "💻 プログラミング、システム設計、IT戦略について専門的なアドバイスを提供します",
        "旅行ガイド": "✈️ 世界各地の観光情報、旅行プラン、文化について詳しくガイドします",
        "ビジネスコーチ": "💼 経営戦略、マーケティング、キャリア開発について実践的なアドバイスを提供します"
    }
    
    st.info(f"**選択された専門家**: {expert_type}\n\n{expert_descriptions[expert_type]}")
    
    # 入力フォーム
    st.subheader("💬 質問を入力してください")
    user_input = st.text_area(
        "ここに質問や相談内容を入力してください:",
        height=150,
        placeholder="例: 最近眠れないのですが、どうしたらいいですか？"
    )
    
    # 回答取得ボタン
    if st.button("🔍 回答を取得", type="primary"):
        if user_input.strip():
            with st.spinner("専門家が回答を準備中..."):
                # LLMに問い合わせ
                response = get_llm_response(user_input, expert_type)
            
            # 回答表示
            st.subheader("💡 専門家からの回答")
            st.markdown(f"**{expert_type}からの回答:**")
            st.success(response)
            
        else:
            st.warning("質問を入力してください。")
    
    # サイドバーに追加情報
    with st.sidebar:
        st.header("🔧 設定確認")
        
        # APIキーの状態確認
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            if api_key.startswith("sk-"):
                st.success("✅ APIキーが設定されています")
                st.info(f"APIキー: {api_key[:7]}...{api_key[-4:]}")
                st.info(f"APIキーの長さ: {len(api_key)} 文字")
                
                # .envファイルからの読み込み確認
                load_dotenv(override=True)
                reloaded_key = os.environ.get("OPENAI_API_KEY")
                if reloaded_key == api_key:
                    st.success("✅ .envファイルから正常に読み込み済み")
                else:
                    st.warning("⚠️ .envファイルの再読み込みで値が変更されました")
            else:
                st.error("❌ APIキーの形式が正しくありません")
        else:
            st.error("❌ APIキーが設定されていません")
            
        # デバッグ情報
        with st.expander("🐛 デバッグ情報"):
            st.write("現在の作業ディレクトリ:", os.getcwd())
            env_file_path = os.path.join(os.getcwd(), '.env')
            st.write("想定される.envファイルパス:", env_file_path)
            st.write(".envファイルの存在:", os.path.exists(env_file_path))
            
        if st.button("🔄 設定を再読み込み"):
            load_dotenv(override=True)
            st.rerun()
            
        # APIキーテスト機能
        if st.button("🧪 APIキーをテスト"):
            test_api_key = os.environ.get("OPENAI_API_KEY")
            if test_api_key:
                try:
                    with st.spinner("APIキーをテスト中..."):
                        client = OpenAI(api_key=test_api_key)
                        test_response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": "Hello"}],
                            max_tokens=5
                        )
                    st.success("✅ APIキーは有効です！")
                    st.info(f"テスト応答: {test_response.choices[0].message.content}")
                except Exception as e:
                    st.error(f"❌ APIキーテスト失敗: {str(e)}")
            else:
                st.error("❌ APIキーが設定されていません")
        
        st.header("ℹ️ 注意事項")
        st.markdown("""
        - このアプリはAIによる回答です
        - 医療や法律に関する重要な判断は専門家に相談してください
        - プライベートな情報の入力は避けてください
        - APIキーは安全に管理してください
        """)
        
        st.header("🔧 技術仕様")
        st.markdown("""
        - **AI Model**: OpenAI GPT-4o-mini
        - **Framework**: OpenAI API
        - **UI**: Streamlit
        - **Language**: Python
        """)
        
        st.header("🆘 トラブルシューティング")
        st.markdown("""
        **APIキーエラーの場合**:
        1. [OpenAI Platform](https://platform.openai.com/api-keys)で新しいキーを作成
        2. `.env`ファイルを更新
        3. アプリを再起動
        
        **よくある問題**:
        - APIキーの有効期限切れ
        - 使用制限の達成
        - 課金設定の問題
        - APIキーの形式エラー
        """)

if __name__ == "__main__":
    main()