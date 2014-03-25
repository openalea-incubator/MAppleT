set border 15 lw 0
set tics out
set xtics nomirror
set title "smoothed observed probabilities"

set xtics 0,1
plot [0:6] [0:1] "gnuplot_tmp_file10.dat" using 4 title "observed value 0" with linespoints,\
"gnuplot_tmp_file10.dat" using 5 title "observed value 1" with linespoints,\
"gnuplot_tmp_file10.dat" using 6 title "observed value 2" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set title ""

set xtics 0,1
plot [0:6] [0:1] "gnuplot_tmp_file10.dat" using 1 title "observed value 0" with linespoints,\
"gnuplot_tmp_file10.dat" using 2 title "observed value 1" with linespoints,\
"gnuplot_tmp_file10.dat" using 3 title "observed value 2" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

plot [0:13] [0:10] "gnuplot_tmp_file11.dat" using 1 title "sequence length frequency distribution" with impulses

pause 0 "End."
