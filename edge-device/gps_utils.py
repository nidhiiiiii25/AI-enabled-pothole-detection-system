# ~/pothole_system/gps_utils.py
import re

def nmea_to_decimal(deg_min, hemi):
    """
    Convert NMEA ddmm.mmmm (or dddmm.mmmm) format to decimal degrees.
    """
    if not deg_min:
        return None
    m = re.match(r"^(\d+)(\d\d\.\d+)$", deg_min)
    if not m:
        return None
    deg = int(m.group(1))
    mins = float(m.group(2))
    dec = deg + mins / 60.0
    if hemi in ('S', 'W'):
        dec = -dec
    return dec

def parse_nmea_line(line):
    """
    Parse a NMEA line. Return dict with any of:
      'lat' (float), 'lon' (float), 'fix' (bool), 'sats' (int), 'hdop' (float), 'raw' (original line)
    Handles GPRMC and GPGGA lines.
    """
    if not line:
        return {}
    parts = line.strip().split(',')
    tag = parts[0].upper()
    result = {'raw': line.strip()}

    # RMC -> has status A = active and lat/lon fields
    if tag.endswith('RMC'):
        # Example: $GPRMC,hhmmss.ss,A,ddmm.mmmm,N,dddmm.mmmm,E,...
        if len(parts) > 6 and parts[2] == 'A':  # 'A' = valid
            lat = nmea_to_decimal(parts[3], parts[4]) if parts[3] and parts[4] else None
            lon = nmea_to_decimal(parts[5], parts[6]) if parts[5] and parts[6] else None
            if lat is not None and lon is not None:
                result['lat'] = lat
                result['lon'] = lon
                result['fix'] = True
        return result

    # GGA -> has fix quality, satellites, hdop, lat/lon
    if tag.endswith('GGA'):
        # fields: 0=$GPGGA,1=time,2=lat,3=N/S,4=lon,5=E/W,6=fix,7=num_sat,8=hdop,...
        if len(parts) > 8:
            try:
                fix_q = int(parts[6])
            except:
                fix_q = 0
            result['fix'] = (fix_q != 0)
            try:
                result['sats'] = int(parts[7])
            except:
                result['sats'] = None
            try:
                result['hdop'] = float(parts[8]) if parts[8] else None
            except:
                result['hdop'] = None
            lat = nmea_to_decimal(parts[2], parts[3]) if parts[2] and parts[3] else None
            lon = nmea_to_decimal(parts[4], parts[5]) if parts[4] and parts[5] else None
            if lat is not None and lon is not None:
                result['lat'] = lat
                result['lon'] = lon
        return result

    # GSV / GSA can be used for sats/hdop but we already handle main ones.
    return result
