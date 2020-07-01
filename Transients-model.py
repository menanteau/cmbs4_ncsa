#!/usr/bin/env python

import pandas as pd


def add(df, row):
    '''return new data frame with row attached.'''
    return df.append(pd.Series(row, index=df.columns, name=df.shape[0]))


# Make infarstructure to record all the numbers in a pandas data frams
df = pd.DataFrame(columns=["Element", 'Owner', 'Governing', 'Name', 'Value', 'Units'])

"""
HIGH LEVEL MEASUREMENT SPECIFI

Here we quote the measurment properties for the data the is the fundamental
input to the transients.

* These are defined in a High level Requirements spreadsheet *

Measurement Requirement: Measure I, Q, and U at 95 and 150 GHz at 1.4'
resolution over 1000s of square degrees on a daily cadence.
The survey shall reach noise levels below 10 mJy in less than 1 week of
observing.

The code block below records them an adds a few convieniece variables.
"""

SP_AVG_SQ_DEG_PER_DAY = 200
CHILEAN_AVG_SQ_DEG_PER_DAY = 1000

# science measurement requirements
owner = 'TBD Upstream Operations'
governing = 'Transients'
element = "OPS Spec"
df = add(df, [element, owner, governing, 'Average usable SP area per day',
         SP_AVG_SQ_DEG_PER_DAY, 'sq degree'])
df = add(df, [element, owner, governing, 'Average usabel Chilean area per Day',
         CHILEAN_AVG_SQ_DEG_PER_DAY, 'sq degree'])

"""
OBSERVATION ASSUMPTIONS

What we want is to work towards the averges "good area" we wil process
in a night.
For the level of baseline we have we need two quantities, one for the SP and
one for two Chilean LATS combined.

Ideally these come to us from a detailed systems engineering analysis, but  for
now we have to SWAG. Considerations for the SWAG are:

* Downtime of system
* Removal of area where the signal is not appropriate
* Conditions precluding observingwere, etc
"""

GHZ_BANDS = [95, 150, 220]
NBANDS = len(GHZ_BANDS)
RESOLUTION_ARC_MIN = 0.5
PIX_PER_SQ_DEGREE = 3600/(RESOLUTION_ARC_MIN)**2

# science measurement requirements
owner = 'Measurements'
governing = 'Transients'
element = "OBS Spec"
df = add(df, [element, owner, governing, 'Bands', GHZ_BANDS, 'GHz'])
df = add(df, [element, owner, governing, 'Resolution', RESOLUTION_ARC_MIN, 'arcmin'])
df = add(df, [element, owner, governing, 'Measurement', GHZ_BANDS, ''])

# Straightforwardly derive a few useful quantities
df = add(df, [element, owner, governing, 'NBANDS', NBANDS, ''])
df = add(df, [element, owner, governing, 'PIX_PER_SQ_DEGREE', PIX_PER_SQ_DEGREE, 'Pixels'])

"""
CHARACTERISTSICS OF THE DAILY QA (DQA) MAPS THAT ARE OUR INPUT

Here we make assumptions about the characteristics of the Daily QA Maps.
We will ge from THE DATA PROCUCTION WBS.

* SHOWS AN UNDERSTANDING OF THE PRIMARY DATA INTERFACE.
* PART OF THE RECORD WE'D RECOMEND TO BE RETAINED FOR REPRODUCEABLITY.
"""

# science measurement requirements
owner = 'Transients'
governing = 'Data Production', 'Data Service'

#
# Transient require these inputs
# Assume all data is pixels -- these are our inputs we expect from the
# daily QA Mao
DQA_BANDS = GHZ_BANDS
NUMBER_DQA_BANDS = len(DQA_BANDS)
DQA_MEASUREMENT_PLANES = ['I', 'Q', 'U', "variance", "bitmask"]
NUMBER_DQA_PLANES = len(DQA_MEASUREMENT_PLANES)

# assume 4 bytes (e.g 32 numbers)  BYTES_PER_PLANE is an uncompressed number.
# 4 bytes = foat32 (in Python)
DQA_BYTES_PER_PIXEL = 4 * (NUMBER_DQA_PLANES * NUMBER_DQA_BANDS)
DQA_BYTES_PER_SQ_DEGREE = DQA_BYTES_PER_PIXEL * PIX_PER_SQ_DEGREE

# volume given observing assumptions
SP_DQA_BYTES_PER_YEAR = DQA_BYTES_PER_SQ_DEGREE*SP_AVG_SQ_DEG_PER_DAY*365
CHILEAN_DQA_BYTES_YEAR = DQA_BYTES_PER_SQ_DEGREE*CHILEAN_AVG_SQ_DEG_PER_DAY*365

