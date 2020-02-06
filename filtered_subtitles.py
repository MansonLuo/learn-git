from moviepy.editor import *


def getTime(raw_data):
    first, second = raw_data.split(',')

    msec = int(second)
    
    h, m, s = first.split(':')
    res_seconds = 0
    h = int(h)
    m = int(m)
    s = int(s)

    if s != 0:
        res_seconds += s
    if m != 0:
        res_seconds += m * 60
    if h != 0:
        res_seconds += h * 60 * 60

    return float(
            str(res_seconds) + '.' + str(msec)
            )

print(getTime('00:10:30,30'))

with open('subtitle.txt') as f:
    lines = f.readlines()

block = []
LENGTH = 3
line_index = 0
subtitles = []

for l in lines:
    l = l.strip()

    if not l:
        continue

    if l.isdigit():
        line_index = 0
        block = None
        block = []
    else:
        line_index += 1
    
    if line_index < LENGTH:
        block.append(l)

    if len(block) == 3:
        if '[' in block[-1]:
            continue
    else:
        continue
    
    subtitles.append(block)

# generate data format
datas = []
data = [] 

for blk in subtitles:
    data = []

    time = getTime(blk[1].split("-->")[0].strip())

    data.append(time)
    data.append(blk[2])
    
    datas.append(data)


# add subtitles
video = VideoFileClip('./output/youtube-1.mp4')
start_time = 0
end_time = video.duration



start_clip = video.subclip(0, datas[0][0])
sub_clip = None
txt_clip = None
composite_clip = None
all_clips = []

for i in range(len(datas) - 1):
    print(str(i) + ': ' + str(len(datas) - 2))
    sub_clip = None
    txt_clip = None
    composite_clip = None

    sub_clip = video.subclip(datas[i][0], datas[i+1][0])
    txt_clip = TextClip(datas[i][1], fontsize=40, color='red')
    txt_clip = txt_clip.set_pos('bottom').set_duration(
        datas[i+1][0] - datas[i][0]
    )
    composite_clip = CompositeVideoClip([sub_clip, txt_clip])
    all_clips.append(composite_clip)


#generate last clip
s_clip = video.subclip(datas[-1][0], end_time)
s_txt_clip = TextClip(datas[-1][1], fontsize=40, color='red')
s_txt_clip = s_txt_clip.set_pos('bottom').set_duration(end_time - datas[-1][0])
com_clip = CompositeVideoClip([s_clip, s_txt_clip])

all_clips.append(com_clip)


# insert first clip
all_clips.insert(0, start_clip)


# concatenate all clips
final_clip = concatenate_videoclips(all_clips)
final_clip.write_videofile('output-youtube.mp4')
