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

<<<<<<< HEAD
        previewImage.innerHTML = "<img src='" + previewImage.src + "' >";
=======
        previewImage.innerHTML = "<img src='" + previewImage.src + "' width='200px'>";
>>>>>>> 6f2315181f90b414accb969b4e12bc7f5c4466ad
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
<<<<<<< HEAD
    previewImage.innerHTML = "<img src='" + document.getElementById("preview").src + "' width='50%' height='50%' >";

    //説明表示
    const msg = document.getElementById('msg');
    const MyTextarea = document.getElementById('my-textarea');
    msg.innerText = MyTextarea.value;
=======
    previewImage.innerHTML = "<img src='" + document.getElementById("preview").src + "' width='200px'>";
>>>>>>> 6f2315181f90b414accb969b4e12bc7f5c4466ad

    // モーダルを表示
    document.getElementById("myModal").style.display = "block";
}
modalBtn.addEventListener('click', function() {
    ModalOpen();
})


function submitForm() {
    // フォームの送信処理を実行（Ajaxや通常のフォーム送信）
    document.getElementById("imageUploadForm").submit();
}

function closeModal() {
    myModal.style.display = 'none';
}
close.addEventListener('click', closeModal);