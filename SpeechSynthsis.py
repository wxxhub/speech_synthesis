#coding=utf-8

import re
from time import ctime, sleep

import numpy as np
from ChineseTone import *
from speech_synthesis.NumToChinese import numToChinese
from speech_synthesis.ToAudio import ToAudio


class SpeechSynthsis:
    punctuation = " ,！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
    @classmethod
    def __init__(self, goal_frequency):
        self.to_audio = ToAudio(goal_frequency)

    @classmethod
    def synthesis(self, content):
        split_contents = re.split(u"[%s]+"%self.punctuation, content)

        play_content = []
        for split_content in split_contents:
            split_content = numToChinese(str(split_content))
            pinyins = PinyinHelper.convertToPinyinFromSentence(split_content, pinyinFormat=PinyinFormat.WITH_TONE_NUMBER)

            for pin_yin in pinyins:
                tone = re.sub(u"([^\u0030-\u0039])", "", pin_yin)
                pronounce = re.sub(u"([^\u0061-\u007a])", "", pin_yin)
                play_content.append(pronounce + tone)
            
            
            play_content.append('')

        ok, result = self.to_audio.synthesis(play_content, 123)
        return ok ,result
    
    @classmethod
    def setFile(self, cache_file, voice_file):
        self.to_audio.setFile(cache_file, voice_file)
        pass

    @classmethod
    def dataEmpty(self):
        return self.to_audio.dataEmpty()
    
    @classmethod
    def reset(self):
        self.to_audio.reset()
        pass
    
    @classmethod
    def playing(self):
        return self.to_audio.playing_

    @classmethod
    def close(self):
        pass