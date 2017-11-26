set terminal wxt size 1200,1000
#set xrange [0:20]
set yrange [0:105]
#set xtics 0.3 2
set ytics 20 20
set xlabel "x axis" offset 0,0.5
set ylabel "y axis" offset 2,0

set term eps
set output "output.eps"
set key horizontal left

# Plot Statement
plot "nox.txt" using 1:2 title "Nox" ls 1 lw 5 smooth cspline,\
#     "2.txt" using 1:2 title "Open" ls 2 lw 2 smooth cspline,\
#     "3.txt" using 1:2 title "3" ls 3 lw 2 smooth cspline,\
#     "4.txt" using 1:2 title "4" ls 4 lw 2 smooth cspline,\
#     "5.txt" using 1:2 title "5" ls 5 lw 2 smooth cspline,\
#     "6.txt" using 1:2 title "6" ls 6 lw 2 smooth cspline,\
#     "7.txt" using 1:2 title "7" ls 7 lw 2 smooth cspline,\
#     "8.txt" using 1:2 title "8" ls 8 lw 2 smooth cspline,\
#     "9.txt" using 1:2 title "9" ls 9 lw 2 smooth cspline