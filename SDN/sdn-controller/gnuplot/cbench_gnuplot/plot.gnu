set datafile separator ','
set autoscale 
set grid
set terminal wxt size 800,600



#set xrange [0:20]
#set yrange [0:100000]

#set xtics 0.3 2
set xtic auto
#set ytics 20 20
set ytic auto
set xtics font ", 10"
set ytics font ", 10"

set xlabel font ", 14"
set ylabel font ", 14"




set xlabel "Number of Loops" offset 0,0.5
set ylabel "Responses per milliseconds(ms)" offset 0,0.5

#set term eps
#set output "output.eps"

set key horizontal left

# Plot Statement

plot "latency_loop.csv" using 1:2 title "Nox"  with linespoints pt 2 lc rgb '#000000' lw 4,\
     "latency_loop.csv" using 1:3 title "Pox" with linespoints pt 4 lc rgb '#16469D' lw 4,\
     "latency_loop.csv" using 1:4 title "Floodlight" with linespoints pt 6 lc rgb '#BD202D' lw 4,\
     "latency_loop.csv" using 1:5 title "ODL" with linespoints pt 8 lc rgb '#00A14B' lw 4,\
     "latency_loop.csv" using 1:6 title "ONOS" with linespoints pt 10 lc rgb '#4B96D1' lw 4,\
     "latency_loop.csv" using 1:7 title "Ryu" with linespoints pt 12 lc rgb '#F16521' lw 4,\
     "latency_loop.csv" using 1:8 title "OpenMul" with linespoints pt 14 lc rgb '#9F6EAF' lw 4,\
     "latency_loop.csv" using 1:9 title "Beacon" with linespoints pt 1 lc rgb'#20B2AA' lw 4,\
     "latency_loop.csv" using 1:10 title "Maestro" with linespoints pt 3 lc rgb '#FF1493' lw 4 

pause -1