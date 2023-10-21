from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii
import os.path
import os
import subprocess
import moviepy.editor as moviepy
import glob
import wave



def extractAudio(url,OutFileName = 'out_audio'):
    subprocess.run(['yt-dlp', '-f', 'bestaudio',  '-P','/', url], check=True)
    clip = moviepy.AudioFileClip(''.join(glob.glob('*.webm')))
    clip.write_audiofile(f"{OutFileName}.wav")
    os.remove(''.join(glob.glob('*.webm')))
    
  

##Encrypting program

def Create_Keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.public_key().export_key()
    #Write Files
    with open('private_key.pem','wb') as pr:
        pr.write(private_key)
    with open('public_key.pem','wb') as pu:
        pu.write(public_key)


def import_privateK(FileName):
    pr_key = RSA.import_key(open(f'{FileName}','r').read())
    return pr_key

def import_publicK(FileName):
    pu_key = RSA.import_key(open(f'{FileName}','r').read())
    return pu_key



#Encode
def encode(pathToAudioFile, string, pu_key, outputFile):
    waveaudio = wave.open(pathToAudioFile, mode='rb')
    key = import_publicK(pu_key)
    #Additional PKCS1 encoding with secret key
    cipher = PKCS1_OAEP.new(key = key)
    res = bytes(string,'utf-8')
    cipher_text = cipher.encrypt(res)
    hexa_text = binascii.hexlify(cipher_text)
    message = hexa_text.decode("utf-8")
    #Audio encoding
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    with wave.open(f"{outputFile}.wav", 'wb') as fd:
        fd.setparams(waveaudio.getparams())
        fd.writeframes(frame_modified)
    waveaudio.close()


#Decode

def decode(pathToAudioFile,pr_key):
    waveaudio = wave.open(pathToAudioFile, mode='rb')
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    msg = string.split("###")[0]
    #2nd Layer PKCS1 encryption with secret key
    key = import_privateK(pr_key)
    decrypt = PKCS1_OAEP.new(key = key)
    hexa_text = msg.encode("utf-8")
    cipher_text = binascii.unhexlify(hexa_text)
    decrypted_message = decrypt.decrypt(cipher_text).decode('utf-8')
    waveaudio.close()
    return decrypted_message







########################################################################################