# Record for grand table at the end
# science measurement requirements
owner = 'Transients'
governing = 'Data Production', 'Data Service'
element = 'DQA Data'
df = add(df, [element, owner, governing, 'DQA Bands', DQA_BANDS, 'GHz'])
df = add(df, [element, owner, governing, 'DQA Planes', DQA_MEASUREMENT_PLANES, ''])
df = add(df, [element, owner, governing, 'DQA Bytes per Sq. Degree', DQA_BYTES_PER_SQ_DEGREE, 'Bytes'])
df = add(df, [element, owner, governing, 'DQA Bytes per Pixel', DQA_BYTES_PER_PIXEL, 'Bytes'])
df = add(df, [element, owner, governing, 'DQA SP Bytes per Year', SP_DQA_BYTES_PER_YEAR, 'Bytes'])
df = add(df, [element, owner, governing, 'DQA Chilean Bytes per Year', CHILEAN_DQA_BYTES_YEAR, 'Bytes'])

"""
CHARACTERISTICS OF THE DATASET (TDET) WE WILL USE FOR DETECTION
Transients will highpass filter the data prior to detection.
DLP does not know what procesing would apply to Q and U. (Pashe information).
For the moment, assume it is processed in some way.  Ditto Book Keeping.
"""

# Products needed for detection --
# these would be high-passed filtered analog of inputs

TDET_BANDS = DQA_BANDS
NUMBER_TDET_BANDS = len(TDET_BANDS)
TDET_MEASUREMENT_PLANES = ['I', 'Q', 'U', "variance", "bitmask"]
NUMBER_TDET_PLANES = len(TDET_MEASUREMENT_PLANES)

# assume 4 bytes (e.g 32 numbers)  BYTES_PER_PLANE is an uncompressed number.
TDET_BYTES_PER_PIXEL = 4 * (NUMBER_TDET_PLANES * NUMBER_TDET_BANDS)
TDET_BYTES_PER_SQ_DEGREE = TDET_BYTES_PER_PIXEL*PIX_PER_SQ_DEGREE

# Volume given observing assumptions
SP_TDET_BYTES_PER_YEAR = TDET_BYTES_PER_SQ_DEGREE * SP_AVG_SQ_DEG_PER_DAY*365
CHILEAN_TDET_BYTES_PER_YEAR = TDET_BYTES_PER_SQ_DEGREE * CHILEAN_AVG_SQ_DEG_PER_DAY*365

# Record for grand table at the end
owner = 'Transients'  # science measurement requirements
governing = 'Data Service'  # keep out internal
element = 'TDET Data'
df = add(df, [element, owner, governing, 'TDET Bands', TDET_BANDS, 'GHz'])
df = add(df, [element, owner, governing, 'TDET Planes', TDET_MEASUREMENT_PLANES, ''])
df = add(df, [element, owner, governing, 'TDET Bytes per Sq. Degree', TDET_BYTES_PER_SQ_DEGREE, 'Bytes'])
df = add(df, [element, owner, governing, 'TDET Bytes per Pixel', TDET_BYTES_PER_PIXEL, 'Bytes'])
df = add(df, [element, owner, governing, 'TDET SP Bytes per Year', SP_TDET_BYTES_PER_YEAR, 'Bytes'])
df = add(df, [element, owner, governing, 'TDET Chilean Bytes per Year', CHILEAN_TDET_BYTES_PER_YEAR, 'Bytes'])

"""
CHARACTERISTIC OF TRANISENT DETECTION PERFORMANCE

Total SWAG here all source Detections that we'd recore as a function of area.
The assumptions are SP is deeper.
"""

SP_TDET_DETECTIONS_PER_SQ_DEGREE = 50/1000
SP_TDET_DETECTIONS_PER_DAY = SP_TDET_DETECTIONS_PER_SQ_DEGREE * SP_AVG_SQ_DEG_PER_DAY

CHILEAN_TDET_DETECTIONS_PER_SQ_DEGREE = 20/1000
CHILEAN_TDET_DETECTIONS_PER_DAY = CHILEAN_TDET_DETECTIONS_PER_SQ_DEGREE * CHILEAN_AVG_SQ_DEG_PER_DAY

owner = 'Transients'  # science measurement requirements
governing = 'Alerts, SP Network, Data Service'
element = 'TDET Opspec'
df = add(df, [element, owner, governing, 'Average Number SP Transient detections/day',
         SP_TDET_DETECTIONS_PER_DAY, 'per day'])
