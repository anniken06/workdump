import os
import re
import time
import youtube_dl


dir_path = os.path.dirname(os.path.realpath(__file__))
dl_path = os.path.join(dir_path, 'ytdownloads')
download_urls = [
### Python ###
    "https://app.pluralsight.com/library/courses/python-fundamentals/table-of-contents", 
    "https://app.pluralsight.com/library/courses/python-beyond-basics/table-of-contents", 
    "https://app.pluralsight.com/library/courses/python-design-patterns/table-of-contents",
    "https://app.pluralsight.com/library/courses/python-developers-toolkit/table-of-contents", 
    "https://app.pluralsight.com/library/courses/play-by-play-zed-shaw/table-of-contents",
### Java ###
    "https://app.pluralsight.com/library/courses/java-fundamentals-core-platform/table-of-contents",
    "https://app.pluralsight.com/library/courses/spring-fundamentals/table-of-contents", 
    "https://app.pluralsight.com/library/courses/design-patterns-java-creational/table-of-contents",
    "https://app.pluralsight.com/library/courses/design-patterns-java-structural/table-of-contents",
    "https://app.pluralsight.com/library/courses/design-patterns-java-behavioral/table-of-contents",
    "https://app.pluralsight.com/library/courses/java-8-whats-new/table-of-contents",
    "https://app.pluralsight.com/library/courses/java-functional-programming/table-of-contents",
### TensorFlow ###
    "https://app.pluralsight.com/library/courses/tensorflow-understanding-foundations/table-of-contents",
    "https://app.pluralsight.com/library/courses/tensorflow-getting-started/table-of-contents",
### Git ###
    "https://app.pluralsight.com/library/courses/how-git-works/table-of-contents",
### Raspberry Pi ###
    "https://app.pluralsight.com/library/courses/home-automation-fundamentals/table-of-contents",
]
ydl_opts = {
    'username': 'jp-gaming',
    'password': 'zxasqwQW!2',
    'sleep_interval': 65,
}


def beep(times=1, interval=1):
    for _ in range(times):
        print("\a")
        time.sleep(interval)

def write_finished(url):
    try:
        with open(os.path.join(dir_path, "finished_urls.txt"), "a") as ffile:
            ffile.write(url + "\n")
    except Exception as e:
        print(e)

def read_finished():
    try:
        with open(os.path.join(dir_path, "finished_urls.txt"), "r") as ffile:
            return ffile.readlines()
    except Exception as e:
        print(e)
        return []

while True:
    try:
        finished_urls = read_finished()
        for url in download_urls:
            #write_finished(url)
            #finished_urls = read_finished()
            if url + "\n" in finished_urls:
                print("Skipping already finished url: ", url)
                continue
            #else:
            #    import code; code.interact(local={**locals(), **globals()})
            out_path = re.search(r'courses/(.+?)/', url).group(1)
            out_dir = os.path.join(dl_path, out_path)
            if not os.path.exists(out_dir): os.makedirs(out_dir)
            new_outtmpl = "%(playlist_index)s--" + youtube_dl.utils.DEFAULT_OUTTMPL
            ydl_opts['outtmpl'] = os.path.join(out_dir, new_outtmpl)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                beep()
                write_finished(url)
    except Exception as e:
        print(e)
        beep(10)
