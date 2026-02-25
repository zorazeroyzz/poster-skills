# 🎨 Poster Skills - 摄影会海报生成技能

OpenClaw Agent Skills，用于生成摄影会活动海报。

## 两个技能

### real-photo-poster - 真人摄影会海报
- 使用真人cos照片作为底图
- Python PIL 代码排版，文字零错字
- 支持角色设定卡片、微信二维码
- 适合：真人摄影会、约拍活动

### acg-poster - 二次元ACG海报
- 通过 Gemini 图像生成模型创建
- AI 生成二次元风格海报
- 适合：漫展、cosplay活动、二次元摄影会

## 字体资源

真人海报需要装饰字体，通过 npm + fontsource 下载：
```bash
cd /tmp && npm install --registry=https://registry.npmmirror.com @fontsource/zcool-kuaile
# fontTools 转 woff2 → ttf
```

## License
MIT
