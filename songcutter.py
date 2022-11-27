from pydub import AudioSegment
import os
from parameters import *

TYPE_list = ["正常", "噪声"]

for TYPE in TYPE_list:

    for soundfile in os.listdir("database/" + TYPE):
        # 默认sample width为1 byte，即8 bits
        sound = AudioSegment.from_file("database/" + TYPE + "/" + soundfile)
        sound = sound.set_frame_rate(SAMPLE_RATE)

        seconds = [5, 10, 20]

        for sec in seconds:
            # 因此计算秒数的时候，要除以8
            sound_mid_len1 = sound[(20*SAMPLE_RATE)//8:(20*SAMPLE_RATE)//8+(sec*SAMPLE_RATE)//8]
            sound_mid_len1.export("query/"+TYPE+"/"+str(sec)+"s/"+soundfile.split(".")[0]+"_1.wav",
                                  format="wav")

            sound_mid_len2 = sound[len(sound)//2:len(sound)//2+(sec*SAMPLE_RATE)//8]
            sound_mid_len2.export("query/"+TYPE+"/"+str(sec)+"s/"+soundfile.split(".")[0]+"_2.wav",
                                  format="wav")

            sound_mid_len3 = sound[len(sound)-(30*SAMPLE_RATE)//8:len(sound)-(30*SAMPLE_RATE)//8+(sec*SAMPLE_RATE)//8]
            sound_mid_len3.export("query/"+TYPE+"/"+str(sec)+"s/"+soundfile.split(".")[0]+"_3.wav",
                                  format="wav")

