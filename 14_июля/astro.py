from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body
from astropy import units as u
from astropy.coordinates import SkyCoord, builtin_frames

t = Time("2014-09-22 23:22")
loc = EarthLocation.of_site('greenwich')

x = solar_system_ephemeris.set('de440s')
y = get_body('jupiter', t, loc)
print(builtin_frames.GeocentricTrueEcliptic(y))
