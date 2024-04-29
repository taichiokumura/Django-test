document.getElementById("id_photo").addEventListener("change", function () {
    previewImage(this);
});

const modalBtn = document.getElementById('myBtn');
const close = document.querySelector('.js-modal-close');
const myModal = document.getElementById('myModal');

function previewImage(obj) {
    const fileReader = new FileReader();
    fileReader.onload = function () {
        const imageUrl = fileReader.result;

        // 画像のプレビューを表示
        const previewImage = document.getElementById("preview");
        previewImage.src = imageUrl;

        previewImage.innerHTML = "<img src='" + previewImage.src + "' >";
    };
    fileReader.readAsDataURL(obj.files[0]);
}

function ModalOpen() {
    const modalContent = document.getElementById("modalContent");

    // フォームの入力値をモーダルに表示
    const contentHTML = "<p>この画像を切り抜きますか？</p>";

    modalContent.innerHTML = contentHTML;

    // プレビュー画像も表示
    const previewImage = document.getElementById("imagePreview");
    previewImage.innerHTML = "<img src='" + document.getElementById("preview").src + "' width='50%' height='50%' >";

    //説明表示
    // const msg = document.getElementById('msg');
    // const MyTextarea = document.getElementById('my-textarea');
    // msg.innerText = MyTextarea.value;

    // モーダルを表示
    document.getElementById("myModal").style.display = "block";
}
modalBtn.addEventListener('click', function() {
    ModalOpen();
})

// 画像選択ボタンにイベントリスナーを追加
document.getElementById("upload_btn").addEventListener("click", function() {
    // フォーム要素とフォームデータを取得
    var form = document.getElementById("imageUploadForm");
    var formData = new FormData(form);

    // ファイルが選択されているかを確認
    const fileInput = document.getElementById('id_photo');
    const file = fileInput.files[0];
    if (!file) {
        alert('ファイルを選択してください。');
        return;
    }

    console.log('ファイルが送信されました:', file);

    // XMLHttpRequestを使用してフォームを非同期で送信
    var xhr = new XMLHttpRequest();
    xhr.open('POST', form.action, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log('リクエストが成功しました')
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                // ログイン成功時の処理
                console.log('ログイン成功：', response.student_id);
                
            } else {
                // ログイン失敗時の処理
                console.log('ログイン失敗:', response.error_message);
                // エラーメッセージをアラートで表示
                alert('ログインに失敗しました。' + response.error_message);
            }
        } else {
            // エラー時の処理
            // console.log('エラーが発生しました');
            // // エラーメッセージをアラートで表示
            // alert('エラーが発生しました。');
            console.log('リクエストが失敗しました')
        }
    };
    // フォームデータを送信
    xhr.send(formData);
});


function closeModal() {
    myModal.style.display = 'none';
}
close.addEventListener('click', closeModal);