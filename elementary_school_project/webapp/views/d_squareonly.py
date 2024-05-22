import cv2
import os
from django.conf import settings

def square_cut(request, uploaded_file_path, card_info):

    try:
        # 画像読み込み
        image = cv2.imread(uploaded_file_path)
        if image is None:
            return {'success': False, 'error_message': '画像の読み込みに失敗しました。ファイルパスを確認してください。'}

        # 切り抜く座標（左上から右下までの矩形の座標）
        coordinates = [
            (167, 315, 1247, 390),  #観察日     
            (167, 390, 1247, 465),  #観察場所1
            (167, 465, 1247, 540),  #観察場所2
            (167, 540, 1247, 1317), #絵
            (167, 1370, 1247, 1806) #説明欄
        ]

        #出力ディレクトリのパスを
        output_dir = os.path.join(settings.MEDIA_ROOT, 'result_images')

        # 座標で画像を切り抜いて保存
        for i, (start_x, start_y, end_x, end_y) in enumerate(coordinates):
            cropped_image = image[start_y:end_y, start_x:end_x]
            if cropped_image.size == 0:
                return  {'success': False, 'error_message': f'座標({start_x}, {start_y}, {end_x}, {end_y})で切り抜きに失敗しました。'}
            
            output_path = os.path.join(output_dir, f'cropped_image_{i+1}.png')
            #画像保存
            output_path_success = cv2.imwrite(output_path, cropped_image)
            if output_path_success:
                # 切り抜いた画像をデータベースに格納
                if i == 0:
                    card_info.observation_date_images = output_path
                elif i == 1:
                    card_info.observation_place_images_1 = output_path
                elif i == 2:
                    card_info.observation_place_images_2 = output_path
                elif i == 3:
                    card_info.river_state_images = output_path
                elif i == 4:
                    card_info.living_thing_consideration_images = output_path

                print(f'画像を保存しました: {output_path}')
            else:
                print(f'画像の保存に失敗しました: {output_path}')
                return {'success': False, 'error_message': f'画像の保存に失敗しました: {output_path}'}
        
        card_info.save()
            
        return {'success': True, 'success_message': 'すべての画像が正常に切り抜かれました。'}
    
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return {'success': False, 'error_message': f'エラーが発生しました: {str(e)}'}