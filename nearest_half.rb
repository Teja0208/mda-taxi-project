2.5.step(25, 0.5).flat_map{|x| [10,15,20,25].map{|t| [x,(2*t/100.0*x).round / 2.0]}}.map{|x, t| (10000*t/x).to_i/100.0}.uniq.sort.take(9)

