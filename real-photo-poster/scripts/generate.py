#!/usr/bin/env python3
"""光环摄影会 海报 v5 - 回归v1干净布局 + 角色卡 + 二维码"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "/root/.openclaw/qqbot/downloads/43EFDEB69176B5FBB4B8AB4CC27B146D_1772044340340.jpg"
CHAR_REF = "/root/.openclaw/qqbot/downloads/C8571EDC8EEC06ABB08D6F0BFEA0B496_1772058020109.jpg"
QR_SRC = "/root/.openclaw/qqbot/downloads/49454C0D9A227F95C7FC2C41272107EE_1772060975866.jpg"
OUT = "/root/.openclaw/workspace/poster_v5.png"

W, H = 2400, 3600

# 字体 - 只用三种
F_BLACK = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Black.ttc"
F_BOLD = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"
F_MED = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Medium.ttc"
F_REG = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc"
F_LIGHT = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc"
F_SERIF_BK = "/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Black.ttc"
F_SERIF_BD = "/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc"
F_CUTE = "/usr/share/fonts/custom/ZCOOLKuaiLe.ttf"

PINK = (255, 140, 170)
HOT_PINK = (255, 80, 130)
WHITE = (255, 255, 255)
GOLD = (255, 215, 140)
LIGHT_GOLD = (255, 235, 200)


def lf(p, s):
    return ImageFont.truetype(p, s, index=0)


def main():
    # 加载底图
    src = Image.open(SRC).convert("RGB")
    sw, sh = src.size
    tr = W / H
    sr = sw / sh
    if sr > tr:
        nw = int(sh * tr); l = (sw - nw) // 2
        src = src.crop((l, 0, l + nw, sh))
    else:
        nh = int(sw / tr); t = (sh - nh) // 2
        src = src.crop((0, t, sw, t + nh))
    src = src.resize((W, H), Image.LANCZOS)
    poster = src.copy().convert("RGBA")

    # 渐变遮罩 - v1风格
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for x in range(int(W * 0.55)):
        a = int(200 * (1 - x / (W * 0.55)))
        od.line([(x, 0), (x, H)], fill=(15, 10, 20, a))
    for y in range(int(H * 0.7), H):
        p = (y - H * 0.7) / (H * 0.3)
        od.line([(0, y), (W, y)], fill=(15, 10, 20, int(180 * p)))
    for y in range(int(H * 0.15)):
        od.line([(0, y), (W, y)], fill=(15, 10, 20, int(100 * (1 - y / (H * 0.15)))))
    poster = Image.alpha_composite(poster, ov)

    # 文字层
    tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tl)

    # "温州 · 第三届"
    td.text((100, 100), "温州 · 第三届", font=lf(F_MED, 72), fill=(255, 255, 255, 200))

    # "光" "环" 竖排大字
    td.text((80, 240), "光", font=lf(F_SERIF_BK, 380), fill=GOLD)
    td.text((80, 640), "环", font=lf(F_SERIF_BK, 380), fill=GOLD)

    # "摄影会" 竖排
    f_ev = lf(F_SERIF_BK, 140)
    yy = 280
    for ch in "摄影会":
        bbox = f_ev.getbbox(ch)
        ch_h = bbox[3] - bbox[1]
        td.text((480, yy), ch, font=f_ev, fill=WHITE)
        yy += ch_h + 30

    # 分隔线
    td.line([(100, 1060), (700, 1060)], fill=(255, 140, 170, 100), width=2)

    # 日期
    td.text((100, 1100), "2026", font=lf(F_BLACK, 130), fill=WHITE)
    td.text((500, 1120), ".3.7", font=lf(F_BLACK, 110), fill=GOLD)

    # 场次 - 快乐体标签
    td.text((100, 1280), "第一场", font=lf(F_CUTE, 60), fill=PINK)
    td.text((330, 1280), "17:00 — 18:00", font=lf(F_MED, 56), fill=(255, 255, 255, 220))
    td.text((100, 1370), "第二场", font=lf(F_CUTE, 60), fill=PINK)
    td.text((330, 1370), "18:30 — 19:30", font=lf(F_MED, 56), fill=(255, 255, 255, 220))

    # 分隔线
    td.line([(100, 1480), (700, 1480)], fill=(255, 140, 170, 100), width=2)

    # 价格
    td.text((100, 1520), "¥", font=lf(F_BLACK, 80), fill=HOT_PINK)
    td.text((180, 1510), "168", font=lf(F_BLACK, 110), fill=WHITE)
    td.text((500, 1540), "/场", font=lf(F_MED, 52), fill=(255, 255, 255, 180))
    td.text((100, 1640), "每场 4拍1", font=lf(F_MED, 50), fill=(255, 255, 255, 160))

    # 云代拍
    td.rounded_rectangle([(100, 1720), (300, 1778)], radius=8, fill=(255, 80, 130, 180))
    td.text((120, 1728), "云代拍", font=lf(F_BOLD, 38), fill=WHITE)
    td.text((320, 1722), "¥99", font=lf(F_BLACK, 56), fill=LIGHT_GOLD)

    # 分隔线
    td.line([(100, 1830), (700, 1830)], fill=(255, 140, 170, 100), width=2)

    # ran3
    td.text((100, 1870), "ran3", font=lf(F_BLACK, 130), fill=WHITE)
    td.text((100, 2010), "全网16万粉博主", font=lf(F_MED, 48), fill=(255, 255, 255, 180))

    # 底部英文
    td.text((100, H - 120), "HALO PHOTOGRAPHY SESSION  |  WENZHOU",
            font=lf(F_REG, 36), fill=(255, 255, 255, 100))

    poster = Image.alpha_composite(poster, tl)

    # === 角色卡片 左下角 ===
    ci = Image.open(CHAR_REF).convert("RGBA")
    ch_ = 580; cw_ = int(ch_ * ci.width / ci.height)
    ci = ci.resize((cw_, ch_), Image.LANCZOS)
    mask = Image.new("L", (cw_, ch_), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (cw_, ch_)], radius=18, fill=255)
    cm = Image.new("RGBA", (cw_, ch_), (0, 0, 0, 0))
    cm.paste(ci, (0, 0), mask)
    bw, bh = cw_ + 14, ch_ + 14
    bd = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ImageDraw.Draw(bd).rounded_rectangle([(0, 0), (bw-1, bh-1)], radius=22, fill=(255, 255, 255, 200))
    bd.paste(cm, (7, 7), cm)
    rot = bd.rotate(7, expand=True, resample=Image.BICUBIC)

    cx, cy = 70, H - rot.height - 160
    cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # 投影
    si = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    si.paste((0, 0, 0, 60), (cx+10, cy+10, cx+10+rot.width, cy+10+rot.height), rot.split()[3])
    si = si.filter(ImageFilter.GaussianBlur(radius=6))
    cl = Image.alpha_composite(cl, si)
    cl.paste(rot, (cx, cy), rot)

    # 当日角色标签+文字 在卡片上方
    cld = ImageDraw.Draw(cl)
    lx, ly = cx + 25, cy - 150
    cld.rounded_rectangle([(lx, ly), (lx+230, ly+56)], radius=10, fill=(255, 80, 130, 220))
    cld.text((lx+22, ly+8), "当日角色", font=lf(F_BOLD, 36), fill=WHITE)
    cld.text((lx, ly+68), "加奈子", font=lf(F_CUTE, 72), fill=WHITE)
    cld.text((lx+5, ly+150), "魅魔看护士", font=lf(F_MED, 42), fill=PINK)

    poster = Image.alpha_composite(poster, cl)

    # === 二维码 右下角 - 无边框 ===
    qr_full = Image.open(QR_SRC).convert("RGBA")
    qr = qr_full.crop((157, 575, 707, 1125))  # 精确裁剪二维码
    qr_sz = 340
    qr = qr.resize((qr_sz, qr_sz), Image.LANCZOS)

    ql = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    qd = ImageDraw.Draw(ql)
    qx = W - qr_sz - 80
    qy = H - qr_sz - 130
    # 直接贴二维码，不加边框
    ql.paste(qr, (qx, qy), qr)
    # 报名方式标签
    qd.rounded_rectangle([(qx, qy-66), (qx+qr_sz, qy-6)],
                         radius=10, fill=(255, 80, 130, 220))
    qd.text((qx+70, qy-58), "报名方式", font=lf(F_CUTE, 44), fill=WHITE)

    poster = Image.alpha_composite(poster, ql)

    poster.convert("RGB").save(OUT, quality=95)
    print(f"Done! {OUT}")


if __name__ == "__main__":
    main()
