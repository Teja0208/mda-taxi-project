#NYC boundaries -74.05, -73.85,    40.67, 40.85

@min_lat = 40.67
@max_lat = 40.85
@range_lat = @max_lat - @min_lat

def scale_lat(lat)
  (lat - @min_lat) / @range_lat
end

def nyc_lat?(lat)
  lat > @min_lat && lat < @max_lat
end


@min_lon = -74.05
@max_lon = -73.85
@range_lon = @max_lon - @min_lon

def scale_lon(lon)
  (lon - @min_lon) / @range_lon
end

def nyc_lon?(lon)
  lon > @min_lon && lon < @max_lon
end

pts = $_.split(',')[10,4].map(&:to_f) rescue return

if nyc_lon?(pts[0]) && nyc_lat?(pts[1]) && nyc_lon?(pts[2]) && nyc_lat?(pts[3])
  
  puts [scale_lon(pts[0]), scale_lat(pts[1]),
        scale_lon(pts[2]), scale_lat(pts[3])].join(',')
end
