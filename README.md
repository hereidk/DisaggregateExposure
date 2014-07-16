DisaggregateExposure
====================

Distribute points based on nighttime lights, corresponds to ~population density, economic activity

Locations with user-defined average value are placed based on probabilities from satellite nighttime lights data.
Data resolution is ~0.5-1km, points are randomly distributed within grid cells.

Next step: Postal code resolution?

Light data available at:
http://www.ngdc.noaa.gov/eog/dmsp/download_radcal.html

Country, state/province boundaries derived from Natural Earth:
http://www.naturalearthdata.com/downloads/

DistributeExposure.py is primary file
ClipLights.py contains classes

Download light data and point image_file (in DistributeExposure-->RunMain()) to location on disk
Unzip boundary files and point geodatafilepath (in DistributeExposure) to location on disk

Python 3.4, Anaconda
