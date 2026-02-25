---
name: acg-poster
description: >
  生成二次元/ACG活动海报（摄影会、漫展、cosplay活动等）。支持角色参考图输入，自动生成带标题、日期、氛围效果的动漫风格活动海报。当用户要求制作二次元海报、漫展海报、cosplay活动海报、摄影会海报时激活。
---

# ACG Poster Generator

通过 Gemini 图像生成模型，创建高质量二次元活动海报。

## 环境要求

- API Key 和 Base URL（兼容 OpenAI 格式的图像生成 API）
- 环境变量: `ACG_POSTER_API_KEY`, `ACG_POSTER_BASE_URL`
- 默认模型: `gemini-3-pro-image-preview`
- Python 3 + requests

## 工作流程

### 1. 收集信息

向用户确认以下内容（缺什么问什么）：

| 信息 | 必填 | 示例 |
|------|------|------|
| 活动名称 | ✅ | 光环摄影会 |
| 副标题 | 可选 | 温州·第三届 |
| 日期 | 可选 | 2026.3.7 |
| 角色参考图 | 可选 | 用户发送的图片 |
| 角色描述 | 可选 | 魅魔看护士加奈子，棕色双马尾... |
| 风格/色调 | 可选 | 粉色暧昧、赛博朋克、日系清新 |

### 2. 生成海报（必须同时生成竖版+横版）

每次生成海报必须同时输出两张图：
1. 竖版 2:3（用于社交媒体、群分享、打印）
2. 横版 16:9（用于banner、群封面、B站头图）

先生成竖版，再以竖版为参考图生成横版（保持角色主体不变，扩展画面）。

```bash
# Step 1: 生成竖版
python3 {baseDir}/scripts/generate.py \
  --event "活动名称" \
  --subtitle "副标题" \
  --date "日期" \
  --ref-image /path/to/reference.png \
  --character "角色描述文字" \
  --style "风格描述" \
  --output /path/to/poster_vertical.png \
  --temperature 0.7

# Step 2: 以竖版为参考，生成横版16:9
python3 {baseDir}/scripts/generate.py \
  --event "活动名称" \
  --subtitle "副标题" \
  --date "日期" \
  --ref-image /path/to/poster_vertical.png \
  --style "Convert to 16:9 wide horizontal banner. Keep character EXACTLY as-is. Extend background. Title upper-left, date bottom-right." \
  --output /path/to/poster_wide.png \
  --temperature 0.7
```

参数说明：
- `--ref-image`: 角色参考图路径，提供后会以图生图方式还原角色
- `--character`: 文字描述角色特征（有参考图时作为补充，无图时作为主要描述）
- `--style`: 整体风格和色调描述
- `--temperature`: 0.5-0.9，越高越有创意，越低越稳定

### 3. 迭代优化

用户反馈后调整 prompt 重新生成。常见调整：
- 角色特征不对 → 在 `--character` 中更详细描述，降低 temperature
- 色调不对 → 修改 `--style`
- 不要某元素 → 在 style 中加 "NO xxx"
- 要更多变体 → 提高 temperature 到 0.8-0.9

## 风格预设参考

| 风格 | style 参数 |
|------|-----------|
| 粉色暧昧 | Pink, romantic, dreamy, 暧昧 atmosphere, heart bokeh, cherry blossoms |
| 赛博朋克 | Cyberpunk, neon glow, dark background, electric blue and magenta |
| 日系清新 | Soft pastel colors, light and airy, watercolor feel, gentle |
| 漫展经典 | Vibrant anime colors, bold composition, energetic, festival atmosphere |
| 极简黑白 | Black and white, high contrast, minimal, elegant typography space |

## 注意事项

- AI 生成的中文文字可能有错字，建议用户后期用PS/Canva覆盖修正
- 角色还原度取决于参考图质量和描述详细程度
- 如果角色特征偏移，在 character 描述中用 MUST/EXACT 等强约束词
- 每次生成约消耗 1 次 API 调用
