# this script used to add subtitles extracted from srt file to youtube video

import os
import copy
from moviepy.editor import *

MAX_INSTANCES = 40  # the number of clips to be processed as the same time

class CustomError(Exception):
    def __init__(self, msg):
        self.msg = msg

# get blocks, each block contains one subtitle block msg
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
    msg = 's'
    datas.insert(0, [0, msg])
    datas.append([end_time, msg])

    #divide datas into subclips
    all_clips = []
    clip = []
    for i in range(len(datas)):
        i = i + 1 # index based 1

        clip.append(copy.deepcopy(datas[i-1]))
        if (i % clip_size == 0) or (i == len(datas)):
            all_clips.append(copy.deepcopy(clip))
            clip = []

    # add edge end time
    clip = None
    # skip last clip
    for i in range(len(all_clips) - 1):
        all_clips[i].append(
            copy.deepcopy(
                all_clips[i+1][0]
            )
        )
    """    
    for clip in all_clips:
        for sub in clip:
            print(sub)
        print('*********************\n')
    """


    # reduce subtitle's start time
    print('number of clips: {}'.format(len(all_clips)))
    for i in range(len(all_clips[1:])):
        first_subtitle_start_time = all_clips[i + 1][0][0]
        print('count: {}'.format(i + 1))
        
        current_clip_length = len(all_clips[i + 1])
        for j in range(current_clip_length):
            start_time = all_clips[i+1][j][0]
            all_clips[i+1][j][0] = str(
                float(start_time) - float(first_subtitle_start_time)
            )

    return all_clips


def generateVideo(video_path, clips_of_subtitles):
    """
        #1 subclip video acording the duration of subclip within subtitles
        #2 process each small video file representing subclip, change it to more smaller files, and add subtitle for each of theme.
        #3 concatenate each small video file
    """
    if not os.path.isfile(video_path):
        raise CustomError('video file doesnt exist')
    
    video = VideoFileClip(video_path)
    print('create instance of VideoFileClip')
    video_name = 'video-{}.mp4'

    # generate small video file
    index = 1
    for clip in clips_of_subtitles:
        small_video = video.subclip(
            float(clip[0][0]),
            float(clip[-1][0])
        )
        print('create small video using video.subclip()')

        ## generate composite clip
        composited_clips = []
        for i in range(len(clip) - 1):
            txt_clip = TextClip(clip[i][1], fontsize=40, color='white')
            txt_clip = txt_clip.set_pos('bottom').set_duration(float(clip[i+1][0])  - float(clip[i][0]))
            txt_video_clip = small_video.subclip(float(clip[i][0]), float(clip[i+1][0]))
            composited_small_video = CompositeVideoClip([txt_video_clip, txt_clip])

            composited_clips.append(composited_small_video)
            txt_clip = None
            txt_video_clip = None
        
        small_video = concatenate_videoclips(composited_clips)
        print('i will save small video file')
        small_video.write_videofile('./' + video_name.format(index))
        print(video_name.format(index) + " has saved.")
        index += 1
	



def addSubtitle(video_path, srt_path):
    subtitles = extractSubtitles(srt_path)
    generateVideo(video_path,
            cleanSubtitles(subtitles, MAX_INSTANCES, 550.84))

addSubtitle('./youtube.mp4', 'english.srt')

