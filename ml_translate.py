import os
import sys
import torch
import warnings
import subprocess
import re
from pathlib import Path
import srt
from transformers import T5ForConditionalGeneration, T5Tokenizer
import signal

# ---------------- КОНФИГУРАЦИЯ ----------------
MODEL_NAME = "utrobinmv/t5_translate_en_ru_zh_large_1024"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 20
PREFIX = "translate to ru: "
# ----------------------------------------------

# Глобальная переменная для остановки при Ctrl+C
STOP_PROCESS = False

def signal_handler(sig, frame):
    global STOP_PROCESS
    print("\n[MAIN] KeyboardInterrupt получен! Завершаем...")
    STOP_PROCESS = True

signal.signal(signal.SIGINT, signal_handler)

warnings.filterwarnings("ignore", category=UserWarning)

def load_translator():
    print(f"[GPU] Загружаю модель на {DEVICE}...")
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16
    )
    model.to(DEVICE)
    model.eval()
    print("[GPU] Модель готова.")
    return model, tokenizer

def translate_batch(model, tokenizer, texts, prefix):
    inputs = [prefix + text for text in texts]

    # вычисляем максимальную длину для очень длинных субтитров
    max_input_len = max(len(tokenizer.encode(t, add_special_tokens=True)) for t in inputs)
    max_tokens = max(max_input_len * 2, 4096)  # умножаем на 2, чтобы хватило для перевода

    encodings = tokenizer(
        inputs,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_tokens
    ).to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **encodings,
            max_new_tokens=max_tokens,
            num_beams=4,
            early_stopping=True,
            do_sample=False
        )
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)

def print_progress(file_name, processed, total):
    percent = (processed / total) * 100
    bar_length = 30
    filled = int(bar_length * processed // total)
    bar = '#' * filled + '.' * (bar_length - filled)
    sys.stdout.write(f"\r  → {file_name}: |{bar}| {percent:.1f}% ({processed}/{total})")
    sys.stdout.flush()

def extract_subtitles(video_path):
    """
    Извлекает первый поток субтитров, возвращает путь к .srt.
    Bitmap субтитры (pgs) пропускаются.
    """
    temp_srt = str(Path(video_path).with_suffix(".extracted.srt"))

    cmd_info = ["ffmpeg", "-i", video_path, "-hide_banner"]
    result = subprocess.run(cmd_info, stderr=subprocess.PIPE, text=True, encoding="utf-8")

    subtitle_streams = []
    for line in result.stderr.splitlines():
        if "Subtitle" in line and "hdmv_pgs_subtitle" not in line.lower():
            stream_match = re.search(r"Stream #(\d+:\d+)", line)
            if stream_match:
                stream_id = stream_match.group(1)
                lang_match = re.search(r"\((\w+)\)", line)
                lang = lang_match.group(1).lower() if lang_match else "und"
                subtitle_streams.append((stream_id, lang))

    if not subtitle_streams:
        return False, ""

    stream_id, lang = subtitle_streams[0]
    ru_srt_path = str(Path(video_path).with_suffix(".ru.srt"))
    if os.path.exists(ru_srt_path):
        return False, ""  # уже есть перевод

    if lang == "rus":
        return False, ""  # Русские субтитры уже есть → пропускаем

    cmd_extract = [
        "ffmpeg", "-i", video_path,
        "-map", stream_id,
        "-c", "copy",
        temp_srt,
        "-y"
    ]
    result_extract = subprocess.run(cmd_extract, stderr=subprocess.PIPE)
    if result_extract.returncode != 0 or not os.path.exists(temp_srt):
        return False, ""

    return True, temp_srt

def process_file(video_path, model, tokenizer):
    global STOP_PROCESS
    file_name = Path(video_path).name
    print(f"\n[PROCESS] {file_name}")

    if STOP_PROCESS:
        return

    success, temp_srt = extract_subtitles(video_path)
    if not success:
        print(f"[SKIP] Нет субтитров или они уже на русском: {file_name}")
        return

    try:
        with open(temp_srt, "r", encoding="utf-8") as f:
            subs = list(srt.parse(f.read()))

        if not subs:
            print(f"[SKIP] Пустые субтитры: {file_name}")
            os.remove(temp_srt)
            return

        total_lines = len(subs)
        translated_texts = []

        for i in range(0, total_lines, BATCH_SIZE):
            if STOP_PROCESS:
                print(f"[STOP] Прерывание перевода: {file_name}")
                return
            batch = [sub.content for sub in subs[i:i+BATCH_SIZE]]
            translated = translate_batch(model, tokenizer, batch, PREFIX)
            translated_texts.extend(translated)
            print_progress(file_name, min(i+BATCH_SIZE, total_lines), total_lines)

        print()  # новая строка после прогресса

        # Обновляем содержимое субтитров
        for idx, sub in enumerate(subs):
            sub.content = translated_texts[idx]

        # Сохраняем переведённые субтитры рядом с видео
        temp_trans_srt = str(Path(video_path).with_suffix(".ru.srt"))
        with open(temp_trans_srt, "w", encoding="utf-8-sig", newline="\n") as f:
            f.write(srt.compose(subs))

        print(f"[OK] Сохранено: {temp_trans_srt}")
        os.remove(temp_srt)

    except Exception as e:
        print(f"[ERR] Ошибка при обработке {file_name}: {e}")
        if os.path.exists(temp_srt):
            os.remove(temp_srt)

def find_video_files(root_dir):
    exts = [".mkv", ".mp4", ".avi", ".mov", ".wmv"]
    folders = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        video_files = [os.path.join(dirpath, f) for f in filenames if Path(f).suffix.lower() in exts]
        if video_files:
            folders[dirpath] = sorted(video_files)
    return folders

def main():
    global STOP_PROCESS
    root_dir = input("Папка с видео: ").strip() or "."
    root_dir = os.path.abspath(root_dir)
    print(f"[AUTO] Скрипт запущен в папке:\n{root_dir}")

    folders = find_video_files(root_dir)
    total_videos = sum(len(v) for v in folders.values())
    print(f"[INFO] Найдено видеофайлов: {total_videos}")

    model, tokenizer = load_translator()

    for folder, files in folders.items():
        if STOP_PROCESS:
            break
        print(f"\n[INFO] Обработка папки: {folder} ({len(files)} файлов)")
        for vf in files:
            if STOP_PROCESS:
                break
            process_file(vf, model, tokenizer)

    print("\n=== ВСЁ ГОТОВО ===")

if __name__ == "__main__":
    main()
