import numpy as np
import cv2

def sheet_upload(request, uploaded_file_path):
    # マーカーの設定
    marker=cv2.imread('media/marker2.png', 0) 
    w, h = marker.shape[::-1]

    # スキャン画像を読み込む
    img = cv2.imread(uploaded_file_path, 0)
    res = cv2.matchTemplate(img, marker, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where( res >= threshold)
    mark_area={}
    mark_area['top_x']= min(loc[1])
    mark_area['top_y']= min(loc[0])
    mark_area['bottom_x']= max(loc[1])
    mark_area['bottom_y']= max(loc[0])
    img = img[mark_area['top_y']:mark_area['bottom_y'],mark_area['top_x']:mark_area['bottom_x']]
    # cv2.imwrite('media/res_sheet.png',img)

    n_col = 3 # 1行あたりのマークの数
    n_row = 2 # マークの行数
    margin_top = 1 # 上余白行数
    margin_bottom = 1 # 下余白行数
    n_row = n_row + margin_top + margin_bottom # 行数 (マーク行 7行 + 上余白 3行 + 下余白 1行)

    img = cv2.resize(img, (n_col*100, n_row*100))
    img = cv2.GaussianBlur(img,(5,5),0)
    res, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img = 255 - img
    # cv2.imwrite('media/sirokuro2.png',img)

    # 質問ごとの回答の単語リスト
    answers = [
        ["上流", "中流", "下流"],
        ["メダカ", "カニ", "カエル"]
    ]

    # 結果を入れる配列を用意
    result = []

    # 行ごとの処理(余白行を除いて処理を行う)
    for row in range(margin_top, n_row - margin_bottom):
        # 処理する行だけ切り出す
        tmp_img = img[row*100:(row+1)*100,]
        area_sum = [] # 合計値を入れる配列

        # 各マークの処理
        for col in range(n_col):
            # NumPyで各マーク領域の画像の合計値を求める
            area_sum.append(np.sum(tmp_img[:,col*100:(col+1)*100]))

        # 画像領域の合計値が，中央値の3倍以上かどうかで判断
        result.append(area_sum > np.median(area_sum) * 2.3)
        print(area_sum)
    # 結果を出力
    for x, row_result in enumerate(result):
        marked_answer_indices = np.where(row_result)[0]
        if len(marked_answer_indices) > 0:
            # マークされた回答がある場合、該当する単語を出力
            answers_for_question = answers[x]
            marked_answers = [answers_for_question[i] for i in marked_answer_indices]
            if len(marked_answers) > 1:
                print(f'Q%d: ' % (x+1) + ' / '.join(marked_answers) + ' ## 複数回答 ##')
                return {'success': False, 'error_message': 'マークが複数あります。'}
                
            else:
                print(f'Q%d: ' % (x+1) + marked_answers[0])
        
                return {'success': True, 'success_message': 'マークが認識できました'}
                
        else:
            # マークがない場合
            print(f'Q%d: ** 未回答 **' % (x+1))
            return {'success': False, 'error_message': 'マークが見つかりませんでした。'}
