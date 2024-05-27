import cv2
import numpy as np
import os
from django.conf import settings

output_dir = os.path.join(settings.MEDIA_ROOT, 'corrected_images')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def preprocess_image(image_path):
    #画像読み込み
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}"
                                )
    org_img = img.copy()  # 元の画像を保持します

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Cannyエッジ検出
    edges = cv2.Canny(gray, 250, 150, apertureSize=3)

    # 膨張と収縮
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(edges,kernel,iterations = 1)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations=2)

    return org_img, closing


def get_contour(org_img, img, filename):
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
    cv2.imwrite(os.path.join(output_dir, f"approx_contour_{filename}.png"), contours_img)

    return approx_contour

def get_plate_img(contour, org_img, filename):
    approx = contour.tolist()

    left = sorted(approx, key=lambda x: x[0][0])[:2]
    right = sorted(approx, key=lambda x: x[0][0])[2:]

    left_down = sorted(left, key=lambda x: x[0][1])[0]
    left_up = sorted(left, key=lambda x: x[0][1])[1]
    right_down = sorted(right, key=lambda x: x[0][1])[0]
    right_up = sorted(right, key=lambda x: x[0][1])[1]

    perspective_base = np.float32([left_down, right_down, right_up, left_up])
    perspective = np.float32([[0, 0],[1414, 0],[1414, 2000],[0, 2000]])  # A4用紙のサイズに合わせて調整します

    psp_matrix = cv2.getPerspectiveTransform(perspective_base, perspective)
    img_psp = cv2.warpPerspective(org_img, psp_matrix, (1414,2000))  # A4用紙のサイズに合わせて調整します

    output_path = os.path.join(output_dir, f"keystone_corrected_{filename}.png")
    cv2.imwrite(output_path, img_psp)

    return output_path

def correct_keystone(image_path, filename):
    org_img, processed_img = preprocess_image(image_path)
    contour = get_contour(org_img, processed_img, filename)
    corrected_image_path = get_plate_img(contour, org_img, filename)

    return corrected_image_path

# # 輪郭検出
# contour = get_contour(org_img, closing)

# # 台形補正
# psp_erode_img = get_plate_img(contour, org_img)


# # 画像を保存
# cv2.imwrite("image/d_keystoneout.png", psp_erode_img)