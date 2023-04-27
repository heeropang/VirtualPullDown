#!/bin/bash

dataset_number=39

new_names=(
"FS868_RS17480.fa_pair"
"FS868_RS17485.fa_pair"
"FS868_RS17490.fa_pair"
"FS868_RS17495.fa_pair"
"FS868_RS17500.fa_pair"
"FS868_RS17505.fa_pair"
"FS868_RS17510.fa_pair"
"FS868_RS17515.fa_pair"
"FS868_RS17535.fa_pair"
"FS868_RS17540.fa_pair"
"FS868_RS17545.fa_pair"
"FS868_RS17550.fa_pair"
"FS868_RS17555.fa_pair"
"FS868_RS17560.fa_pair"
"FS868_RS17565.fa_pair"
"FS868_RS17570.fa_pair"
"FS868_RS17575.fa_pair"
"FS868_RS17585.fa_pair"
"FS868_RS17590.fa_pair"
"FS868_RS17595.fa_pair"
"FS868_RS17600.fa_pair"
"FS868_RS17610.fa_pair"
"FS868_RS17615.fa_pair"
"FS868_RS17625.fa_pair"
"FS868_RS17630.fa_pair"
"FS868_RS17640.fa_pair"
"FS868_RS17645.fa_pair"
"FS868_RS17650.fa_pair"
"FS868_RS17660.fa_pair"
"FS868_RS17665.fa_pair"
"FS868_RS17670.fa_pair"
"FS868_RS17675.fa_pair"
"FS868_RS17680.fa_pair"
"FS868_RS17685.fa_pair"
"FS868_RS17690.fa_pair"
"FS868_RS17695.fa_pair"
"FS868_RS17700.fa_pair"
"FS868_RS27700.fa_pair"
"FS868_RS27705.fa_pair"
"FS868_RS28195.fa_pair"
)

for i in $(seq 0 $dataset_number); do
    prefix="$i"_
    for f in "$prefix"*; do
        new_name="${new_names[i]}_${f#$prefix}"
        mv "$f" "$new_name"
    done
done
