---
name: real-photo-poster
description: >
  生成真人摄影会海报（cos摄影会、约拍活动等）。使用真人cos照片作为底图，纯代码排版文字（零错字），
  支持角色设定卡片、微信二维码等元素。与acg-poster（AI生成二次元海报）不同，本skill完全基于
  Python PIL代码排版，适合需要精确文字控制的真人活动海报。
---

# Real Photo Poster Generator - 真人摄影会海报

通过 Python PIL 代码排版，在真人cos照片上叠加活动信息，生成零错字的专业海报。

## 与 acg-poster 的区别

| 特性 | real-photo-poster | acg-poster |
|------|------------------|------------|
| 底图 | 真人cos照片（用户提供） | AI生成二次元风格 |
| 文字 | Python PIL代码排版，零错字 | AI生成，可能有错字 |
| 适用 | 真人摄影会、约拍活动 | 二次元/ACG活动、漫展 |
| 角色图 | 可选，贴角色设定卡片 | AI生成角色 |
| 二维码 | 支持裁剪嵌入 | 不支持 |

## 环境要求

- Python 3 + Pillow (PIL)
- 字体文件（系统自带 Noto CJK + 可选装饰字体）

### 可用字体

| 字体 | 路径 | 风格 |
|------|------|------|
| Noto Sans CJK Black | /usr/share/fonts/google-noto-cjk/NotoSansCJK-Black.ttc | 超粗黑体 |
| Noto Sans CJK Bold | /usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc | 粗黑体 |
| Noto Sans CJK Medium | /usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc | 中等黑体 |
| Noto Serif CJK Black | /usr/share/fonts/google-noto-cjk/NotoSerifCJK-Black.ttc | 超粗衬线 |
| ZCOOL KuaiLe | /usr/share/fonts/custom/ZCOOLKuaiLe.ttf | 圆润可爱 |
| ZCOOL XiaoWei | /usr/share/fonts/custom/ZCOOLXiaoWei.ttf | 文艺清新 |
| Kiwi Maru | /usr/share/fonts/custom/KiwiMaru.ttf | 圆润温柔 |
| Zen Maru Gothic | /usr/share/fonts/custom/ZenMaruGothic.ttf | 圆润优雅 |
| M+ Rounded 1c | /usr/share/fonts/custom/MPlusRounded1c.ttf | 圆角现代 |

装饰字体不够时，用 npm + fontsource 下载：
```bash
cd /tmp && npm install --registry=https://registry.npmmirror.com @fontsource/<font-name>
# 然后用 fontTools 转 woff2 → ttf
```

## 工作流程

### 1. 收集信息

向用户确认以下内容：

| 信息 | 必填 | 示例 |
|------|------|------|
| 活动名称 | ✅ | 光环摄影会 |
| 副标题 | 可选 | 温州·第三届 |
| 日期 | ✅ | 2026.3.7 |
| 场次时间 | 可选 | 第一场 17:00-18:00 |
| 价格 | ✅ | ¥168/场 |
| 云代拍价格 | 可选 | ¥99 |
| 模特名 | ✅ | ran3 |
| 模特描述 | 可选 | 全网16万粉博主 |
| 角色名 | 可选 | 加奈子（魅魔看护士） |
| 真人cos照片 | ✅ | 用户发送的图片 |
| 角色设定图 | 可选 | 角色卡片图 |
| 微信二维码 | 可选 | 报名用二维码 |

### 2. 生成海报

使用脚本生成竖版 2:3 海报（2400x3600）：

```bash
python3 {baseDir}/scripts/generate.py \
  --src /path/to/cos_photo.jpg \
  --event "光环摄影会" \
  --subtitle "温州 · 第三届" \
  --date "2026.3.7" \
  --session1 "17:00 — 18:00" \
  --session2 "18:30 — 19:30" \
  --price 168 \
  --cloud-price 99 \
  --model-name "ran3" \
  --model-desc "全网16万粉博主" \
  --char-name "加奈子" \
  --char-sub "魅魔看护士" \
  --char-ref /path/to/char_card.jpg \
  --qr /path/to/qr_code.jpg \
  --output /path/to/poster.png
```

### 3. 设计规范

#### 布局结构（从上到下）
```
┌─────────────────────────┐
│ 副标题（左上）            │
│ 活动名大字（竖排左侧）    │
│ "摄影会"（竖排右侧）      │
│ ─── 分隔线 ───           │
│ 日期                     │
│ 场次信息                  │
│ ─── 分隔线 ───           │
│ 价格 / 云代拍             │
│ ─── 分隔线 ───           │
│ 模特名 / 描述             │
│                          │
│ [角色卡片]    [二维码]     │
│  左下旋转      右下        │
│ 底部英文                  │
└─────────────────────────┘
```

#### 遮罩策略
- 左侧渐变遮罩：从左到右逐渐透明（宽度55%），保证文字可读
- 底部渐变遮罩：从下到上逐渐透明（高度30%），覆盖角色卡区域
- 顶部轻微遮罩：15%高度，保证副标题可读

#### 字体搭配原则
- 标题大字（活动名）：Noto Serif CJK Black — 大气庄重
- 数字/价格/模特名：Noto Sans CJK Black — 醒目现代
- 正文信息：Noto Sans CJK Medium — 清晰易读
- 可爱点缀（场次标签、角色名）：ZCOOL KuaiLe — 圆润可爱
- 不要全部换装饰字体，只在需要可爱感的地方点缀
- 书法/手写体不适合摄影会海报，避免使用

#### 角色卡片
- 位置：左下角
- 带白色边框 + 圆角
- 旋转 7° 倾斜
- 高斯模糊投影
- 上方放"当日角色"标签 + 角色名 + 角色描述

#### 二维码
- 位置：右下角
- 精确裁剪只保留二维码本身（不含头像/文字）
- 不加额外边框
- 上方放"报名方式"标签

### 4. 迭代优化

常见调整：
- 文字看不清 → 加深遮罩或给文字加描边（`otxt` 函数）
- 字体太单调 → 在场次/角色名处用快乐体点缀
- 间距不对 → 调整 y 坐标
- 颜色不搭 → 调整 GOLD/PINK/HOT_PINK 色值

## 参考脚本

完整生成脚本见 `scripts/generate.py`
