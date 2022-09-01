import torch
import pyaudio
import nltk
nltk.download('punkt')

print(torch.cuda.is_available())
print(torch.cuda.get_arch_list())

# pyaudio class instance
po = pyaudio.PyAudio()
