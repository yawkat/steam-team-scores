yellow=    "#b58900"
orange=    "#cb4b16"
red=       "#dc322f"
magenta=   "#d33682"
violet=    "#6c71c4"
blue=      "#268bd2"
cyan=      "#2aa198"
green=     "#859900"
grey=      "#CCCCCC"

set terminal pngcairo size 1000,600 font "Ubuntu"
set output ofile

unset key
set datafile separator "\t"
set xdata time
set timefmt "%s"
set format x "%H:%M"
set yrange [0:]
plot ifile using 1:(($2+$3+$4+$5+$6)/5) with lines linecolor rgb grey linewidth 3, \
     ifile using 1:2 with lines linecolor rgb red, \
     ifile using 1:5 with lines linecolor rgb green, \
     ifile using 1:4 with lines linecolor rgb magenta, \
     ifile using 1:3 with lines linecolor rgb cyan, \
     ifile using 1:6 with lines linecolor rgb violet