#!/usr/bin/sh
#du -sh . &  # Start the command in the background
TREMSUCS -p TCGA-CESC -p TCGA-HNSC -p TCGA-LUSC -d carboplatin -d carboplatin,paclitaxel -d cisplatin -C 5 -C 8 -t 5 -t 10 -t 20 -o /scr/palinca/gabor/TCGA-pipeline_12_pval_prod -c 40 &
PID=$!
ps -o pid,comm,%mem,rss,etime,%cpu,start,time -p $PID >> memory_log.txt
sleep 1m
while kill -0 $PID 2> /dev/null; do
    ps -o pid,comm,%mem,rss,etime,%cpu,start,time -p $PID | sed '1d' >> memory_log.txt
    sleep 1m
done
