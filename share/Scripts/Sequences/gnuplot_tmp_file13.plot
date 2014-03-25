set border 15 lw 0
set tics out
set xtics nomirror
set title

set xtics 0,1
plot [0:5] [0:36] "gnuplot_tmp_file11.dat" using 5 title "value 0 recurrence time frequency distribution" with impulses
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:55] "gnuplot_tmp_file11.dat" using 6 title "value 1 recurrence time frequency distribution" with impulses
set xtics autofreq

pause 0 "End."
