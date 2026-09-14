"""Turns stock clips into security-camera footage for the game.

Each entry in CLIPS is downloaded (free Mixkit / Pexels licenses, see
CREDITS.md), trimmed, converted to 16:9, desaturated a little, given a CCTV
overlay (camera label, running timestamp, REC dot) and saved as
src/assets/video/<id>.mp4 plus a poster image <id>.jpg.

To swap a clip for your own footage, drop a file at tools/_work/<id>.mp4
(any size, any length) and re-run: local files are never re-downloaded.

    python3 tools/process_stock.py            # all clips
    python3 tools/process_stock.py cat_tree   # one clip
"""
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(__file__), "..")
WORK = os.path.join(os.path.dirname(__file__), "_work")
OUT = os.path.join(ROOT, "src", "assets", "video")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
W, H = 960, 540

# id: (url, start_seconds, length_seconds, camera label, clock start, vertical?)
CLIPS = {
    "home_burglary": ("https://assets.mixkit.co/videos/31372/31372-720.mp4", 2, 12, "CAM 07  REHOV HAGEFEN 12", "02:32:10", False),
    "shop_breakin":  ("https://assets.mixkit.co/videos/31380/31380-720.mp4", 1, 12, "CAM 03  KENYON HASHUK", "01:14:52", False),
    "car_breakin":   ("https://assets.mixkit.co/videos/31363/31363-720.mp4", 0, 12, "CAM 04  HANYON MERKAZ", "23:41:05", False),
    "bag_snatch":    ("https://assets.mixkit.co/videos/31359/31359-720.mp4", 0, 7.5, "CAM 11  REHOV HERZL", "18:05:33", False),
    "lost_child":    ("https://videos.pexels.com/video-files/19735477/19735477-uhd_1440_2560_30fps.mp4", 0, 12, "CAM 06  PARK HAIR", "16:20:47", True),
    "cat_tree":      ("https://videos.pexels.com/video-files/34285395/14525591_1450_1440_30fps.mp4", 2, 12, "CAM 08  GINAT HAPRAHIM", "10:12:09", True),
    "red_light":     ("https://assets.mixkit.co/videos/4272/4272-720.mp4", 6, 12, "CAM 02  TSOMET HAATSMAUT", "08:47:21", False),
}


def fetch(cid, url):
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, f"{cid}.mp4")
    if os.path.exists(path) and os.path.getsize(path) > 100_000:
        return path
    print("downloading", cid)
    urllib.request.urlretrieve(url, path)
    return path


def process(cid):
    url, start, length, label, clock, vertical = CLIPS[cid]
    src = fetch(cid, url)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"{cid}.mp4")
    if vertical:
        # blurred copy fills the frame, the sharp clip sits in the middle
        fit = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
               f"gblur=sigma=30,eq=brightness=-0.15[bg];"
               f"[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0")
    else:
        fit = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    hh, mm, ss = (int(x) for x in clock.split(":"))
    base = hh * 3600 + mm * 60 + ss
    clock_expr = (f"%{{eif\\:mod(({base}+t)/3600\\,24)\\:d\\:2}}\\:"
                  f"%{{eif\\:mod(({base}+t)/60\\,60)\\:d\\:2}}\\:"
                  f"%{{eif\\:mod({base}+t\\,60)\\:d\\:2}}")
    vf = (
        f"{fit},"
        "eq=saturation=0.55:contrast=1.08,"
        "noise=alls=8:allf=t,"
        f"drawbox=x=0:y=0:w=iw:h=44:color=black@0.45:t=fill,"
        f"drawtext=fontfile={FONT}:text='{label}':x=18:y=12:fontsize=22:fontcolor=white,"
        f"drawtext=fontfile={FONT}:text='14/09/2026  {clock_expr}':x=w-tw-18:y=12:fontsize=22:fontcolor=white,"
        f"drawtext=fontfile={FONT}:text='REC':x=18:y=h-38:fontsize=22:fontcolor=red:enable='lt(mod(t\\,1)\\,0.6)',"
        "drawbox=x=0:y=ih-4:w=iw:h=4:color=black@0.6:t=fill"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-t", str(length), "-i", src,
           "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "26",
           "-movflags", "+faststart", "-r", "25", out]
    subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(length * 0.5), "-i", out, "-frames:v", "1",
                    "-vf", "scale=480:-1", os.path.join(OUT, f"{cid}.jpg")], check=True)
    print("done", cid, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    wanted = sys.argv[1:] or list(CLIPS)
    for cid in wanted:
        process(cid)
