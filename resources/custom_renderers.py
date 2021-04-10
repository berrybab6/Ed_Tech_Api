from rest_framework import renderers
class VideoRenderer(renderers.BaseRenderer):
    media_type = 'video/mp4'
    format = 'mp4'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

