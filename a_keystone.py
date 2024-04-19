import cv2
import numpy as np

img_path = 'image/fish.jpg'
output_dir = "image/"

def get_contour(org_img, img):
    contours_img = org_img.copy()

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_areas = {}
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        contour_areas[i] = area

    max_area = max(contour_areas.values())
    max_area_idx = [i for i, v in contour_areas.items() if v == max_area][0]

    max_contour = contours[max_area_idx]
    arc_len = cv2.arcLength(max_contour, True)

    # 輪郭の近似
    epsilon = 0.03 * arc_len  
    approx_contour = cv2.approxPolyDP(max_contour, epsilon, closed=True)

    cv2.drawContours(contours_img, [approx_contour], -1, (0,255,0), 30)
    cv2.imwrite(f"{output_dir}approx_contour.png",contours_img)

    return approx_contour

def get_plate_img(contour, org_img):
    approx = contour.tolist()

    left = sorted(approx, key=lambda x: x[0][0])[:2]
    right = sorted(approx, key=lambda x: x[0][0])[2:]

    left_down = sorted(left, key=lambda x: x[0][1])[0]
    left_up = sorted(left, key=lambda x: x[0][1])[1]
    right_down = sorted(right, key=lambda x: x[0][1])[0]
    right_up = sorted(right, key=lambda x: x[0][1])[1]

    perspective_base = np.float32([left_down, right_down, right_up, left_up])
    perspective = np.float32([[0, 0],[210, 0],[210, 297],[0, 297]])  # A4用紙のサイズに合わせて調整します

    psp_matrix = cv2.getPerspectiveTransform(perspective_base, perspective)
    img_psp = cv2.warpPerspective(org_img, psp_matrix, (210,297))  # A4用紙のサイズに合わせて調整します

    return img_psp

img = cv2.imread(img_path)
org_img = img.copy()  # 元の画像を保持します

# グレースケールに変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Cannyエッジ検出
edges = cv2.Canny(gray, 250, 150, apertureSize=3)

# 膨張と収縮
kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(edges,kernel,iterations = 1)
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=2)

# 輪郭検出
contour = get_contour(org_img, closing)

# 台形補正
psp_erode_img = get_plate_img(contour, org_img)


# 画像を保存
cv2.imwrite("image/keystoneout.png", psp_erode_img)

