# pylint: disable=W0223
"""VideoAlpha is ungraded Xmodule for support video content.
It's new improved video module, which support additional feature:

- Can play non-YouTube video sources via in-browser HTML5 video player.
- YouTube defaults to HTML5 mode from the start.
- Speed changes in both YouTube and non-YouTube videos happen via
in-browser HTML5 video method (when in HTML5 mode).
- Navigational subtitles can be disabled altogether via an attribute
in XML.
"""

import json
import logging

from lxml import etree
from pkg_resources import resource_string, resource_listdir

from django.http import Http404
from django.conf import settings

from xmodule.x_module import XModule
from xmodule.editing_module import MetadataOnlyEditingDescriptor
from xmodule.modulestore.mongo import MongoModuleStore
from xmodule.modulestore.django import modulestore
from xmodule.contentstore.content import StaticContent
from xblock.core import Integer, Scope, String, Boolean, Float, List

import datetime
import time

log = logging.getLogger(__name__)


class VideoAlphaFields(object):
    """Fields for `VideoAlphaModule` and `VideoAlphaDescriptor`."""
    position = Integer(help="Current position in the video", scope=Scope.user_state, default=0)
    show_captions = Boolean(help="This controls whether or not captions are shown by default.", display_name="Show Captions", scope=Scope.settings, default=True)
    youtube_id_1_0 = String(help="This is the Youtube ID reference for the normal speed video.", display_name="Default Speed", scope=Scope.settings, default="OEoXaMPEzfM")
    youtube_id_0_75 = String(help="The Youtube ID for the .75x speed video.", display_name="Speed: .75x", scope=Scope.settings, default="")
    youtube_id_1_25 = String(help="The Youtube ID for the 1.25x speed video.", display_name="Speed: 1.25x", scope=Scope.settings, default="")
    youtube_id_1_5 = String(help="The Youtube ID for the 1.5x speed video.", display_name="Speed: 1.5x", scope=Scope.settings, default="")
    start_time = Float(help="Time the video starts", display_name="Start Time", scope=Scope.settings, default=0.0)
    end_time = Float(help="Time the video ends", display_name="End Time", scope=Scope.settings, default=0.0)
    # TODO (pfogg): Write less bad documentation
    sources = List(help="A comma-separated list of filenames to be used with HTML5 video.", display_name="Video Sources", scope=Scope.settings, default=[])
    track = String(help="The external URL to download the subtitle track. This appears as a link beneath the video.", display_name="Download Track", scope=Scope.settings, default="")
    sub = String(help="The name of the subtitle track (for non-Youtube videos).", display_name="HTML5 Subtitles", scope=Scope.settings, default="")


