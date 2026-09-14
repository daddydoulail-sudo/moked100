"""Generates all narration (Hebrew, Microsoft neural voices via edge-tts) and
sound effects (synthesised with numpy) for the game.

    python3 tools/make_audio.py           # everything
    python3 tools/make_audio.py sfx       # only sound effects
    python3 tools/make_audio.py tts       # only narration

The narration text is also written to src/data/lines.json so the UI shows the
same sentence it speaks.
"""
import asyncio
import json
import math
import os
import struct
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..")
AUDIO = os.path.join(ROOT, "src", "assets", "audio")
DATA = os.path.join(ROOT, "src", "data")
os.makedirs(AUDIO, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

DISPATCHER = "he-IL-HilaNeural"
COMMANDER = "he-IL-AvriNeural"
MAN = "he-IL-AvriNeural"
WOMAN = "he-IL-HilaNeural"

# id: (voice, text, rate)
LINES = {
    # dispatcher / guidance
    "welcome": (DISPATCHER, "מוקד מאה, ערב טוב. השוטר התורן מתבקש להתחיל משמרת.", "-5%"),
    "ring": (DISPATCHER, "קריאה נכנסת למוקד. ענה לשיחה.", "-5%"),
    "watch": (DISPATCHER, "מעביר אותך לשידור חי ממצלמת האבטחה באזור.", "-5%"),
    "pick_place": (DISPATCHER, "סמן במפה את מקום האירוע.", "-5%"),
    "pick_unit": (DISPATCHER, "בחר את הכוח שנשלח לאירוע.", "-5%"),
    "wrong_place": (DISPATCHER, "שלילי, זה לא מקום האירוע. בדוק שוב.", "-5%"),
    "hint_place": (DISPATCHER, "המוקד מסמן לך את המיקום במפה.", "-5%"),
    "wrong_unit": (DISPATCHER, "יש כוח מתאים יותר לאירוע הזה. בחר שוב.", "-5%"),
    "dispatched": (DISPATCHER, "הכוח יצא לדרך. זמן הגעה משוער: שתי דקות.", "-5%"),
    "arrived": (DISPATCHER, "הכוח הגיע למקום. יש למלא דוח אירוע.", "-5%"),
    "report_q1": (DISPATCHER, "מה קרה?", "-10%"),
    "report_q2": (DISPATCHER, "מי צריך עזרה?", "-10%"),
    "report_q3": (DISPATCHER, "מה השוטרים צריכים לעשות?", "-10%"),
    "correct": (DISPATCHER, "אושר. ממשיכים.", "-5%"),
    "wrong": (DISPATCHER, "שלילי. בדוק שוב.", "-5%"),
    "report_done": (DISPATCHER, "הדוח נשלח למפקד התחנה לאישור.", "-5%"),
    # callers
    "call_home_burglary": (MAN, "הלו, משטרה? אני רואה מישהו עם קפוצ'ון נכנס לדירה של השכנים שלי ברחוב הגפן. הם לא בבית!", "+0%"),
    "call_shop_breakin": (MAN, "כאן השומר של קניון השוק. יש מישהו שמנסה לפתוח את המנעול של אחת החנויות, עכשיו, באמצע הלילה.", "+0%"),
    "call_car_breakin": (MAN, "שלום, אני שומר בחניון המרכזי. יש בחור עם מסכה שפורץ לרכב לבן בקומה שתיים.", "+0%"),
    "call_bag_snatch": (WOMAN, "הלו! מישהו חטף עכשיו תיק מאישה ברחוב הרצל וברח לכיוון השוק!", "+5%"),
    "call_lost_child": (WOMAN, "שלום, אני בפארק העיר ליד השער הראשי. יש כאן ילד קטן שמסתובב לבד, אני לא רואה הורים.", "+0%"),
    "call_cat_tree": (WOMAN, "היי, החתול שלנו תקוע על עץ בגינת הפרחים ויש כלב שעומד מתחת ולא נותן לו לרדת.", "+0%"),
    "call_red_light": (MAN, "מונית עברה עכשיו באור אדום בצומת העצמאות, ממש כשאנשים חצו במעבר החצייה!", "+0%"),
    # resolutions
    "done_home_burglary": (DISPATCHER, "הניידת הגיעה. הפורץ נעצר בתוך הדירה, והחפצים הוחזרו לבעלים.", "-5%"),
    "done_shop_breakin": (DISPATCHER, "השוטרים תפסו את הפורץ ליד דלת החנות לפני שהספיק להיכנס.", "-5%"),
    "done_car_breakin": (DISPATCHER, "הפורץ נתפס בחניון. הרכב נבדק ובעל הרכב עודכן.", "-5%"),
    "done_bag_snatch": (DISPATCHER, "האופנוע השיג את החוטף אחרי מרדף קצר. התיק הוחזר לבעלים.", "-5%"),
    "done_lost_child": (DISPATCHER, "השוטר הקהילתי נשאר עם הילד עד שההורים נמצאו. הכל בסדר.", "-5%"),
    "done_cat_tree": (DISPATCHER, "השוטר הרחיק את הכלב והוריד את החתול בשלום.", "-5%"),
    "done_red_light": (DISPATCHER, "ניידת התנועה עצרה את המונית. הנהג קיבל דוח על נסיעה באור אדום.", "-5%"),
    # commander
    "cmd_3": (COMMANDER, "טיפול מצוין באירוע. שלושה כוכבים. כל הכבוד, ככה עובדים במשטרה.", "-5%"),
    "cmd_2": (COMMANDER, "טיפול טוב. שני כוכבים. שים לב לפרטים בפעם הבאה.", "-5%"),
    "cmd_1": (COMMANDER, "האירוע טופל, אבל היו טעויות. כוכב אחד. נתאמן ונשתפר.", "-5%"),
    "cmd_rankup": (COMMANDER, "מזל טוב. בהחלטת מפקד התחנה, אתה מקודם בדרגה.", "-5%"),
    "cmd_intro": (COMMANDER, "אני מפקד התחנה. אני אבדוק כל דוח שלך ואתן לך ציון.", "-5%"),
    # unit names (spoken when a unit card is pressed and held)
    "unit_patrol": (DISPATCHER, "ניידת סיור", "-5%"),
    "unit_moto": (DISPATCHER, "אופנוע משטרה", "-5%"),
    "unit_traffic": (DISPATCHER, "ניידת תנועה", "-5%"),
    "unit_community": (DISPATCHER, "שוטר קהילתי", "-5%"),
    # rank names
    "rank_0": (COMMANDER, "שוטר", "-5%"),
    "rank_1": (COMMANDER, "סמל", "-5%"),
    "rank_2": (COMMANDER, "רב סמל ראשון", "-5%"),
    "rank_3": (COMMANDER, "קצין", "-5%"),
    "rank_4": (COMMANDER, "מפקד", "-5%"),
}

# report answer options, read aloud when the child presses the speaker button
OPTIONS = {
    "home_burglary": ("פורץ נכנס לדירה", "בעלי הדירה", "לתפוס את הפורץ ולאבטח את הדירה"),
    "shop_breakin": ("פורץ פותח מנעול של חנות בלילה", "בעל החנות", "לתפוס את הפורץ לפני שייכנס"),
    "car_breakin": ("מישהו פורץ למכונית", "בעל הרכב", "לתפוס את הפורץ בחניון"),
    "bag_snatch": ("מישהו חטף תיק מאישה וברח", "האישה שהתיק שלה נחטף", "לרדוף אחרי החוטף ולהחזיר את התיק"),
    "lost_child": ("ילד קטן נמצא לבד בלי הורים", "הילד", "להישאר עם הילד ולמצוא את ההורים"),
    "cat_tree": ("חתול תקוע על עץ וכלב מתחתיו", "החתול", "להרחיק את הכלב ולהוריד את החתול"),
    "red_light": ("מונית עברה באור אדום", "הולכי הרגל במעבר החצייה", "לעצור את הנהג ולתת לו דוח"),
}
for _sid, _texts in OPTIONS.items():
    for _q, _t in zip(("what", "who", "action"), _texts):
        LINES[f"opt_{_sid}_{_q}"] = (DISPATCHER, _t, "-5%")

SR = 44100


def write_wav(name, samples):
    samples = np.clip(samples, -1, 1)
    path = os.path.join(AUDIO, name + ".wav")
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((samples * 32767).astype("<i2").tobytes())
    # convert to mp3 so every effect shares one format
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-codec:a", "libmp3lame", "-q:a", "4",
                    os.path.join(AUDIO, name + ".mp3")], check=True)
    os.remove(path)


