import os
import subprocess

def convert_utf16_to_utf8(directory='.'):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            
            # `file`コマンドを使ってファイルタイプを取得
            try:
                filetype_output = subprocess.check_output(['file', '-i', filepath], text=True)
            except subprocess.CalledProcessError as e:
                print(f"{filepath} のファイルタイプ取得中にエラーが発生しました: {e}")
                continue
            
            # ファイルがUTF-16LEかどうかをチェック
            if 'charset=utf-16le' in filetype_output:
                # ファイルをUTF-16LEからUTF-8に変換
                try:
                    # UTF-16LEエンコーディングでファイルを読み込む
                    with open(filepath, 'r', encoding='utf-16le') as f:
                        content = f.read()
                    
                    # UTF-8エンコーディングでファイルに書き戻す
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"{filepath} をUTF-16LEからUTF-8に変換しました。")
                except Exception as e:
                    print(f"{filepath} の変換中にエラーが発生しました: {e}")

if __name__ == "__main__":
    convert_utf16_to_utf8('/Users/uryuatsuya/Desktop/AA dataset')
