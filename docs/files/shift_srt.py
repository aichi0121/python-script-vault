import re
import os
import glob

# ====== 設定區 ======
OFFSET_SECONDS = 1.30
INPUT_FOLDER = "."
OUTPUT_FOLDER = "字幕修正完成"
# ====================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
offset_ms = int(round(OFFSET_SECONDS * 1000))

def time_to_ms(h, m, s, ms):
    return (int(h)*3600 + int(m)*60 + int(s)) * 1000 + int(ms)

def ms_to_time(total_ms, sep):
    if total_ms < 0:
        total_ms = 0
    h = total_ms // 3600000
    m = (total_ms % 3600000) // 60000
    s = (total_ms % 60000) // 1000
    ms = total_ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"

pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2})([,.])(\d{3})")

def shift_line(line):
    def replacer(match):
        h, m, s, sep, ms = match.groups()
        total = time_to_ms(h, m, s, ms) - offset_ms
        return ms_to_time(total, sep)
    return pattern.sub(replacer, line)

files = glob.glob(os.path.join(INPUT_FOLDER, "*.srt")) + \
        glob.glob(os.path.join(INPUT_FOLDER, "*.vtt"))

if not files:
    print("⚠️ 找不到任何 .srt 或 .vtt 檔案")
else:
    for filepath in files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = [shift_line(line) for line in lines]
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ 已處理: {filename}")

    print(f"\n🎉 全部完成!已輸出到「{OUTPUT_FOLDER}」資料夾")
