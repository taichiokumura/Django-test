import numpy as np
import cv2

def sheet_reader(request, uploaded_file_path):
    # スキャン画像を読み込む
    img = cv2.imread(uploaded_file_path, 0)

    # チェックボックスの座標を指定
    checkbox_positions = [
        # Q1のチェックボックス座標 (x, y, width, height)
        [(186, 438, 19, 18), (309, 438, 19, 18), (433, 438, 19, 18),(556, 438, 19, 18), (651, 438, 19, 18), (765, 438, 19, 18)],
        # Q2のチェックボックス座標 (x, y, width, height)
        [(186, 513, 19, 18), (296, 513, 19, 18), (391, 513, 19, 18),(487, 513, 19, 18)]
    ]

    # 質問ごとの回答の単語リスト
    answers = [
        ["左岸", "中州", "右岸", "瀬", "ふち", "その他(陸上・上空など)"],
        ["どろ", "砂", "石", "コンクリート"]
    ]

    # 結果を入れる配列を用意
    result = []

    # 各質問の処理
    for q_idx, question in enumerate(checkbox_positions):
        row_result = []
        for cb_idx, (x, y, w, h) in enumerate(question):
            # 指定した座標の領域を切り出し
            cb_img = img[y:y+h, x:x+w]
            # 領域の画素値の合計を求める
            area_sum = np.sum(cb_img)
            # 画素値の合計がしきい値以下かどうかでマークの有無を判定
            is_marked = area_sum < 255 * w * h * 0.5  # しきい値は調整が必要
            row_result.append(is_marked)
        result.append(row_result)

    # 結果を出力
    all_success = True
    for q_idx, row_result in enumerate(result):
        marked_answer_indices = np.where(row_result)[0]
        if len(marked_answer_indices) > 0:
            # マークされた回答がある場合、該当する単語を出力
            answers_for_question = answers[q_idx]
            marked_answers = [answers_for_question[i] for i in marked_answer_indices]
            if len(marked_answers) > 1:
                print('Q%d: ' % (q_idx+1) + ' / '.join(marked_answers) + ' ## 複数回答 ##')
                return {'success': False, 'error_message': 'マークが複数あります。'}
            else:
                print('Q%d: ' % (q_idx+1) + marked_answers[0])
                
        else:
            # マークがない場合
            print('Q%d: ** 未回答 **' % (q_idx+1))
            all_success = False
    
    if all_success:
        return {'success': True, 'success_message': 'すべてのマークが認識されました'}
    else:
        return {'success': False, 'error_message': 'マークが見つかりませんでした'}
