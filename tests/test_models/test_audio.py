import os
import tempfile
import json
import pytest
from faker import Faker
import random
from datetime import datetime
from app.models.audio import Audio, AudioTypes
from ..factories.audio import AudioFactory
from app.schemas.audio import validate_audio
from tests.client import client

faker = Faker()

# def test_empty_db(client):
#     """Start with a blank database."""
#     rv = client.get('/')
#     print(rv)
#     assert 0 == len(json.loads(rv.data))

def test_audio_book_validation(client):
    audio = AudioFactory.build_json(audio_type=AudioTypes.AUDIO_BOOK)
    result = validate_audio(audio)
    assert result.get('success') == True

def test_podcast_validation(client):
    audio = AudioFactory.build_json(audio_type=AudioTypes.PODCAST)
    result = validate_audio(audio)
    assert result.get('success') == True

def test_song_validation(client):
    audio = AudioFactory.build_json(audio_type=AudioTypes.SONG)
    result = validate_audio(audio)
    assert result.get('success') == True