governing = 'Alerts, Data Service'
df = add(df, [element, owner, governing, 'Average Number Chilean Transient detections/day',
         CHILEAN_TDET_DETECTIONS_PER_DAY, 'per day'])

"""
CHARACTERISTICS OF THE CUTOUTS  (TCUT) DATA

* This is the data that we package to descibe teh detection we made.
* This "nominal" data unclear is nominal is a sixe that fits all
* These would be in a 9maybe concpetutal) alert packet
"""

TCUT_SIZE_ARCMIN = 10
TCUT_AREA_SQDEG = TCUT_SIZE_ARCMIN**2/3600.
TCUT_AREA_PIX = PIX_PER_SQ_DEGREE*TCUT_AREA_SQDEG
# TCUT_AREA_PIX = 81
TCUT_PIXEL_BYTES = TDET_BYTES_PER_PIXEL * (TCUT_AREA_PIX) * NUMBER_TDET_BANDS
TCUT_METADATA_BYTES = 400   # A Swag
BYTES_PER_TCUT = TCUT_PIXEL_BYTES + TCUT_METADATA_BYTES

print(f"TCUT_AREA_PIX:{TCUT_AREA_PIX} [PIX]")
print(f"TCUT_AREA_SQDEG:{TCUT_AREA_SQDEG} [PIX]")
print(f"PIX_PER_SQ_DEGREE:{PIX_PER_SQ_DEGREE} [PIX/SQDEG]")

owner = 'Transients'  # science measurement requirements
governing = 'Alerts', 'Data Service'  # keep out internal
element = 'TCUT Dset'
df = add(df, [element, owner, governing, 'Cutout Bands', TDET_BANDS, 'GHz'])
df = add(df, [element, owner, governing, 'Coutout Resolution', RESOLUTION_ARC_MIN, 'arcsec'])
df = add(df, [element, owner, governing, 'Cutout Measurement', TDET_MEASUREMENT_PLANES, ''])
df = add(df, [element, owner, governing, 'Cutout Pixels Per Plane', TCUT_AREA_PIX, ''])
df = add(df, [element, owner, governing, 'Cutout Data Volume', BYTES_PER_TCUT, 'Bytes'])

# Data volume related numbers fof Cutouts from the SP
SP_TCUT_DATA_VOLUME_PER_DAY = SP_TDET_DETECTIONS_PER_DAY*BYTES_PER_TCUT
SP_TCUT_DATA_VOLUME_PER_YEAR = SP_TCUT_DATA_VOLUME_PER_DAY*365
governing = 'Alerts, "SP Network", Data Service'
df = add(df, [element, owner, governing, 'daily avg SP Cutout Data volume',
         SP_TCUT_DATA_VOLUME_PER_DAY, 'Bytes/day'])
df = add(df, [element, owner, governing, 'Yearly SP Cutout data volume',
         SP_TCUT_DATA_VOLUME_PER_YEAR, 'per year'])

# Cutouts from Chile
governing = 'Alerts, Data Service'
CHILEAN_TCUT_DATA_VOLUME_PER_DAY = CHILEAN_TDET_DETECTIONS_PER_DAY*BYTES_PER_TCUT
CHILEAN_TCUT_DATA_VOLUME_PER_YEAR = CHILEAN_TCUT_DATA_VOLUME_PER_DAY*365
df = add(df, [element, owner, governing, 'daily avg Chilean Cutout Data volume',
         CHILEAN_TCUT_DATA_VOLUME_PER_DAY, 'Bytes/day'])
df = add(df, [element, owner, governing, 'Yearly Chilean Cutout data volume',
         CHILEAN_TCUT_DATA_VOLUME_PER_DAY*365, 'per year'])


"""
Annual Data Volumes
"""
# And a grand totals for fun
ANNUAL_TRANSIENT_RECORD_DATA_VOLUME_PER_YEAR = \
    SP_TDET_BYTES_PER_YEAR + \
    CHILEAN_TDET_BYTES_PER_YEAR + \
    SP_TCUT_DATA_VOLUME_PER_YEAR + \
    CHILEAN_TCUT_DATA_VOLUME_PER_YEAR


owner = "Transients"
governing = 'Data Service'
element = 'T Data Total'
# our data record
# THE SUM OF TRANSIENT-GENEARTED DATA VOlUME PER
df = add(df, [element, owner, governing, 'Yearly Volume for planned data volume',
         ANNUAL_TRANSIENT_RECORD_DATA_VOLUME_PER_YEAR, 'Bytes'])

print(df)
