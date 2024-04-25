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
    const msg = document.getElementById('msg');
    const MyTextarea = document.getElementById('my-textarea');
    msg.innerText = MyTextarea.value;

    // モーダルを表示
    document.getElementById("myModal").style.display = "block";
}
modalBtn.addEventListener('click', function() {
    ModalOpen();
})

function submitForm() {
    // フォームの送信処理を実行
    document.getElementById("imageUploadForm").submit();
}

function loginWithQRCode() {
    // ログイン処理を実行
    $.ajax({
        type: "POST",
        url: "{% url 'webapp:login_qr_code' %}", // ここにログイン処理を行うURLを指定
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}',
            // その他のデータをここに追加
        },
        success: function(response) {
            console.log(response); 
            if (response.success) {
                alert("ログインに成功しました。学籍番号: " + response.student_id);
            } else {
                alert("ログインに失敗しました。");
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
            alert("エラーが発生しました: " + error);
        }
    });
}

function closeModal() {
    myModal.style.display = 'none';
}
close.addEventListener('click', closeModal);
