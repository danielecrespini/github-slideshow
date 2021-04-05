import pyaudio
import audioop
import cv2 as cv

# a simple function to get non-negative integer values from audio input volume
def getting_rms():
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)
    print(rms)
    return rms

# here rms will process video from the webcam. The higher is RMS more blurred the video will be
# it overflows very easy.
# It works on my 2014 MacBookPro with input mic level at max value (in System Preferences Settings)
# I found that 22050 sampling rate works. At at 44100 it overflows
def image_process():
    ret, frame = cap.read()
    frame = cv.blur(frame, (getting_rms(), getting_rms()))
    window_name = 'name'
    return cv.imshow(window_name, frame)


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 22050
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
cap = cv.VideoCapture(0)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# here is where you trig the process and set "esc" button to stop the program
while cap.isOpened():
    image_process()
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()

stream.stop_stream()
stream.close()
p.terminate()
