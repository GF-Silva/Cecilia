from . import FFProbeAdapter
from fastapi import Depends
from typing import Annotated

def get_ffprobe_adater():
    return FFProbeAdapter()

FFProbeAdapterDep = Annotated[FFProbeAdapter, Depends(get_ffprobe_adater)]