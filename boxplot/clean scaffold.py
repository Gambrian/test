import sys
from Bio import SeqIO

f = open("Genome_noscaffold.fa","w")
for record in SeqIO.parse(sys.argv[1],"fasta"):
    if "chr" in record.id:
        f.write(">"+str(record.id+"\n"))
        f.write(str(record.seq+"\n"))
        
f.close()
