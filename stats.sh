#!/bin/sh
#while true; do
file=$1
cwd="$(pwd)"
if [ ! -f "${cwd}/tagsoup-1.2.1.jar" ]
then
	wget "http://vrici.lojban.org/~cowan/XML/tagsoup/tagsoup-1.2.1.jar"
fi
i=0
cat $file | while read line
do
	wget ${line} -O "shpe_notion${i}.html"
	java -jar tagsoup-1.2.1.jar --files "shpe_notion${i}.html"
	#python3 parser.py "shpe_notion${i}.xhtml"
	#rm *shpe_notion*
	echo $((i=i+1))
done
#sleep 30m
#done
