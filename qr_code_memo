import cv2
import pyzbar.pyzbar as pyzbar

# 入力画像のパスを指定
input_image_path = 'image/sheet.png'

# 出力画像の解像度を指定する (幅, 高さ)
output_resolution = (800, 600)  # 適切な値に変更する

# 入力画像を読み込む
input_image = cv2.imread(input_image_path)

# QRコードを検出する
decoded_objects = pyzbar.decode(input_image)

# 結果を格納する画像を作成し、リサイズする
output_image = cv2.resize(input_image, output_resolution)

# 検出されたQRコードをデコードする
for obj in decoded_objects:
    # QRコードの座標を取得 (リサイズ後の座標に変換する)
    (x, y, w, h) = [
        int(val * output_resolution[0] / input_image.shape[1])
        for val in [obj.rect.left, obj.rect.top, obj.rect.width, obj.rect.height]
    ]
    
    # QRコードの内容をデコード
    qr_data = obj.data.decode("utf-8")
    
    # デコードされたデータをターミナルに出力
    print(f"Decoded QR Code Data: {qr_data}")
    
    # QRコードの位置を長方形で描画
    cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # デコードされたデータを画像上に描画
    cv2.putText(output_image, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# 結果を出力
cv2.imshow("QR Code Detection", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()