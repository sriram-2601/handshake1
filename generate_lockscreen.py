import math
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

def generate_lockscreen(output_path="countdown_lockscreen_9_16.png"):
    width, height = 1080, 1920
    img = Image.new("RGBA", (width, height), (11, 15, 25, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Dark ambient background with cyber-slate gradient
    draw_gradient_background(draw, width, height, (10, 14, 26), (18, 24, 38))
    
    # Ambient glows
    draw_radial_glow(img, width // 2, 380, 420, (56, 189, 248), 65)  # Cyan glow behind clock area
    draw_radial_glow(img, 200, 1200, 500, (99, 102, 241), 50)        # Indigo glow
    draw_radial_glow(img, 880, 1600, 450, (16, 185, 129), 45)        # Emerald glow
    
    draw = ImageDraw.Draw(img)
    
    # Subtle geometric grid / dots
    for gx in range(60, width, 120):
        for gy in range(60, height, 120):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(255, 255, 255, 25))

    # --- TOP 32% IS RESERVED CLEAN SPACE FOR SYSTEM CLOCK ---
    # Clock placeholder guide (subtle aesthetic indicator)
    font_clock_hint = get_font("segoeui.ttf", 26)
    font_clock_time = get_font("segoeuib.ttf", 94)
    font_clock_date = get_font("segoeui.ttf", 32)
    
    # Display clock preview softly so user sees lockscreen look
    draw.text((width // 2, 220), "MONDAY, NOVEMBER 23", fill=(148, 163, 184, 220), font=font_clock_date, anchor="mm")
    draw.text((width // 2, 330), "06:00", fill=(255, 255, 255, 240), font=font_clock_time, anchor="mm")
    draw.text((width // 2, 420), "DEADLINE COUNTDOWN ACTIVE", fill=(56, 189, 248, 230), font=font_clock_hint, anchor="mm")

    # Divider bar
    draw.line([(width // 2 - 180, 465), (width // 2 + 180, 465)], fill=(56, 189, 248, 140), width=3)

    # --- MAIN COUNTDOWN CONTAINER (Glassmorphic Card) ---
    card_x1, card_y1 = 80, 540
    card_x2, card_y2 = 1000, 1720
    
    # Card surface
    card_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(card_layer)
    cdraw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=42, fill=(15, 23, 42, 205), outline=(56, 189, 248, 120), width=2)
    img.alpha_composite(card_layer)
    
    draw = ImageDraw.Draw(img)
    
    # Card Header
    font_badge = get_font("segoeuib.ttf", 24)
    font_title = get_font("segoeuib.ttf", 46)
    font_sub = get_font("segoeui.ttf", 26)
    
    # Pill badge
    badge_w, badge_h = 320, 46
    bx1, by1 = width // 2 - badge_w // 2, card_y1 + 45
    draw.rounded_rectangle([bx1, by1, bx1 + badge_w, by1 + badge_h], radius=23, fill=(37, 99, 235, 180), outline=(96, 165, 250, 220), width=2)
    draw.text((width // 2, by1 + badge_h // 2), "T-MINUS COUNTDOWN", fill=(255, 255, 255), font=font_badge, anchor="mm")
    
    draw.text((width // 2, card_y1 + 135), "MISSION: 6:00 PM SPRINT", fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, card_y1 + 185), "Target: Final Completion & Launch", fill=(148, 163, 184), font=font_sub, anchor="mm")
    
    # Horizontal separator
    draw.line([(card_x1 + 60, card_y1 + 225), (card_x2 - 60, card_y1 + 225)], fill=(51, 65, 85, 160), width=1)

    # Milestones definition
    milestones = [
        {"t": "T-7h", "time": "11:00 AM", "desc": "Kickoff & Core Architecture", "done": False, "tag": "START"},
        {"t": "T-5h", "time": "01:00 PM", "desc": "Feature Implementation Finished", "done": False, "tag": "BUILD"},
        {"t": "T-3h", "time": "03:00 PM", "desc": "Integration & First Build", "done": False, "tag": "SYNC"},
        {"t": "T-1h", "time": "05:00 PM", "desc": "QA Testing & Polish", "done": False, "tag": "VERIFY"},
        {"t": "T-0",  "time": "06:00 PM", "desc": "Ship & Submit Final", "done": True,  "tag": "DEADLINE"},
    ]
    
    item_y = card_y1 + 265
    font_t = get_font("segoeuib.ttf", 34)
    font_desc = get_font("segoeuib.ttf", 30)
    font_meta = get_font("segoeui.ttf", 22)
    font_tag = get_font("segoeuib.ttf", 18)
    
    for i, m in enumerate(milestones):
        row_y = item_y + (i * 165)
        
        # Sub-row container
        row_bg = (30, 41, 59, 130) if not m["done"] else (22, 101, 52, 90)
        row_border = (71, 85, 105, 120) if not m["done"] else (34, 197, 94, 160)
        draw.rounded_rectangle([card_x1 + 40, row_y - 20, card_x2 - 40, row_y + 115], radius=24, fill=row_bg, outline=row_border, width=1)
        
        # Checkbox
        box_x = card_x1 + 75
        box_y = row_y + 48
        box_r = 24
        
        if m["done"]:
            # Glowing checked circle
            draw.ellipse([box_x - box_r, box_y - box_r, box_x + box_r, box_y + box_r], fill=(34, 197, 94), outline=(74, 222, 128), width=3)
            # Checkmark poly
            chk_pts = [
                (box_x - 11, box_y),
                (box_x - 3, box_y + 9),
                (box_x + 12, box_y - 8)
            ]
            draw.line(chk_pts, fill=(255, 255, 255), width=4, joint="curve")
        else:
            # Unchecked ring
            draw.ellipse([box_x - box_r, box_y - box_r, box_x + box_r, box_y + box_r], fill=(15, 23, 42), outline=(148, 163, 184), width=3)
            
        # T-Minus Badge
        t_color = (56, 189, 248) if not m["done"] else (74, 222, 128)
        draw.text((card_x1 + 130, row_y + 14), m["t"], fill=t_color, font=font_t)
        
        # Time badge pill
        tag_bg = (51, 65, 85, 220) if not m["done"] else (20, 83, 45, 220)
        tag_text = f"{m['time']} • {m['tag']}"
        draw.rounded_rectangle([card_x1 + 250, row_y + 14, card_x1 + 470, row_y + 46], radius=10, fill=tag_bg)
        draw.text((card_x1 + 360, row_y + 30), tag_text, fill=(241, 245, 249), font=font_tag, anchor="mm")
        
        # Milestone Title Description (Strictly <= 5 words)
        desc_color = (255, 255, 255) if not m["done"] else (220, 252, 231)
        draw.text((card_x1 + 130, row_y + 64), m["desc"], fill=desc_color, font=font_desc)

    # Card Footer / Motivation
    draw.rounded_rectangle([card_x1 + 60, card_y2 - 95, card_x2 - 60, card_y2 - 35], radius=20, fill=(30, 41, 59, 180), outline=(56, 189, 248, 80))
    draw.text((width // 2, card_y2 - 65), "⚡ 100% FOCUS • FINISH STRONG BY 6:00 PM ⚡", fill=(56, 189, 248), font=font_badge, anchor="mm")
    
    # Bottom home bar
    draw.rounded_rectangle([width // 2 - 140, height - 45, width // 2 + 140, height - 35], radius=5, fill=(255, 255, 255, 120))
    
    img.save(output_path, "PNG")
    print(f"Generated lockscreen saved to {output_path}")
    return output_path

def generate_handshake_cover(lockscreen_path="countdown_lockscreen_9_16.png", output_path="handshake_cover_preview_3_2.png"):
    width, height = 1800, 1200  # 3:2 aspect ratio, >1200px wide
    img = Image.new("RGBA", (width, height), (10, 14, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient backdrop
    draw_gradient_background(draw, width, height, (7, 10, 19), (15, 23, 42))
    
    # Glowing ambient lights
    draw_radial_glow(img, 1350, 600, 500, (56, 189, 248), 65)
    draw_radial_glow(img, 350, 400, 600, (99, 102, 241), 55)
    draw_radial_glow(img, 800, 1000, 550, (16, 185, 129), 40)
    
    draw = ImageDraw.Draw(img)
    
    # Grid accents
    for gx in range(50, width, 100):
        for gy in range(50, height, 100):
            draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(255, 255, 255, 18))

    # --- LEFT SIDE: HERO TITLE & MISSION SPECS ---
    font_badge = get_font("segoeuib.ttf", 26)
    font_h1 = get_font("segoeuib.ttf", 68)
    font_h2 = get_font("segoeuib.ttf", 44)
    font_body = get_font("segoeui.ttf", 28)
    font_feature = get_font("segoeuib.ttf", 28)
    
    # Top badge
    draw.rounded_rectangle([100, 110, 520, 165], radius=28, fill=(37, 99, 235, 180), outline=(96, 165, 250), width=2)
    draw.text((310, 137), "GOOGLE GEMINI × HANDSHAKE", fill=(255, 255, 255), font=font_badge, anchor="mm")
    
    # Main Headline
    draw.text((100, 205), "Your Deadline, Your Design:", fill=(255, 255, 255), font=font_h1)
    draw.text((100, 285), "Countdown Lock Screen", fill=(56, 189, 248), font=font_h1)
    
    # Subtitle
    draw.text((100, 395), "Mission: 6:00 PM Sprint Countdown", fill=(226, 232, 240), font=font_h2)
    
    desc_lines = [
        "A focused AI-assisted milestone architecture designed to turn an",
        "intense 7-hour sprint into clear, actionable backward checkpoints.",
        "Engineered with high-contrast glassmorphic design, clock clearance,",
        "and interactive checkbox milestones to guarantee delivery."
    ]
    for idx, line in enumerate(desc_lines):
        draw.text((100, 480 + idx * 40), line, fill=(148, 163, 184), font=font_body)

    # Feature Highlights (Cards on Left Bottom)
    features = [
        ("🎯", "AI Backward Planning", "5 T-Minus milestones under 5 words"),
        ("📱", "Dynamic 9:16 Design", "Clock clearance & glassmorphic cards"),
        ("⚡", "Sprint Accountability", "Pre-set daily & hourly reminder triggers")
    ]
    
    for i, (icon, ftitle, fdesc) in enumerate(features):
        fy = 690 + (i * 125)
        draw.rounded_rectangle([100, fy, 820, fy + 105], radius=20, fill=(15, 23, 42, 220), outline=(51, 65, 85, 200), width=2)
        # Icon circle
        draw.ellipse([125, fy + 22, 185, fy + 82], fill=(30, 41, 59), outline=(56, 189, 248, 160), width=2)
        draw.text((155, fy + 52), icon, font=font_badge, anchor="mm")
        
        draw.text((210, fy + 24), ftitle, fill=(255, 255, 255), font=font_feature)
        draw.text((210, fy + 62), fdesc, fill=(148, 163, 184), font=font_body)

    # --- RIGHT SIDE: PHONE MOCKUP SHOWCASING LOCKSCREEN ---
    phone_w, phone_h = 490, 870
    phone_x, phone_y = 1130, 165
    
    # Phone outer shadow / glow
    shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    for s in range(50, 0, -5):
        sdraw.rounded_rectangle([phone_x - s, phone_y - s, phone_x + phone_w + s, phone_y + phone_h + s], radius=50 + s, fill=(0, 0, 0, int(90 * (1 - s/50))))
    img.alpha_composite(shadow_layer)
    
    draw = ImageDraw.Draw(img)
    # Phone titanium bezel
    draw.rounded_rectangle([phone_x - 12, phone_y - 12, phone_x + phone_w + 12, phone_y + phone_h + 12], radius=52, fill=(30, 41, 59), outline=(94, 234, 212, 140), width=3)
    # Inner border
    draw.rounded_rectangle([phone_x - 4, phone_y - 4, phone_x + phone_w + 4, phone_y + phone_h + 4], radius=44, fill=(15, 23, 42))

    # Paste resized lockscreen into phone screen
    lock_img = Image.open(lockscreen_path).convert("RGBA")
    lock_resized = lock_img.resize((phone_w, phone_h), Image.Resampling.LANCZOS)
    
    # Mask rounded corners of screen
    mask = Image.new("L", (phone_w, phone_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, phone_w, phone_h], radius=40, fill=255)
    
    img.paste(lock_resized, (phone_x, phone_y), mask)
    
    # Phone Dynamic Island / Speaker notch at top
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([phone_x + phone_w//2 - 60, phone_y + 14, phone_x + phone_w//2 + 60, phone_y + 38], radius=12, fill=(0, 0, 0))
    
    # Floating Pill badge on right
    draw.rounded_rectangle([phone_x + phone_w - 240, phone_y + phone_h - 70, phone_x + phone_w + 50, phone_y + phone_h - 15], radius=25, fill=(16, 185, 129, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((phone_x + phone_w - 95, phone_y + phone_h - 42), "✓ READY TO SUBMIT", fill=(255, 255, 255), font=font_badge, anchor="mm")

    img.save(output_path, "PNG")
    print(f"Generated Handshake 3:2 cover preview saved to {output_path}")
    return output_path

if __name__ == "__main__":
    lock_path = generate_lockscreen("countdown_lockscreen_9_16.png")
    generate_handshake_cover(lock_path, "handshake_cover_preview_3_2.png")
