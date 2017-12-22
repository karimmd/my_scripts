set datafile separator ','
set autoscale 
set grid
set terminal wxt size 800,600

#set xrange [0:20]
#set yrange [0:1000]

#set logscale y
#set ytics auto

set xtics font ", 10"
set ytics font ", 10"

set xlabel font ", 14"
set ylabel font ", 14"


set xlabel "Time" offset 0,0.5
set ylabel "cpu utilization ovs-vswitchd (%)" offset 0,0.5


set key horizontal left


# Plot Statement

plot "switch_cpu.csv" using 1:2 title "Nox" ls 1 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:3 title "Pox" ls 2 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:4 title "Floodlight" ls 3 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:5 title "ODL" ls 4 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:6 title "ONOS" ls 5 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:7 title "Ryu" ls 6 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:8 title "OpenMul" ls 7 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:9 title "Beacon" ls 8 lw 1.5 w linespoints,\
     "switch_cpu.csv" using 1:10 title "Maestro" ls 9 lw 1.5 w linespoints 

pause -1