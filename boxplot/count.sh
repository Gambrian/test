#!/bin/bash


#PBS -N boxplot
#PBS -l nodes=1:ppn=6
#PBS -q batch


#delete scaffold in reference genome
python clean_scaffold.py GRCm38.primary_assembly.genome.fa
 
#makewindows
##Statistical chromosome length
pip install pyfaidx
faidx Genome_noscaffold.fa -i chromsizes > sizes.genome
bedtools makewindows -g sizes.genome -w 10000 > 10k_Genomewindows.bed

#statistc number of reads in the window
path="/home/zyang/yjgeng/boxplot/pooled_tagAlign/"
files=$(ls $path |grep ".gz")
for filenames in $files
do
	startpath="/home/zyang/yjgeng/boxplot/pooled_tagAlign/"$filenames
	endpath="/home/zyang/yjgeng/boxplot/sorted/"${filenames}"_sorted"
	countfile="/home/zyang/yjgeng/boxplot/count/"$filenames"_10kcount.bed"
	zcat $startpath|sort -k 1,1 -k 2,2n - > $endpath
	bedtools coverage -a "/home/zyang/yjgeng/boxplot/10k_Genomewindows.bed" -b $endpath > $countfile
	echo -e $endpath"has been done.\n"
done


#sed -n "5000,5050p" 10k_counts.bed
