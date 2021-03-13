from faker import Faker
import random
from app.models.audio import AudioTypes, Audio

faker = Faker()

class AudioFactory(object):

    @staticmethod
    def build_audio(
        audio_type=random.choice([AudioTypes.AUDIO_BOOK, AudioTypes.PODCAST, AudioTypes.SONG]),
        title = faker.text()[:100],
        duration = random.randint(100, 30000),
        uploaded_time = faker.date_time(),
        host = faker.text()[:100],
        author = faker.text()[:100],
        narrator = faker.text()[:100],
    ):
        audio = Audio(
            audio_type = audio_type,
            title = title,
            duration = duration,
            uploaded_time = uploaded_time,
        )
        if audio_type == AudioTypes.PODCAST:
            audio.host = host
        if audio_type == AudioTypes.AUDIO_BOOK:
            audio.author = author
            audio.narrator = narrator
        return audio

    @staticmethod
    def build_json(*args, **kwargs):
        audio = AudioFactory.build_audio(*args, **kwargs)
        data = audio.serialize()
        if audio.audio_type == AudioTypes.PODCAST:
            data['audioFileMetadata']['participants'] = [faker.text()[:100] for participants in range(random.randint(1, 100))]
        if data.__contains__('id'):
            data.__delitem__('id')
        return data

    @staticmethod
    def create_audio(*args, **kwargs):
        audio = AudioFactory.build_audio()
        audio.save()
        audio.fill_participants([faker.text()[:100] for participants in range(random.randint(1, 100))])
        return audio
