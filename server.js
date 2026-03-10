const express = require('express');
const path = require('path');
const app = express();
const PORT = 8080;

// 设置静态文件目录 (当前目录)
app.use(express.static(__dirname));

// 监听端口
app.listen(PORT, () => {
    console.log(`🚀 游戏服务器已启动！`);
    console.log(`🌐 访问地址：http://localhost:${PORT}`);
    console.log(`📂 目录：${__dirname}`);
});