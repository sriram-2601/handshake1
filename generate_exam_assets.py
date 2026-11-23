import os
from PIL import Image, ImageDraw, ImageFont

def get_font(name, size, fallback="arial.ttf"):
    try:
        return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
    except Exception:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{fallback}", size)
        except Exception:
            return ImageFont.load_default()

def draw_gradient_background(draw, width, height, top_color, bottom_color):
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * (y / height))
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * (y / height))
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_radial_glow(img, center_x, center_y, radius, color, max_alpha=120):
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_layer)
    for r in range(radius, 0, -4):
        alpha = int(max_alpha * (1 - r / radius)**1.5)
        gdraw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(color[0], color[1], color[2], alpha))
    img.alpha_composite(glow_layer)

def generate_exam_lockscreen(output_path="countdown_lockscreen_final_exam_9_16.png"):
    width, height = 1080, 1920
    img = Image.new("RGBA", (width, height), (13, 17, 28, 255))
    draw = ImageDraw.Draw(img)
    
    # Modern deep violet / navy gradient
    draw_gradient_background(draw, width, height, (15, 23, 42), (30, 27, 75))
    
    # Ambient glows
    draw_radial_glow(img, width // 2, 380, 440, (147, 51, 234), 60)   # Purple glow behind clock
    draw_radial_glow(img, 200, 1100, 500, (59, 130, 246), 55)        # Blue glow
    draw_radial_glow(img, 850, 1550, 450, (236, 72, 153), 45)        # Pink glow
    
    draw = ImageDraw.Draw(img)
    
    # Grid dots
    for gx in range(60, width, 120):
        for gy in range(60, height, 120):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(255, 255, 255, 22))

    # --- TOP 32% RESERVED FOR SYSTEM CLOCK ---
    font_clock_date = get_font("segoeui.ttf", 32)
    font_clock_time = get_font("segoeuib.ttf", 96)
    font_clock_hint = get_font("segoeui.ttf", 26)
    
    draw.text((width // 2, 220), "TUESDAY, DECEMBER 1", fill=(192, 132, 252, 220), font=font_clock_date, anchor="mm")
    draw.text((width // 2, 330), "09:41", fill=(255, 255, 255, 240), font=font_clock_time, anchor="mm")
    draw.text((width // 2, 420), "14 DAYS TO TARGET DEADLINE", fill=(216, 180, 254, 230), font=font_clock_hint, anchor="mm")
    
    draw.line([(width // 2 - 180, 465), (width // 2 + 180, 465)], fill=(168, 85, 247, 140), width=3)

    # --- MAIN COUNTDOWN CONTAINER (Glassmorphic Card) ---
    card_x1, card_y1 = 80, 540
    card_x2, card_y2 = 1000, 1720
    
    card_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_layer)
    cdraw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=42, fill=(17, 24, 39, 210), outline=(168, 85, 247, 130), width=2)
    img.alpha_composite(card_layer)
    
    draw = ImageDraw.Draw(img)
    
    font_badge = get_font("segoeuib.ttf", 24)
    font_title = get_font("segoeuib.ttf", 46)
    font_sub = get_font("segoeui.ttf", 26)
    
    # Pill badge
    badge_w, badge_h = 330, 46
    bx1, by1 = width // 2 - badge_w // 2, card_y1 + 45
    draw.rounded_rectangle([bx1, by1, bx1 + badge_w, by1 + badge_h], radius=23, fill=(126, 34, 206, 180), outline=(192, 132, 252, 220), width=2)
    draw.text((width // 2, by1 + badge_h // 2), "T-MINUS COUNTDOWN", fill=(255, 255, 255), font=font_badge, anchor="mm")
    
    draw.text((width // 2, card_y1 + 135), "FINAL EXAM & CAPSTONE", fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, card_y1 + 185), "Target Date: December 15, 2026", fill=(203, 213, 225), font=font_sub, anchor="mm")
    
    draw.line([(card_x1 + 60, card_y1 + 225), (card_x2 - 60, card_y1 + 225)], fill=(75, 85, 99, 160), width=1)

    # Milestones (Strictly <= 5 words per milestone description)
    milestones = [
        {"t": "T-14 Days", "date": "Dec 01", "desc": "Syllabus Review & Summary Notes", "done": True,  "tag": "FOUNDATION"},
        {"t": "T-7 Days",  "date": "Dec 08", "desc": "Complete All Practice Exams",     "done": False, "tag": "PRACTICE"},
        {"t": "T-3 Days",  "date": "Dec 12", "desc": "Deep Dive Weak Areas",          "done": False, "tag": "REVIEW"},
        {"t": "T-1 Day",   "date": "Dec 14", "desc": "Final Formula Memory Check",       "done": False, "tag": "WARMUP"},
        {"t": "T-0 Days",  "date": "Dec 15", "desc": "Ace Exam & Celebrate",           "done": False, "tag": "TARGET"},
    ]
    
    item_y = card_y1 + 265
    font_t = get_font("segoeuib.ttf", 32)
    font_desc = get_font("segoeuib.ttf", 29)
    font_tag = get_font("segoeuib.ttf", 18)
    
    for i, m in enumerate(milestones):
        row_y = item_y + (i * 165)
        
        row_bg = (31, 41, 55, 140) if not m["done"] else (22, 101, 52, 100)
        row_border = (75, 85, 99, 130) if not m["done"] else (34, 197, 94, 160)
        draw.rounded_rectangle([card_x1 + 40, row_y - 20, card_x2 - 40, row_y + 115], radius=24, fill=row_bg, outline=row_border, width=1)
        
        box_x = card_x1 + 75
        box_y = row_y + 48
        box_r = 24
        
        if m["done"]:
            draw.ellipse([box_x - box_r, box_y - box_r, box_x + box_r, box_y + box_r], fill=(34, 197, 94), outline=(74, 222, 128), width=3)
            chk_pts = [(box_x - 11, box_y), (box_x - 3, box_y + 9), (box_x + 12, box_y - 8)]
            draw.line(chk_pts, fill=(255, 255, 255), width=4, joint="curve")
        else:
            draw.ellipse([box_x - box_r, box_y - box_r, box_x + box_r, box_y + box_r], fill=(17, 24, 39), outline=(156, 163, 175), width=3)
            
        t_color = (216, 180, 254) if not m["done"] else (74, 222, 128)
        draw.text((card_x1 + 130, row_y + 14), m["t"], fill=t_color, font=font_t)
        
        tag_bg = (55, 65, 81, 220) if not m["done"] else (20, 83, 45, 220)
        tag_text = f"{m['date']} • {m['tag']}"
        draw.rounded_rectangle([card_x1 + 310, row_y + 14, card_x1 + 530, row_y + 46], radius=10, fill=tag_bg)
        draw.text((card_x1 + 420, row_y + 30), tag_text, fill=(243, 244, 246), font=font_tag, anchor="mm")
        
        desc_color = (255, 255, 255) if not m["done"] else (220, 252, 231)
        draw.text((card_x1 + 130, row_y + 64), m["desc"], fill=desc_color, font=font_desc)

    # Footer banner
    draw.rounded_rectangle([card_x1 + 60, card_y2 - 95, card_x2 - 60, card_y2 - 35], radius=20, fill=(31, 41, 55, 180), outline=(168, 85, 247, 90))
    draw.text((width // 2, card_y2 - 65), "🎯 WORK BACKWARD • CRUSH YOUR DEADLINE 🎯", fill=(216, 180, 254), font=font_badge, anchor="mm")
    
    draw.rounded_rectangle([width // 2 - 140, height - 45, width // 2 + 140, height - 35], radius=5, fill=(255, 255, 255, 120))
    
    img.save(output_path, "PNG")
    print(f"Generated exam lockscreen saved to {output_path}")
    return output_path

def generate_exam_cover(lockscreen_path="countdown_lockscreen_final_exam_9_16.png", output_path="handshake_cover_final_exam_3_2.png"):
    width, height = 1800, 1200
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    draw_gradient_background(draw, width, height, (10, 15, 30), (25, 20, 55))
    
    draw_radial_glow(img, 1350, 600, 520, (147, 51, 234), 65)
    draw_radial_glow(img, 350, 400, 600, (59, 130, 246), 55)
    draw_radial_glow(img, 800, 1000, 550, (236, 72, 153), 40)
    
    draw = ImageDraw.Draw(img)
    for gx in range(50, width, 100):
        for gy in range(50, height, 100):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(255, 255, 255, 18))

    font_badge = get_font("segoeuib.ttf", 26)
    font_h1 = get_font("segoeuib.ttf", 66)
    font_h2 = get_font("segoeuib.ttf", 44)
    font_body = get_font("segoeui.ttf", 28)
    font_feature = get_font("segoeuib.ttf", 28)
    
    draw.rounded_rectangle([100, 110, 520, 165], radius=28, fill=(126, 34, 206, 180), outline=(192, 132, 252), width=2)
    draw.text((310, 137), "GOOGLE GEMINI × HANDSHAKE", fill=(255, 255, 255), font=font_badge, anchor="mm")
    
    draw.text((100, 205), "Your Deadline, Your Design:", fill=(255, 255, 255), font=font_h1)
    draw.text((100, 285), "Countdown Lock Screen", fill=(192, 132, 252), font=font_h1)
    
    draw.text((100, 395), "Mission: Final Exam & Capstone Countdown", fill=(226, 232, 240), font=font_h2)
    
    desc_lines = [
        "A 14-day backward planning milestone system built with Google Gemini.",
        "Structures study preparation into T-14, T-7, T-3, and T-1 checkpoints.",
        "Combines habit tracking, phone clock clearance, and custom aesthetic",
        "typography to turn deadline stress into daily measurable momentum."
    ]
    for idx, line in enumerate(desc_lines):
        draw.text((100, 480 + idx * 40), line, fill=(156, 163, 175), font=font_body)

    features = [
        ("🎯", "T-Minus Architecture", "T-14, T-7, T-3, T-1, T-0 milestones under 5 words"),
        ("📱", "Native Lock Screen Fit", "Optimized 9:16 ratio with clean clock space"),
        ("🔔", "Accountability Reminders", "Scheduled daily calendar alert prompts")
    ]
    
    for i, (icon, ftitle, fdesc) in enumerate(features):
        fy = 690 + (i * 125)
        draw.rounded_rectangle([100, fy, 820, fy + 105], radius=20, fill=(17, 24, 39, 220), outline=(75, 85, 99, 200), width=2)
        draw.ellipse([125, fy + 22, 185, fy + 82], fill=(31, 41, 55), outline=(192, 132, 252, 160), width=2)
        draw.text((155, fy + 52), icon, font=font_badge, anchor="mm")
        draw.text((210, fy + 24), ftitle, fill=(255, 255, 255), font=font_feature)
        draw.text((210, fy + 62), fdesc, fill=(156, 163, 175), font=font_body)

    # Phone mockup on right
    phone_w, phone_h = 490, 870
    phone_x, phone_y = 1130, 165
    
    shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    for s in range(50, 0, -5):
        sdraw.rounded_rectangle([phone_x - s, phone_y - s, phone_x + phone_w + s, phone_y + phone_h + s], radius=50 + s, fill=(0, 0, 0, int(90 * (1 - s/50))))
    img.alpha_composite(shadow_layer)
    
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([phone_x - 12, phone_y - 12, phone_x + phone_w + 12, phone_y + phone_h + 12], radius=52, fill=(31, 41, 55), outline=(192, 132, 252, 140), width=3)
    draw.rounded_rectangle([phone_x - 4, phone_y - 4, phone_x + phone_w + 4, phone_y + phone_h + 4], radius=44, fill=(17, 24, 39))

    lock_img = Image.open(lockscreen_path).convert("RGBA")
    lock_resized = lock_img.resize((phone_w, phone_h), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (phone_w, phone_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, phone_w, phone_h], radius=40, fill=255)
    img.paste(lock_resized, (phone_x, phone_y), mask)
    
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([phone_x + phone_w//2 - 60, phone_y + 14, phone_x + phone_w//2 + 60, phone_y + 38], radius=12, fill=(0, 0, 0))
    
    draw.rounded_rectangle([phone_x + phone_w - 240, phone_y + phone_h - 70, phone_x + phone_w + 50, phone_y + phone_h - 15], radius=25, fill=(147, 51, 234, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((phone_x + phone_w - 95, phone_y + phone_h - 42), "✓ READY TO SUBMIT", fill=(255, 255, 255), font=font_badge, anchor="mm")

    img.save(output_path, "PNG")
    print(f"Generated exam cover saved to {output_path}")
    return output_path

if __name__ == "__main__":
    lock = generate_exam_lockscreen("countdown_lockscreen_final_exam_9_16.png")
    generate_exam_cover(lock, "handshake_cover_final_exam_3_2.png")
