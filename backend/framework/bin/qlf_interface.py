from util import (
    format_night,
    extract_exposure_data,
    extract_fibermap_data
)
import os
import datetime
import re
from log import get_logger

qlf_root = os.environ.get('QLF_ROOT')

log = get_logger(
    "qlf.interface",
    os.path.join(qlf_root, "logs", "qlf_interface.log")
)


class QLFInterface(object):

    def last_exposure(self):

        spectro_data = os.environ.get('DESI_SPECTRO_DATA')

        night = re.findall(
            r"(\d{8})",
            ''.join(sorted(os.listdir(spectro_data), reverse=True)))[:1]
        night = ''.join(night)

        if not night:
            log.error("Empty nights directory: {}".format(spectro_data))
            return dict()
        
        night_path = os.path.join(spectro_data, night)

        exposure = re.findall(
            r"(\d{8})",
            ''.join(sorted(os.listdir(night_path), reverse=True)))[:1]
        exposure = ''.join(exposure)

        if not exposure:
            log.error("Empty exposures directory: {}".format(night_path))
            return dict()

        exposure_path = os.path.join(night_path, exposure)

        try:
            file_list = ''.join(sorted(os.listdir(exposure_path), reverse=True))
        except:
            log.error("File not found {}".format(exposure_path))
            return None

        exp_dir = re.findall(
            r"desi-(\d+).fits.fz",
            file_list
        )[:1]
        exp_dir = ''.join(exp_dir)

        if not exp_dir:
            log.error("Not found exposures: {}".format(exposure_path))
            return dict()

        return dict(exposure=extract_exposure_data(int(exp_dir), night),
                    fibermap=extract_fibermap_data(int(exp_dir), night))
