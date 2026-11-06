from pydantic import BaseModel
from datetime import datetime

class StreamTags(BaseModel):
    encoder: str | None = None

class Disposition(BaseModel):
    default:            int | str | None = None
    dub:                int | str | None = None
    original:           int | str | None = None
    comment:            int | str | None = None
    lyrics:             int | str | None = None
    karaoke:            int | str | None = None
    forced:             int | str | None = None
    hearing_impaired:   int | str | None = None
    visual_impaired:    int | str | None = None
    clean_effects:      int | str | None = None
    attachment_pic:     int | str | None = None
    timed_thumbnails:   int | str | None = None
    non_diegetic:       int | str | None = None
    captions:           int | str | None = None
    descriptions:       int | str | None = None
    metadata:           int | str | None = None
    dependent:          int | str | None = None
    still_image:        int | str | None = None
    multilayer:         int | str | None = None

class Stream(BaseModel):
    index:              int
    codec_name:         str
    codec_type:         str
    codec_long_name:    str         | None = None
    codec_tag_string:   str         | None = None
    codec_tag:          str         | None = None
    mime_codec_string:  str         | None = None
    sample_fmt:         str         | None = None
    sample_rate:        int         | None = None
    channels:           int         | None = None
    channel_layout:     str         | None = None
    bit_per_sample:     int         | None = None
    initial_padding:    int         | None = None
    r_frame_rate:       str         | None = None
    avg_frame_rate:     str         | None = None
    time_base:          str         | None = None
    start_pts:          int         | None = None
    start_time:         float       | None = None
    duration_ts:        int         | None = None
    duration:           float       | None = None
    bit_rate:           int         | None = None
    disposition:        Disposition | None = None
    tags:               StreamTags  | None = None

    # TODO: tem streams de video q n estou tratando aq

class FormatTags(BaseModel):
    title:             str      | None = None 
    artist:            str      | None = None
    album:             str      | None = None
    composer:          str      | None = None
    creation_time:     datetime | None = None
    encoder:           str      | None = None
    major_brand:       str      | None = None
    minor_version:     int      | None = None
    compatible_brands: str      | None = None

class Format(BaseModel):
    filename:           str
    nb_streams:         int
    format_name:        str
    nb_programs:        int        | None = None
    nb_streams_groups:  int        | None = None
    format_long_name:   str        | None = None
    start_time:         float      | None = None
    bit_time:           int        | None = None
    probe_score:        int        | None = None
    tags:               FormatTags | None = None
    nb_stream_groups:   int        | None = None
    duration:           float      | None = None
    size:               int        | None = None
    bit_rate:           int        | None = None

class FFProbeResponse(BaseModel):
    streams: list[Stream]
    format: Format
