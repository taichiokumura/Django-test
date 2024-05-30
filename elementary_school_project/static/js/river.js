document.addEventListener('DOMContentLoaded', function () {
    const river = document.getElementById('river');
    const canvas = document.getElementById('river-canvas');
    const ctx = canvas.getContext('2d');
    const message = document.getElementById('message');

    river.onload = function () {
        canvas.width = river.width;
        canvas.height = river.height;
        ctx.drawImage(river, 0, 0, river.width, river.height);
    };

    const regions = [
        { name: '上流', x: 0, y: 0, width: river.width, height: river.height * 0.33 },
        { name: '中流', x: 0, y: river.height * 0.33, width: river.width, height: river.height * 0.33 },
        { name: '下流', x: 0, y: river.height * 0.66, width: river.width, height: river.height * 0.33 },
    ];

    river.addEventListener('click', function(event) {
        // なんのメソッド?
        //画像要素riverの位置とサイズに関する情報を取得
        const rect = river.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        for (const region of regions) {
            if (x >= region.x && x <= region.x + region.width &&
                y >= region.y && y <= region.y + region.height) {
                    message.innerText = `${region.name} をクリックしました`;
                    return;
            }
        }
        message.innerText = 'クリックされた場所に領域はありません';
    });
});