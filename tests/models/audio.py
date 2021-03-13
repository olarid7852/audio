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

faker = Faker()

def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    print(rv)
    assert 0 == len(json.loads(rv.data))

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

def test_get_list(client):
    data_length = 10
    previous_data_length = Audio.query.count()
    [AudioFactory.create_audio() for audio in range(data_length)]
    rv = client.get('/')
    assert previous_data_length + data_length == len(json.loads(rv.data))


def test_create_audio(client):
    current_length = Audio.query.count()
    
    data = AudioFactory.build_json()
    # del(data['id'])
    rv = client.post('/', json=data)
    assert rv.status_code == 200
    assert Audio.query.count() == current_length + 1
    newly_created_audio = Audio.query.get(rv.json.get('id'))
    assert newly_created_audio
    assert newly_created_audio.audio_type == data['audioFileType']
    metadata = data['audioFileMetadata']
    assert newly_created_audio.title == metadata['title']
    assert newly_created_audio.duration == metadata['duration']
    # assert newly_created_audio.uploaded_time == audio.uploaded_time

def test_create_podcast(client):
    data = AudioFactory.build_json(audio_type=AudioTypes.PODCAST)
    rv = client.post('/', json=data)
    assert rv.status_code == 200
    newly_created_audio = Audio.query.get(rv.json.get('id'))
    assert newly_created_audio
    assert newly_created_audio.audio_type == data['audioFileType']
    metadata = data['audioFileMetadata']
    assert newly_created_audio.title == metadata['title']
    assert newly_created_audio.duration == metadata['duration']
    assert len(newly_created_audio.participants) == len(metadata['participants'])

def test_find_audio(client):
    audio = AudioFactory.create_audio()
    rv = client.get(f'/{audio.audio_type}/{audio.id}/')
    assert rv.status_code == 200

    rv = client.get(f'/10/{audio.id}/')
    assert rv.status_code == 404

def test_delete_audio(client):
    audio = AudioFactory.create_audio()
    rv = client.delete(f'/{audio.audio_type}/{audio.id}/')
    assert rv.status_code == 204
    deleted_audio = Audio.query.get(audio.id)
    assert deleted_audio == None
    rv = client.delete(f'/{audio.audio_type}/{audio.id}/')
    assert rv.status_code == 404


def test_update_audio(client):
    audio = AudioFactory.create_audio()
    update_data = AudioFactory.build_json(audio_type=audio.audio_type)
    rv = client.put(f'/{audio.audio_type}/{audio.id}/', json=update_data)
    assert rv.status_code == 200
    updated_data = Audio.query.get(audio.id)
    assert updated_data.title == update_data['audioFileMetadata']['title']
    assert updated_data.duration == update_data['audioFileMetadata']['duration']

def test_update_podcast(client):
    audio = AudioFactory.create_audio(audio_type=AudioTypes.PODCAST)
    update_data = AudioFactory.build_json(audio_type=AudioTypes.PODCAST)
    rv = client.put(f'/{audio.audio_type}/{audio.id}/', json=update_data)
    assert rv.status_code == 200
    updated_data = Audio.query.get(audio.id)
    assert updated_data.title == update_data['audioFileMetadata']['title']
    assert updated_data.host == update_data['audioFileMetadata']['host']
    assert len(updated_data.participants) == len(update_data['audioFileMetadata']['participants'])

if __name__ == '__main__':
    test_update_audio(app.test_client())

