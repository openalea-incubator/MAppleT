set border 15 lw 0
set tics out
set xtics nomirror
set title

set xtics 0,1
plot [0:2] [0:24] "gnuplot_tmp_file11.dat" using 2 title "time up to the first occurrence of value 0 frequency distribution" with impulses
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:3] [0:12] "gnuplot_tmp_file11.dat" using 3 title "time up to the first occurrence of value 1 frequency distribution" with impulses
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:6] [0:2] "gnuplot_tmp_file11.dat" using 4 title "time up to the first occurrence of value 2 frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause 0 "End."
