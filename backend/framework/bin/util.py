import logging
import os
import astropy.io.fits
import datetime
import yaml

logger = logging.getLogger()

qlf_root = os.getenv('QLF_ROOT')

if not qlf_root:
    raise ValueError('QLF_ROOT not define.')

# TODO: flat program can also use flat_preproc.
program_mapping = {
    'flat': 'flat',  # flat_preproc
    'arc': 'arc',
    'dark': 'science',
    'gray': 'science',
    'bright': 'science'
}


def get_ql_config_file(program):
    """ Gets configuration file from directory defined in env QL_CONFIG_DIR

    Arguments:
        program {str} -- program

    Returns:
        str -- config file path that will be used
    """

    program_file = program_mapping.get(program, 'science')

    return '{}/qlconfig_{}.yaml'.format(os.environ.get('QL_CONFIG_DIR'), program_file)


def extract_exposure_data(exposure_id, night):
    """ Extracts exposure data from fits file.

    Arguments:
        exposure_id {int} -- exposure ID
        night {str} -- night (format: YYYYMMDD)

    Returns:
        dict -- exposure data from fits file.
    """

    desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')
    desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')

    exposure_zfill = str(exposure_id).zfill(8)
    expo_name = "desi-{}.fits.fz".format(exposure_zfill)

    file_path = os.path.join(desi_spectro_data, night, exposure_zfill, expo_name)

    try:
        hdr = astropy.io.fits.getheader(file_path)
    except Exception as err:
        logger.error("Error to load fits file: %s" % err)
        return {}

    # TODO: improve after understanding the QL pipeline cycle.
    program = hdr.get('program')
    current_config = get_ql_config_file(program)

    return {
        "exposure_id": exposure_id,
        "dateobs": hdr.get('date-obs'),
        "night": night,
        "zfill": exposure_zfill,
        "desi_spectro_data": desi_spectro_data,
        "desi_spectro_redux": desi_spectro_redux,
        'telra': hdr.get('telra', None),
        'teldec': hdr.get('teldec', None),
        'tile': hdr.get('tileid', None),
        'flavor': hdr.get('flavor', None),
        'program': hdr.get('program', None),
        'airmass': hdr.get('airmass', None),
        'exptime': hdr.get('exptime', None),
        'qlconfig': current_config,
        'time': datetime.datetime.utcnow()
    }

def extract_fibermap_data(exposure_id, night):
    """ Extracts fibermap data from fits file.

    Arguments:
        exposure_id {int} -- exposure ID
        night {str} -- night (format: YYYYMMDD)

    Returns:
        dict -- fibermap data from fits file.
    """

    desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')

    exposure_zfill = str(exposure_id).zfill(8)
    fiber_name = "fibermap-{}.fits".format(exposure_zfill)

    file_path = os.path.join(desi_spectro_data, night,
                             exposure_zfill, fiber_name)

    try:
        fmap = astropy.io.fits.open(file_path)
    except Exception as err:
        logger.error("Error to load fits file: %s" % err)
        return {}

    fiber_ra = fmap['FIBERMAP'].data['FIBER_RA']
    fiber_dec = fmap['FIBERMAP'].data['FIBER_DEC']
    fiber = fmap['FIBERMAP'].data['FIBER']
    objtype = fmap['FIBERMAP'].data['OBJTYPE']

    return {
        "fiber_ra": fiber_ra.tolist(),
        "fiber_dec": fiber_dec.tolist(),
        "fiber": fiber.tolist(),
        "objtype": objtype.tolist()
    }


def check_hdu(exposure_id, night):
    """ Checks camera and EXPID data from fits file header.

    Arguments:
        exposure_id {int} -- exposure ID
        night {str} -- night (format: YYYYMMDD)

    Returns:
        array -- avaiable camera list.
    """

    desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')

    exposure_zfill = str(exposure_id).zfill(8)
    expo_name = "desi-{}.fits.fz".format(exposure_zfill)

    file_path = os.path.join(desi_spectro_data, night,
                             exposure_zfill, expo_name)

    try:
        hdr = astropy.io.fits.open(file_path)
        cameras = []
        for camera in hdr:
            try:
                if camera.header['EXPID'] == exposure_id and \
                  camera.header['CAMERA']:
                    cameras.append(camera.header['CAMERA'])
            except:
                None
        return cameras
    except Exception as err:
        logger.error("Error to load fits file: %s" % err)
        return []


def ensure_dir(path):
    """ Ensures that the directory exists.

    Arguments:
        path {str} -- directory path
    """

    os.makedirs(path, exist_ok=True)


def format_night(new_date):
    """ Gets date formated
    
    Arguments:
        new_date {object} -- datetime object 
    
    Returns:
        str -- date formated
    """

    return new_date.strftime("%Y%m%d")


if __name__ == "__main__":
    check_hdu(3578, '20191001')
