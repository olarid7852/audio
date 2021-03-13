from kanpai import Kanpai
from ..utils.validators import DateValiator, ChoiceValidator
from ..models.audio import AudioTypes


song_schema = Kanpai.Object({
    "title": Kanpai.String().required().max(100),
    "duration": Kanpai.Number().required(),
    "uploaded_time": DateValiator().required(),
})

podcast_schema = Kanpai.Object({
    "title": Kanpai.String().required().max(100),
    "duration": Kanpai.Number().required(),
    "uploaded_time": DateValiator().required(),
    "host": Kanpai.String().required().max(100),
    "participants": Kanpai.Array().of(
        Kanpai.String().required().max(100)
    ).required(),
})

audio_book_schema = Kanpai.Object({
    "title": Kanpai.String().required().max(100),
    "duration": Kanpai.Number().required(),
    "uploaded_time": DateValiator().required(),
    "narrator": Kanpai.String().required().max(100),
    "author": Kanpai.String().required().max(100),
})

def validate_audio(data):
    audio_type = data.get('audioFileType')
    metadata = song_schema
    if audio_type == AudioTypes.PODCAST:
        metadata = podcast_schema
    if audio_type == AudioTypes.AUDIO_BOOK:
        metadata = audio_book_schema
    validator = Kanpai.Object({
        "audioFileType": ChoiceValidator([AudioTypes.AUDIO_BOOK, AudioTypes.PODCAST, AudioTypes.SONG]).required(),
        "audioFileMetadata": metadata
    })
    return validator.validate(data)