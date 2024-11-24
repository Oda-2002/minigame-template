from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import os

app = Flask(__name__)

# CORS設定
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

# APIキーの設定 (ひらがな化API)
API_KEY = '7dd726c3e3bd92948d538e80c0773656d7b89328b3eb400a11e893efe91f7a12'

# ひらがな→音素変換関数
def hiragana_to_phonemes(hiragana_text):
    phoneme_map = {
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'k a', 'き': 'k i', 'く': 'k u', 'け': 'k e', 'こ': 'k o',
        'さ': 's a', 'し': 's i', 'す': 's u', 'せ': 's e', 'そ': 's o',
        'た': 't a', 'ち': 't i', 'つ': 't u', 'て': 't e', 'と': 't o',
        'な': 'n a', 'に': 'n i', 'ぬ': 'n u', 'ね': 'n e', 'の': 'n o',
        'は': 'h a', 'ひ': 'h i', 'ふ': 'h u', 'へ': 'h e', 'ほ': 'h o',
        'ま': 'm a', 'み': 'm i', 'む': 'm u', 'め': 'm e', 'も': 'm o',       
        'ら': 'r a', 'り': 'r i', 'る': 'r u', 'れ': 'r e', 'ろ': 'r o',
        'や': 'ja', 'ゆ': 'ju', 'よ': 'jo',
        'きゃ': 'k ja', 'きゅ': 'k ju', 'きょ': 'k jo',
        'ぎゃ': 'g ja', 'ぎゅ': 'g ju', 'ぎょ': 'g jo',
        'しゃ': 's ja', 'しゅ': 's ju', 'しょ': 's jo',
        'じゃ': 'z ja', 'じゅ': 'z ju', 'じょ': 'z jo',
        'ちゃ': 't ja', 'ちゅ': 't ju', 'ちょ': 't jo',
        'にゃ': 'n ja', 'にゅ': 'n ju', 'にょ': 'n jo',
        'ひゃ': 'h ja', 'ひゅ': 'h ju', 'ひょ': 'h jo',
        'ぴゃ': 'p ja', 'ぴゅ': 'p ju', 'ぴょ': 'p jo',
        'びゃ': 'b ja', 'びゅ': 'b ju', 'びょ': 'b jo',
        'みゃ': 'm ja', 'みゅ': 'm ju', 'みょ': 'm jo',
        'りゃ': 'r ja', 'りゅ': 'r ju', 'りょ': 'r jo',
        'わ': 'w a', 'を': 'w o', 'ん': 'N', 'っ': 'Q', 'ー': 'R',
        'だ': 'd a', 'で': 'd e', 'ど': 'd o',
        'ざ': 'z a', 'じ': 'z i', 'ず': 'z u', 'ぜ': 'z e', 'ぞ': 'z o',
        'が': 'g a', 'ぎ': 'g i', 'ぐ': 'g u', 'げ': 'g e', 'ご': 'g o',
        'ば': 'b a', 'び': 'b i', 'ぶ': 'b u', 'べ': 'b e', 'ぼ': 'b o',
        'ぱ': 'p a', 'ぴ': 'p i', 'ぷ': 'p u', 'ぺ': 'p e', 'ぽ': 'p o',
        'ゃ': 'ja', 'ゅ': 'ju', 'ょ': 'jo' 
    }

    phonemes = []
    skip_next = False

    for i in range(len(hiragana_text)):
        if skip_next:
            skip_next = False
            continue

        current_char = hiragana_text[i]
        next_char = hiragana_text[i + 1] if i + 1 < len(hiragana_text) else None

        # 拗音の処理: 「ゃ」「ゅ」「ょ」が続く場合
        if next_char in ['ゃ', 'ゅ', 'ょ']:
            combined = current_char + next_char
            phonemes.append(phoneme_map.get(combined, combined))  # 拗音を変換
            skip_next = True
        else:
            phonemes.append(phoneme_map.get(current_char, current_char))  # 通常の変換

    # デバッグ用: 変換結果をコンソールに出力
    print(f'変換結果: {" ".join(phonemes)}')
    
    return ' '.join(phonemes)

# ひらがな変換のエンドポイント
@app.route('/hiragana', methods=['POST'])
def hiragana():
    text = request.json.get('text', '')

    try:
        # ひらがな化APIを呼び出す
        response = requests.post('https://labs.goo.ne.jp/api/hiragana', json={
            'app_id': API_KEY,
            'sentence': text,
            'output_type': 'hiragana'
        })

        response.raise_for_status()
        hiragana = response.json().get('converted', '')
        phonemes = hiragana_to_phonemes(hiragana)

        return jsonify({
            'converted': hiragana,  # ひらがな化されたテキスト
            'phonemes': phonemes
        })
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return jsonify({'error': 'エラーが発生しました'}), 500

# ルート
@app.route('/')
def home():
    return render_template('A.html')

@app.route('/utterance_check')
def utterance_check():
    return render_template('A.html')

@app.route('/play-end')
def play_end():
    correct = request.args.get('correct', 0)
    mistakes = request.args.get('mistakes', 0)
    correctWords = request.args.get('correctWords', '')
    mistakeWords = request.args.get('mistakeWords', '')
    targetCorrect = request.args.get('targetCorrect', 5)
    return render_template('A_play_end.html', correct=correct, mistakes=mistakes, correctWords=correctWords, mistakeWords=mistakeWords, targetCorrect=targetCorrect)

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# サーバー起動
if __name__ == '__main__':
    app.run(debug=True)