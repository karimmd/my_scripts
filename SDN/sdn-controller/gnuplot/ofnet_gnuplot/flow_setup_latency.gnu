set datafile separator ','
set autoscale 
set grid
set terminal wxt size 800,600

#set xrange [0:20]
#set yrange [0.1:7000]

#set logscale y 
#set ytics auto



set xtic auto
set ytic auto


set xtics font ", 10"
set ytics font ", 10"

set xlabel font ", 14"
set ylabel font ", 14"


set xlabel "Time" offset 0,0.5
set ylabel "average flow setup latency in milliseconds" offset 0,0.5


set key horizontal left


# Plot Statement

plot "flow_setup_latency.csv" u 1:2 smooth csplines title "Nox" ls 1 lw 2.5,\
     "flow_setup_latency.csv" u 1:3 smooth csplines title "Pox" ls 2 lw 2.5,\
     "flow_setup_latency.csv" u 1:4 smooth csplines title "Floodlight" ls 3 lw 2.5,\
     "flow_setup_latency.csv" u 1:5 smooth csplines title "ODL" ls 4 lw 2.5,\
     "flow_setup_latency.csv" u 1:6 smooth csplines title "ONOS" ls 5 lw 3,\
     "flow_setup_latency.csv" u 1:7 smooth csplines title "Ryu" ls 6 lw 2.5,\
     "flow_setup_latency.csv" u 1:8 smooth csplines title "OpenMul" ls 7 lw 2.5,\
     "flow_setup_latency.csv" u 1:9 smooth csplines title "Beacon" ls 8 lw 2.5,\
     "flow_setup_latency.csv" u 1:10 smooth csplines title "Maestro" ls 9 lw 2.5 

pause -1