import cv2

# 入力画像のパス
input_file_path = 'image/square31.png'
# 出力画像のパス
output_file_path_prefix = 'image/square3110'

# 入力画像の読み込み
img = cv2.imread(input_file_path)

# 輪郭検出
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 元画像の幅と高さの3分の1を計算
o_width, o_height = img.shape[:2]
o_width //= 3
o_height //= 3

# 長方形を検出して切り出した画像の保存
for i, contour in enumerate(contours):
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        # 外接矩形の幅と高さが指定したサイズより大きい場合のみ保存
        if w > o_width and h > o_height:
            rectangle_roi = img[y:y + h, x:x + w]
            output_file_path = f"{output_file_path_prefix}_{i}.jpg"
            cv2.imwrite(output_file_path, rectangle_roi)
