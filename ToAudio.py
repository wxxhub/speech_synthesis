#coding=utf-8

import wave
import os
from pydub import AudioSegment
import numpy as np
import struct

class ToAudio:
    play_num_ = 0
    cache_file_num = 0
    cache_file_ = "cache"
    voice_file_ = "wav"

    __voice_cache = dict()
    __params = []

    @classmethod
    def __init__(self, goal_frequency = 16000):
        # create cache file
        self.enable_ = True
        if not os.path.exists(self.cache_file_):
            os.mkdir(self.cache_file_)

        self.__patition_audio = struct.pack('<h', int(0)) * 5000
        pass
    
    @classmethod
    def scanVoiceFile(self):
        wavs = os.listdir(self.voice_file)

        if 0 == len(wavs):
            return
            
        self.__voice_cache.clear()

        for wav in wavs:
            wav_file = os.path.join(self.voice_file, wav)
            read_wave = wave.open(wav_file, 'r')
            params = read_wave.getparams()
            data = read_wave.readframes(read_wave.getnframes())

            self.__params = read_wave.getparams()

            # 去掉文件后缀
            wav = wav.split('.')[0]
            self.__voice_cache[wav] = data

        
        pass

    @classmethod
    def __del__(self):
        pass
    
    @classmethod
    def reset(self):
        self.sentence_queue_.queue.clear()
        self.cache_file_num = 0
        pass

    @classmethod
    def setFile(self, cache_file, voice_file):
        self.cache_file_ = cache_file
        self.voice_file = voice_file

        self.scanVoiceFile()
        pass

    @classmethod
    def printFile(self):
        print ("cache_file: "+self.cache_file_)
        print ("voice_file: "+self.voice_file_)
        pass

    @classmethod
    def synthesis(self, content, cache_name = None):
        return self.__synthesis(content, cache_name)
        pass


    @classmethod
    def __synthesis(self, content, cache_name = None):
        file_name = ''
        if cache_name:
            file_name = self.cache_file_+'/voices'+str(cache_name)+'.wav'
        else:
            self.cache_file_num += 1
            file_name = self.cache_file_+'/voices'+str(self.cache_file_num)+'.wav'

        out_put_wave = wave.open(file_name,  'w')
        out_put_wave.setparams(self.__params)
        
        for data in content:
            if not data:
                out_put_wave.writeframes(self.__patition_audio)
            else:
                out_put_wave.writeframes(self.__voice_cache[data])
            
        out_put_wave.close()
        return True, file_name
        