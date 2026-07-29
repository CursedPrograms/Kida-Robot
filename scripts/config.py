# GPIO Pins
LED_PINS = [17, 27, 22, 18]

# Music
MUSIC_FOLDER = "/home/kida-01/Desktop/Kida-Robot/audio/music"
SUPPORTED_FORMATS = (".mp3", ".wav", ".ogg")

# Arduino
ARDUINO_PORT = "/dev/ttyUSB0"
ARDUINO_BAUD = 9600

# Camera
IMAGE_DIR = "captures/images"
VIDEO_DIR = "captures/videos"
CAM_ROTATION = 0

# UI
SCREEN_SIZE = (1000, 500)
IMAGE_SIZE = (300, 300)
CHARACTER_FOLDER = "/home/kida-01/Desktop/Kida-Robot/images/characters"
BACKGROUND_IMAGE = "/home/kida-01/Desktop/Kida-Robot/images/background.jpeg"

# Motor
MAX_SPEED = 255
DEFAULT_SPEED = MAX_SPEED   # always start at full speed
SPEED_STEP = 50
MIN_SPEED = 100

# Motor lock — password required to unlock (see motor_lock.py)
MOTOR_LOCK_PASSWORD = "1234"

# Bluetooth
BLUETOOTH_NAME = "KIDA01"
