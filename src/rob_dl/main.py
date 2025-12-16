import yt_dlp
import argparse
import os
import shutil
import sys

def has_ffmpeg():
        return shutil.which("ffmpeg") is not None

####################
# File flag
####################

def rob_file(url): # Downloads a file from given url
    if not url:
        raise ValueError("No URL provided")

    output_filename = url.split("/")[-1]
    os.system(f'curl -L -o "{output_filename}" "{url}"')
    return output_filename

def rob_video(url, quality):
    if not url:
        raise ValueError("No URL provided")

    ffmpeg_installed = has_ffmpeg()

    if quality.isdigit():
        if ffmpeg_installed:
            format_string = f"bestvideo[height<={quality}]+bestaudio/best"
        else:
            format_string = f"best[height<={quality}]"
    else:
        format_string = quality if ffmpeg_installed else "best"

    ydl_opts = {
        "format": format_string,
        "merge_output_format": "mp4",
        "noplaylist": True
    }

    if not ffmpeg_installed:
        print("No ffmpeg installation found")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as error:
        raise RuntimeError(f"Download failed: {error}")


def rob_update():
    pm = input("Update using (1) pip or (2) uv?")
    if pm == "1":
        print("Updating rob using pip")
        os.system("pip install -U rob-dl")
    elif pm == "2":
        os.system("uv pip install -U rob-dl")
    else:
        print("Please input (1) pip or (2) uv")


def main():
    parser = argparse.ArgumentParser(description="rob - file and YouTube downloader")
    parser.add_argument("url", nargs="?", help="File URL or YouTube video URL")
    parser.add_argument("-q", "--quality", help="Video quality (e.g., 720, 480, best, worst)(to be used with -v)", default="best")
    parser.add_argument("-f", "--file", help="Download a normal file instead of a video", action="store_true")
    parser.add_argument("-v", "--video", help="Download a Youtube video", action="store_true")
    parser.add_argument("-u", "--update", help="Updates rob", action="store_true")

    args = parser.parse_args()

    try:
        if args.file:
            fileout = rob_file(args.url)
            print(f"File downloaded as '{fileout}'")

        elif args.video:
            videout = rob_video(args.url, args.quality)
            print(f"Video downloaded as '{videout}'")

        elif args.update:
            rob_update()

        else:
            print("Please provide a flag; -v for video, -f for file, or -u for updating rob")
    
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()