class VideoAlphaModule(VideoAlphaFields, XModule):
    """
    XML source example:

        <videoalpha show_captions="true"
            youtube="0.75:jNCf2gIqpeE,1.0:ZwkTiUPN0mg,1.25:rsq9auxASqI,1.50:kMyNdzVHHgg"
            url_name="lecture_21_3" display_name="S19V3: Vacancies"
        >
            <source src=".../mit-3091x/M-3091X-FA12-L21-3_100.mp4"/>
            <source src=".../mit-3091x/M-3091X-FA12-L21-3_100.webm"/>
            <source src=".../mit-3091x/M-3091X-FA12-L21-3_100.ogv"/>
        </videoalpha>
    """
    video_time = 0
    icon_class = 'video'

    js = {
        'js': [
            resource_string(__name__, 'js/src/videoalpha/01_helper_utils.js'),
            resource_string(__name__, 'js/src/videoalpha/02_initialize.js'),
            resource_string(__name__, 'js/src/videoalpha/03_html5_video.js'),
            resource_string(__name__, 'js/src/videoalpha/04_video_player.js'),
            resource_string(__name__, 'js/src/videoalpha/05_video_control.js'),
            resource_string(__name__, 'js/src/videoalpha/06_video_quality_control.js'),
            resource_string(__name__, 'js/src/videoalpha/07_video_progress_slider.js'),
            resource_string(__name__, 'js/src/videoalpha/08_video_volume_control.js'),
            resource_string(__name__, 'js/src/videoalpha/09_video_speed_control.js'),
            resource_string(__name__, 'js/src/videoalpha/10_video_caption.js'),
            resource_string(__name__, 'js/src/videoalpha/11_main.js')
        ]
    }
    css = {'scss': [resource_string(__name__, 'css/videoalpha/display.scss')]}
    js_module_name = "VideoAlpha"

    def __init__(self, *args, **kwargs):
        XModule.__init__(self, *args, **kwargs)
        # xmltree = etree.fromstring(self.data)

        # # Front-end expects an empty string, or a properly formatted string with YouTube IDs.
        # self.youtube_streams = xmltree.get('youtube', '')

        # self.sub = xmltree.get('sub')

        # self.autoplay = xmltree.get('autoplay') or ''
        # if self.autoplay.lower() not in ['true', 'false']:
        #     self.autoplay = 'true'

        # self.position = 0
        # self.show_captions = xmltree.get('show_captions', 'true')
        # self.sources = {
        #     'main': self._get_source(xmltree),
        #     'mp4': self._get_source(xmltree, ['mp4']),
        #     'webm': self._get_source(xmltree, ['webm']),
        #     'ogv': self._get_source(xmltree, ['ogv']),
        # }
        # self.track = self._get_track(xmltree)
        # self.start_time, self.end_time = self.get_timeframe(xmltree)

    # def _get_source(self, xmltree, exts=None):
    #     """Find the first valid source, which ends with one of `exts`."""
    #     exts = ['mp4', 'ogv', 'avi', 'webm'] if exts is None else exts
    #     condition = lambda src: any([src.endswith(ext) for ext in exts])
    #     return self._get_first_external(xmltree, 'source', condition)

    # def _get_track(self, xmltree):
    #     """Find the first valid track."""
    #     return self._get_first_external(xmltree, 'track')

    # def _get_first_external(self, xmltree, tag, condition=bool):
    #     """Will return the first 'valid' element of the given tag.
    #     'valid' means that `condition('src' attribute) == True`
    #     """
    #     result = None

    #     for element in xmltree.findall(tag):
    #         src = element.get('src')
    #         if condition(src):
    #             result = src
    #             break
    #     return result

    # def get_timeframe(self, xmltree):
    #     """ Converts 'start_time' and 'end_time' parameters in video tag to seconds.
    #     If there are no parameters, returns empty string. """

    #     def parse_time(str_time):
    #         """Converts s in '12:34:45' format to seconds. If s is
    #         None, returns empty string"""
    #         if str_time is None:
    #             return ''
    #         else:
    #             x = time.strptime(str_time, '%H:%M:%S')
    #             return datetime.timedelta(
    #                 hours=x.tm_hour,
    #                 minutes=x.tm_min,
    #                 seconds=x.tm_sec
    #             ).total_seconds()

    #     return parse_time(xmltree.get('start_time')), parse_time(xmltree.get('end_time'))

    def handle_ajax(self, dispatch, data):
        """This is not being called right now and we raise 404 error."""
        log.debug(u"GET {0}".format(data))
        log.debug(u"DISPATCH {0}".format(dispatch))
        raise Http404()

    def get_instance_state(self):
        """Return information about state (position)."""
        return json.dumps({'position': self.position})

    def get_html(self):
        if isinstance(modulestore(), MongoModuleStore):
            caption_asset_path = StaticContent.get_base_url_path_for_course_assets(self.location) + '/subs_'
        else:
            # VS[compat]
            # cdodge: filesystem static content support.
            caption_asset_path = "/static/subs/"

        get_ext = lambda filename: filename.rpartition('.')[-1]
        sources = {get_ext(src): src for src in self.sources}

        return self.system.render_template('videoalpha.html', {
            'youtube_streams': {'youtube-id-0-75': self.youtube_id_0_75,
                                'youtube-id-1-0': self.youtube_id_1_0,
                                'youtube-id-1-25': self.youtube_id_1_25,
                                'youtube-id-1-5': self.youtube_id_1_5},
            'id': self.location.html_id(),
            'sub': self.sub,
            'sources': sources,
            'track': self.track,
            'display_name': self.display_name_with_default,
            # This won't work when we move to data that
            # isn't on the filesystem
            'data_dir': getattr(self, 'data_dir', None),
            'caption_asset_path': caption_asset_path,
            'show_captions': self.show_captions,
            'start': self.start_time,
            'end': self.end_time,
            'autoplay': settings.MITX_FEATURES.get('AUTOPLAY_VIDEOS', True)
        })


