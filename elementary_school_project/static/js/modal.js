window.addEventListener('load', function(){
    const fileInput = document.getElementById("id_photo");

    fileInput.addEventListener("change", function(event) {
        previewImage(event.target);
        if(!fileInput){ return false;}
    })
})

const modalBtn = document.getElementById('myBtn');
const close = document.querySelector('.js-modal-close');
const myModal = document.getElementById('myModal');

// 画像ファイルの読み込みと画像表示
function previewImage(obj) {
    // コンピュータに保存されているファイルの内容を非同期に読み取る
    const fileReader = new FileReader();
    // 画像読み込み完了した時点でイベント発生
    fileReader.onload = function () {
        const imageUrl = fileReader.result;

        // 画像のプレビューを表示
        const previewImage = document.getElementById("preview");
        previewImage.src = imageUrl;

        previewImage.innerHTML = "<img src='" + previewImage.src + "' >";
    };
    fileReader.readAsDataURL(obj.files[0]);
}

// モーダルウィンドウ表示関数
function ModalOpen() {
    const modalContent = document.getElementById("modalContent");

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

// 画像ファイルをバックエンドに送信
function submitForm() {
    document.getElementById('imageUploadForm').submit();

    // ファイルが選択されているかを確認
    const fileInput = document.getElementById('id_photo');
    const file = fileInput.files[0];
    if (!file) {
        alert('ファイルを選択してください。');
        return;
    }

    console.log('ファイルが送信されました:', file);
}

function closeModal() {
    myModal.style.display = 'none';
}
close.addEventListener('click', closeModal);

// オーバーレイ要素の取得
const overlay = document.getElementById('overlay');

// オーバーレイをクリックしても何も起こらないようにする
overlay.onclick = function() {
    return false;
}