from .controllers import audio

def routes(api):
    '''All Routes / Url
    This app uses an MVC pattern, hence all the url are routed here
    Just import your logics from the controllers package and route
    using the add_url_rule function

    :param app: Flask app instance
    :return: None
    '''

    api.add_resource(audio.AudioItemController, '/<string:audio_type>/<int:audio_id>/')
    api.add_resource(audio.AudioTypeController, '/<string:audio_type>/')
    api.add_resource(audio.AudioController, '/')
