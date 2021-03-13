from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import request, jsonify
import enum
import json
from flask_expects_json import validate, ValidationError

from ..db.db import db


class AudioTypes:
    SONG = 'song'
    PODCAST = 'podcast'
    AUDIO_BOOK = 'audiobook'

AUDIO_TYPES_NAMES = {
    AudioTypes.SONG: 'SONG',
    AudioTypes.PODCAST: 'PODCAST',
    AudioTypes.AUDIO_BOOK: 'AUDIO BOOK'
}

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    audio_id = db.Column(db.Integer, db.ForeignKey('audio.id'))

    @staticmethod
    def get_perticipants(id):
        return [participant.name for participant in Participant.query.filter_by(audio_id=id).all()]

    @staticmethod
    def fill_participants(audio_id, participants):
        if not participants:
            return False
        saved_participants = Participant.query.filter(Participant.name.in_(participants)).order_by(Participant.name)
        deleted_participants = Participant.query.filter(~Participant.name.in_(participants))
        deleted_participants.delete(synchronize_session=False)
        db.session.commit()
        new_participants = set(participants) - set(saved_participants)
        db.session.bulk_insert_mappings(Participant, [{'name': participant, 'audio_id': audio_id} for participant in new_participants])
        db.session.commit()
        return True

class Audio(db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.Integer, primary_key=True)
    audio_type = db.Column(db.String(10))
    title = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    uploaded_time = db.Column(db.DateTime)
    host = db.Column(db.String(100))
    author = db.Column(db.String(100))
    narrator = db.Column(db.String(100))

    # def __init__(self, *args, **kwargs):
    #     super(db.Model, self).__init__()
    #     self.updated_participants = kwargs.get('participants')

    @staticmethod
    def query_by_type(audio_type):
        return Audio.query.filter_by(audio_type=audio_type)

    @property
    def updated_participants(self):
        if self.__dict__.get('updated_participants'):
            return self.__dict__.get('updated_participants')
        return None

    @updated_participants.setter
    def updated_participants(self, value):
        self.__dict__['updated_participants'] = value

    @property
    def participants(self):
        return Participant.get_perticipants(self.id)



    def fill_participants(self, participants):
        Participant.fill_participants(self.id, participants)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, audio_type, data):
        self.audio_type = audio_type
        updated_participants = None
        if data.get('participants'):
            updated_participants = data.pop('participants')
        for key in data.keys():
            self.__dict__[key] = data[key]
        Audio.query.filter_by(id=self.id).update(data)
        if updated_participants:
            self.fill_participants(updated_participants)
        db.session.commit()
        return self
    
    def serialize(self):
        metadata = {
            'title': self.title,
            'duration': self.duration,
            'uploaded_time': self.uploaded_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
        }
        if self.audio_type == AudioTypes.AUDIO_BOOK:
            metadata['author'] = self.author
            metadata['narrator'] = self.narrator
        if self.audio_type == AudioTypes.PODCAST:
            metadata['participants'] = self.participants
            metadata['host'] = self.host

        return {
            'id': self.id,
            'audioFileType': self.audio_type,
            'audioFileMetadata': metadata
        }

