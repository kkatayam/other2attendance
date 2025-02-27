import streamlit as st
import pandas as pd
import io

# タイトル
st.title("📂 出席データ変換ツール（Web版）")

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    # CSV 読み込み（Shift-JIS対応、最初の1行目はスキップしない）
    raw_data = uploaded_file.read().decode("cp932")
    data_io = io.StringIO(raw_data)

    # 1行目をスキップ（タイトル行）
    first_line = data_io.readline().strip()

    # 2行目をヘッダーとして読み込む
    df = pd.read_csv(data_io, encoding="cp932")

    # **ファイル名から処理を分岐**
    file_name = uploaded_file.name.lower()
    
    if file_name.startswith("tststatus_"):  # `tststatus_` で始まる場合
        df_attendcourse = df[["#ユーザーID", "状況", "学籍番号/教職員番号", "氏名"]].copy()
        df_attendcourse.columns = ["ユーザーID", "出席状態種別", "(学籍番号/教職員番号)", "(氏名)"]
        df_attendcourse["出席状態種別"] = df_attendcourse["出席状態種別"].astype(str).str.strip().apply(lambda x: 1 if x == "実施済" else 0)

    elif file_name.startswith("eqtstatus_"):  # `eqtstatus_` で始まる場合
        df_attendcourse = df[["#ユーザーID", "状況", "学籍番号/教職員番号", "氏名"]].copy()
        df_attendcourse.columns = ["ユーザーID", "出席状態種別", "(学籍番号/教職員番号)", "(氏名)"]
        df_attendcourse["出席状態種別"] = df_attendcourse["出席状態種別"].astype(str).str.strip().apply(lambda x: 1 if x == "回答済" else 0)

    else:
        st.error("❌ 対応していないファイルです。")
        st.stop()

    # **登録日時を空欄にする**
    df_attendcourse["(登録日時)"] = ""

    # **数値データを桁区切りなしで表示**
    for col in df_attendcourse.select_dtypes(include=["int", "float"]).columns:
        df_attendcourse[col] = df_attendcourse[col].apply(lambda x: int(x) if pd.notnull(x) else "")

    # **変換後のデータを表示**
    st.subheader("✅ 変換後のデータ")
    st.dataframe(df_attendcourse)

    # **CSVファイルとしてダウンロード**
    output = io.BytesIO()
    df_attendcourse.to_csv(output, index=False, encoding="cp932")
    output.seek(0)

    st.download_button(
        label="📥 変換後のCSVをダウンロード",
        data=output.getvalue(),
        file_name="attendcourse.csv",
        mime="text/csv",
    )
