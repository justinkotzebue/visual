import numpy as np
import cv2
import sounddevice as sd
import random
import math
import numpy
import pyaudio


def sine(frequency, seconds, sampling_rate):
    """factor = cycles/sec / bits/sec
    Args:
        frequency: the frequency of the wave.
        seconds: the length of the wave in seconds.
        sampling_rate: the sampling rate of audio I/O. Defaults to
            44.1 kHz.
    """
    # The length of the array to generate.
    length = int(seconds * sampling_rate)

    # Angular frequency of a wave.
    angular_freq = float(frequency) * (math.pi * 2)

    # Normalized frequency, or the frequency in radians divided by sampling
    # rate.
    cycles_per_sample = angular_freq / sampling_rate

    # The sampling period, expressed as a discrete interval of time
    # [0, seconds).
    values = numpy.arange(length)
    return numpy.sin(cycles_per_sample * values)

def triangle(frequency, seconds, sampling_rate):
    """A triangle wave.
    Args:
        frequency: the frequency of the wave.
        seconds: the length of the wave in seconds.
        sampling_rate: the sampling rate of audio I/O. Defaults to
            44.1 kHz.
    """
    # The length of the array to generate.
    length = int(seconds * sampling_rate)

    # Angular frequency of a wave.
    angular_freq = float(frequency) * (math.pi * 2)

    # Normalized frequency, or the frequency in radians divided by sampling
    # rate.
    cycles_per_sample = angular_freq / sampling_rate

    # The sampling period, expressed as a discrete interval of time
    # [0, seconds).
    values = numpy.arange(length)
    # from wolframalpha: http://mathworld.wolfram.com/TriangleWave.html
    return 2 * numpy.arcsin(numpy.sin(values * cycles_per_sample))


def square(frequency, seconds, sampling_rate):
    """A square wave.
    Args:
        frequency: the frequency of the wave.
        seconds: the length of the wave in seconds.
        sampling_rate: the sampling rate of audio I/O. Defaults to
            44.1 kHz.
    """
    # The length of the array to generate.
    length = int(seconds * sampling_rate)

    # The period of the square wave.
    period = sampling_rate / float(frequency)
    values = numpy.arange(length)
    def squaregen(period, length, amplitude):
        x = 0
        y = -amplitude
        half_period = round(float(period) / 2)
        while x < length:
            # An acceptable epsilon value. Flip signs every half period.
            if x % half_period <= 0.5:
                y *= -1
            yield y
            x += 1
    values = numpy.fromiter(squaregen(period, length, 0.5), "d")
    return values

def play_tone(stream, frequency=440, seconds=1, rate=44100):
    """Play a tone, as expressed by a waveform.
    Args:
        stream: the audio stream to write to.
        frequency: the frequency of the tone, in Hz.
        seconds: the length of the tone in seconds.
        rate: the sampling rate of the audio stream.
    """
    chunks = []
    sine_tone = sine(frequency, seconds, rate)
    sine_tone.shape
    triangle_tone = triangle(frequency, seconds, rate)
    square_tone = square(frequency, seconds, rate)
    chunks.append(sine_tone)
    chunks.append(triangle_tone)
    chunks.append(square_tone)

    chunk = numpy.concatenate(chunks)

    stream.write(chunk.astype(numpy.float32).tostring())


def make_array_to_sound(array, band=0, play=False, ret=True):
    try:
        if array.shape[2] == 3:
            sound = array[:, :, band]
    except:
        sound = array
    s = sound.reshape(sound.shape[0] * sound.shape[1])
    print(s)
    if play:
        sd.play(s, blocking=True)
    if ret:
        return s


    # p = pyaudio.PyAudio()
    # stream = p.open(format=pyaudio.paInt16,
    #                 channels=1, rate=44100, output=1)
    # stream_2 = stream.write(s)
    #
    # play_tone(s)

cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    frequency = np.arange(1,9999,1)
    for i in frequency:
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #make_array_to_sound(gray, band=1)
        gray_array = gray.reshape(gray.shape[0] * gray.shape[1])
        l,b = gray.shape

        # Sinus
        frequency = random.randint(1,99999)
        seconds = random.randint(1,6)
        sine_tone = sine(frequency=frequency, seconds=seconds, sampling_rate=len(gray_array)/seconds)
        sinte_int = np.rint(sine_tone) * 1000
        gray_sine = gray_array + sinte_int.astype(np.uint8)
        gray_s = gray_sine.reshape(l,b)

        # sqare


        sqare = square(frequency=i, seconds=1, sampling_rate=len(gray_array))
        sq = sqare.astype(np.float)*150
        sqare_int = np.rint(sq)
        sqare_i = sqare_int.reshape(l,b)
        gray_sq = sqare_i + gray_s
        # Display the resulting frame
        cv2.imshow("frame-by-frame", gray_sq)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
