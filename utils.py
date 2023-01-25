import face_recognition
from pydub import AudioSegment


def convert_mp3_to_wav(file_path):
    file = AudioSegment.from_file(file_path)
    file.set_frame_rate(16000)

    file.export(file_path, format="wav")


def search_face(file_path):
    file = face_recognition.load_image_file(file_path)
    result_face = face_recognition.face_locations(file)

    return True if result_face else False
