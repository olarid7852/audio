from flask import request
from flask_restful import Resource
from ..models.audio import Audio, Participant
from ..schemas.audio import validate_audio

class AudioController(Resource):
    def get(self):
        return [a.serialize() for a in Audio.query.all()]
    
    def post(self):
        validation_result = validate_audio(request.json)
        if validation_result.get('success', False) is False:
            return {
                    "status" : "Error",
                    "errors" : validation_result.get("error")
                }, 400
        metadata = request.json.get("audioFileMetadata")
        audio = Audio(
            audio_type=request.json.get('audioFileType'),
            title=metadata.get('title'),
            duration=metadata.get('duration'),
            uploaded_time=metadata.get('uploaded_time')
        )
        audio.save()
        audio.fill_participants(metadata.get('participants'))
        return audio.serialize()

class AudioItemController(Resource):
    def get_audio(self, audio_type, id):
        return Audio.query_by_type(audio_type).filter_by(id=id).first_or_404()

    def get(self, audio_type, audio_id):
        return self.get_audio(audio_type, audio_id).serialize()

    def put(self, audio_type, audio_id):
        audio = self.get_audio(audio_type, audio_id)
        validation_result = validate_audio(request.json)
        if validation_result.get('success', False) is False:
            return {
                    "status" : "Error",
                    "errors" : validation_result.get("error")
                }, 400
        audio.update(request.json.get('audioFileType'), request.json.get("audioFileMetadata"))
        return {}

    def delete(self, audio_type, audio_id):
        audio = self.get_audio(audio_type, audio_id)
        audio.delete()
        return {'message': 'Audio deleted successfully'}, 204

class AudioTypeController(Resource):
    def get(self, audio_type):
        return [audio.serialize() for audio in Audio.query_by_type(audio_type)]