def tone(freq, dur, vol=0.5, shape="sine", attack=0.01, release=0.05):
    n = int(SR * dur)
    t = np.arange(n) / SR
    if shape == "square":
        s = np.sign(np.sin(2 * np.pi * freq * t))
    elif shape == "tri":
        s = 2 * np.abs(2 * ((t * freq) % 1) - 1) - 1
    else:
        s = np.sin(2 * np.pi * freq * t)
    env = np.ones(n)
    a, r = int(SR * attack), int(SR * release)
    env[:a] = np.linspace(0, 1, a)
    env[n - r:] = np.linspace(1, 0, r)
    return s * env * vol


def silence(dur):
    return np.zeros(int(SR * dur))


def make_sfx():
    # phone ring: two short trills, repeated
    trill = np.concatenate([tone(880, 0.05, 0.4, "tri") + tone(1320, 0.05, 0.2, "tri") for _ in range(12)])
    ring = np.concatenate([trill, silence(0.25), trill, silence(1.2)])
    write_wav("sfx_ring", np.tile(ring, 2))

    # siren: sweeping between two pitches, 3 seconds
    n = int(SR * 3.0)
    t = np.arange(n) / SR
    f = 700 + 300 * np.sin(2 * np.pi * 0.8 * t)
    phase = 2 * np.pi * np.cumsum(f) / SR
    siren = np.sin(phase) * 0.35
    env = np.ones(n)
    env[-SR // 2:] = np.linspace(1, 0, SR // 2)
    write_wav("sfx_siren", siren * env)

    # click
    write_wav("sfx_click", tone(1200, 0.06, 0.4, "sine", release=0.04))

    # correct ding: rising major arpeggio
    write_wav("sfx_correct", np.concatenate([tone(523, 0.12, 0.4), tone(659, 0.12, 0.4), tone(784, 0.25, 0.45)]))

    # wrong: soft low double tone (not scary)
    write_wav("sfx_wrong", np.concatenate([tone(300, 0.15, 0.3, "tri"), silence(0.05), tone(250, 0.25, 0.3, "tri")]))

    # star: sparkle
    write_wav("sfx_star", np.concatenate([tone(1047, 0.08, 0.35), tone(1319, 0.08, 0.35), tone(1568, 0.08, 0.35), tone(2093, 0.3, 0.4)]))

    # fanfare for the commander screen
    fan = np.concatenate([tone(523, 0.18, 0.4, "tri"), tone(659, 0.18, 0.4, "tri"), tone(784, 0.18, 0.4, "tri"),
                          tone(1047, 0.5, 0.45, "tri")])
    write_wav("sfx_fanfare", fan)

    # radio beep (dispatch confirmation)
    write_wav("sfx_radio", np.concatenate([tone(1500, 0.08, 0.3, "square"), silence(0.05), tone(1500, 0.08, 0.3, "square")]))
    print("sfx done")


async def make_tts():
    import edge_tts
    proxy = os.environ.get("HTTPS_PROXY")
    for key, (voice, text, rate) in LINES.items():
        out = os.path.join(AUDIO, f"{key}.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            continue
        for attempt in range(3):
            try:
                c = edge_tts.Communicate(text, voice, rate=rate, proxy=proxy)
                await c.save(out)
                break
            except Exception as e:  # noqa: BLE001
                print("retry", key, e)
                await asyncio.sleep(2)
        print("tts", key)
    with open(os.path.join(DATA, "lines.json"), "w", encoding="utf-8") as f:
        json.dump({k: v[1] for k, v in LINES.items()}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "sfx"):
        make_sfx()
    if what in ("all", "tts"):
        asyncio.run(make_tts())