class VideoAlphaDescriptor(VideoAlphaFields, MetadataOnlyEditingDescriptor):
    """Descriptor for `VideoAlphaModule`."""
    module_class = VideoAlphaModule
    template_dir_name = "videoalpha"

    def __init__(self, *args, **kwargs):
        super(VideoAlphaDescriptor, self).__init__(*args, **kwargs)
        if self.data:
            self._parse_video_xml(self, self.data)
            del self.data

    @property
    def non_editable_metadata_fields(self):
        non_editable_fields = super(MetadataOnlyEditingDescriptor, self).non_editable_metadata_fields
        non_editable_fields.extend([VideoAlphaFields.start_time,
                                    VideoAlphaFields.end_time])
        return non_editable_fields

    @classmethod
    def from_xml(cls, xml_data, system, org=None, course=None):
        """
        Creates an instance of this descriptor from the supplied xml_data.
        This may be overridden by subclasses

        xml_data: A string of xml that will be translated into data and children for
            this module
        system: A DescriptorSystem for interacting with external resources
        org and course are optional strings that will be used in the generated modules
            url identifiers
        """
        video = cls(system, {})
        VideoAlphaDescriptor._parse_video_xml(video, xml_data)
        return video

    def export_to_xml(self, resource_fs):
        """
        Returns an xml string representing this module, and all modules
        underneath it.  May also write required resources out to resource_fs

        Assumes that modules have single parentage (that no module appears twice
        in the same course), and that it is thus safe to nest modules as xml
        children as appropriate.

        The returned XML should be able to be parsed back into an identical
        XModuleDescriptor using the from_xml method with the same system, org,
        and course
        """
        xml = etree.Element('videoalpha')
        attrs = {
            'display_name': self.display_name,
            'show_captions': json.dumps(self.show_captions),
            'youtube': self._create_youtube_string(),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'sub': self.sub
        }
        for key, value in attrs.items():
            if value:
                xml.set(key, str(value))

        for source in self.sources:
            ele = etree.Element('source')
            ele.set('src', source)
            xml.append(ele)

        if self.track:
            ele = etree.Element('track')
            ele.set('src', self.track)
            xml.append(ele)

        return etree.tostring(xml, pretty_print=True)


    def _create_youtube_string(self):
        """
        Create a string of Youtube IDs from this module's metadata
        attributes. Only writes a speed if an ID is present in the
        module.  Necessary for backwards compatibility with XML-based
        courses.
        """
        youtube_ids = [
            self.youtube_id_0_75,
            self.youtube_id_1_0,
            self.youtube_id_1_25,
            self.youtube_id_1_5
        ]
        youtube_speeds = ['0.75', '1.00', '1.25', '1.50']
        return ','.join([':'.join(pair)
                         for pair
                         in zip(youtube_speeds, youtube_ids)
                         if pair[1]])

    @staticmethod
    def _parse_youtube(data):
        """
        Parses a string of Youtube IDs such as "1.0:AXdE34_U,1.5:VO3SxfeD"
        into a dictionary. Necessary for backwards compatibility with
        XML-based courses.
        """
        ret = {'0.75': '', '1.00': '', '1.25': '', '1.50': ''}
        if data == '':
            return ret
        videos = data.split(',')
        for video in videos:
            pieces = video.split(':')
            # HACK
            # To elaborate somewhat: in many LMS tests, the keys for
            # Youtube IDs are inconsistent. Sometimes a particular
            # speed isn't present, and formatting is also inconsistent
            # ('1.0' versus '1.00'). So it's necessary to either do
            # something like this or update all the tests to work
            # properly.
            ret['%.2f' % float(pieces[0])] = pieces[1]
        return ret

    @staticmethod
    def _parse_video_xml(video, xml_data):
        """
        Parse video fields out of xml_data. The fields are set if they are
        present in the XML.
        """
        xml = etree.fromstring(xml_data)

        display_name = xml.get('display_name')
        if display_name:
            video.display_name = display_name

        youtube = xml.get('youtube')
        if youtube:
            speeds = VideoAlphaDescriptor._parse_youtube(youtube)
            if speeds['0.75']:
                video.youtube_id_0_75 = speeds['0.75']
            if speeds['1.00']:
                video.youtube_id_1_0 = speeds['1.00']
            if speeds['1.25']:
                video.youtube_id_1_25 = speeds['1.25']
            if speeds['1.50']:
                video.youtube_id_1_5 = speeds['1.50']

        show_captions = xml.get('show_captions')
        if show_captions:
            video.show_captions = json.loads(show_captions)

        sources = xml.findall('source')
        if sources:
            video.sources = [ele.get('src') for ele in sources]

        track = xml.find('track')
        if track is not None:
            video.track = track.get('src')

        start_time = VideoAlphaDescriptor._parse_time(xml.get('from'))
        if start_time:
            video.start_time = start_time

        end_time = VideoAlphaDescriptor._parse_time(xml.get('to'))
        if end_time:
            video.end_time = end_time

        sub = xml.get('sub')
        if sub:
            video.sub = sub

    @staticmethod
    def _parse_time(str_time):
        """Converts s in '12:34:45' format to seconds. If s is
        None, returns empty string"""
        if str_time is None or str_time == '':
            return ''
        else:
            obj_time = time.strptime(str_time, '%H:%M:%S')
            return datetime.timedelta(
                hours=obj_time.tm_hour,
                minutes=obj_time.tm_min,
                seconds=obj_time.tm_sec
            ).total_seconds()
