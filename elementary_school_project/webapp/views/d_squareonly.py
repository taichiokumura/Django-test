import cv2

# 画像読み込み
image = cv2.imread('image/sheetlatest.jpg')

# 切り抜く座標（左上から右下までの矩形の座標）
coordinates = [
    (167, 315, 1247, 390),  #観察日     
    (167, 390, 1247, 465),  #観察場所1
    (167, 465, 1247, 540),  #観察場所2
    (167, 540, 1247, 1317),   #絵
    (167, 1370, 1247, 1806)   #説明欄
]

# 座標で画像を切り抜いて保存
for i, (start_x, start_y, end_x, end_y) in enumerate(coordinates):
    cropped_image = image[start_y:end_y, start_x:end_x]
    cv2.imwrite(f'd_cropped_image_{i+1}.jpg', cropped_image)