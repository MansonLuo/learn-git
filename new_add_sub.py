# this script used to add subtitles extracted from srt file to youtube video

import os
import copy

MAX_INSTANCES = 40  # the number of clips to be processed as the same time

class CustomError(Exception):
    def __init__(self, msg):
        self.msg = msg


def extractSubtitles(srt_path):
    if not os.path.isfile(srt_path):
        raise CustomError('srt file does not exist.')

    with open(srt_path) as f:
        lines = f.readlines()

    # extract info blocks
    block = []
    blocks = []
    LENGTH = 3
    
    for l in lines:
        l = l.strip()

        ## discard lines without chars
        if len(l) == 0:
            continue
        ## filter real subtitle lines
        block.append(l)

        if block[-1].isdigit():
            if (len(block) - 1) ==  LENGTH:
                block.pop()  # discard last index char
                # check wheth this block contained 3 lines is a real subtitles
                if '[' in block[-1]:
                    # discard all data within block
                    block.clear()
                    block = []
                    block.append(l)
                    continue

                # add real subtitles
                blocks.append(copy.deepcopy(block))
                block.clear()
                block = []
                block.append(l)
            else:
                # this block just contain two lines datas
                block.clear()
                block = []
                block.append(l)
                continue
        continue

    # Generate data structure containing two datas, first represent start time,
    # the other represent subtitle
    datas = []

    for blk in blocks:
        data = []

        #generate start seconds
        time, msec = blk[1].split("-->")[0].split(',')
        hour, minute, second = time.split(':')
        express = "{h}*60*60 + {m}*60 + {s}"
        start_seconds = eval(
            express.format(
                h=int(hour),
                m=int(minute),
                s=int(second)
            )
        )
        str_start_seconds = str(start_seconds) + '.' + msec

        # conposite data structure
        data.append(str_start_seconds)
        data.append(blk[2])

        datas.append(copy.deepcopy(data))
        
    return datas

def cleanSubtitles(datas, clip_size, end_time):
    """
        #1 decrease each time within subclip to appropriate time
        #2 append subclip a edge time representing the end time of subclip
        #3 append each subclip datas to a new list
    """

    # add start time and end time
    msg = ''
    datas.insert(0, [0, msg])
    datas.append([end_time, msg])

    #divide datas into subclips
    all_clips = []
    clip = []
    for i in range(len(datas)):
        i = i + 1 # index based 1

        clip.append(copy.deepcopy(datas[i-1]))
        if (i // clip_size == 0) or (i == len(datas)):
            all_clips.append(copy.deepcopy(clip))
            clip = []

    # add edge end time
    clip = None
    for i in range(len(all_clips) - 1):
        clip = all_clips[i]
        clip.append(
            copy.deepcopy(
                all_clips[i+1][0]
            )
        )
    
    # reduce subtitle's start time
    for clip in all_clips[1:]:
        start_time = float(clip[0][0])
        for subtitle in clip:
                subtitle[0] = float(subtitle[0]) - start_time

    return all_clips


def generateVideo(video_path, subtitles):
    if not os.path.isfile(video_path):
        raise CustomError('video file doesnt exist')

    numbers_of_videoclips = len(subtitles) + 2  # add first clip and last clip
    count, mod = divmod(numbers_of_videoclips, MAX_INSTANCE)
    if mod != 0:
        count = count + 1
    
    # clean subtitle time
    subtitles = cleanSubtitles(subtitles)

    # generate composited sublicp one by one
    for i  in range(count):
        pass




def addSubtitle(video_path, srt_path):
    subtitles = extractSubtitles(srt_path)
    generateVideo(video_path, subtitles)

subtitles = extractSubtitles('./test.srt')
all_clips = cleanSubtitles(subtitles, MAX_INSTANCES, 914.36)

for i in range(len(all_clips)):
    print('clip {}:'.format(i))
    for subtitle in all_clips[i]:
        print(subtitle)
    print()
    print()
