(5..50).map{|x| x*0.5}.flat_map{|x| [0.10,0.15,0.20,0.25].map{|t| [x,((t*x)*2).round / 2.0]}}.map{|x, y| (10000*y/x).to_i/100.0}.uniq.sort.take(9)

