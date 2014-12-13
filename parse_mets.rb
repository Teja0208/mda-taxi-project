#
# ruby -lan parse_mets.rb

require 'date'
require 'time'

puts [$_.split(',')[0,2]].map{|date_str, time_str|
  date = Date.strptime(date_str, "%m/%d/%y")
  time = Time.parse(time_str)

  fmt_dt = lambda{|d,t| d.strftime("%F ") + t.strftime("%T")}

"dropoff_datetime > '" + fmt_dt[date, time - 30*60] + "' AND dropoff_datetime < '" + fmt_dt[date, time + 30*60] + "' OR "
}.first rescue next


