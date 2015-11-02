import re

f=open('gff.th','w')

for i in open('Bacillus.sp.T61.glimmer.gff','r').readlines():
    if 'Scaffold' in i:
        if 'RefSeq	gene' in i:
            r1=re.findall('(Scaffold[0-9]*?)	glimmer',i)
            r2=re.findall('glimmer	gene	([0-9]*?)	',i)
            r3=re.findall('	([0-9]*?)	\.	',i)
            r4=re.findall('	ID=(Bacillus.sp.T61GL[0-9]{6});Name',i)
            f.write(r1[0]+'	'+r4[0]+'	'+r2[0]+'	'+r3[0]+"\n")
        elif 'RefSeq	exon' in i:
            r1=re.findall('(Scaffold[0-9]*?)	glimmer',i)
            r2=re.findall('RefSeq	exon	([0-9]*?)	',i)
            r3=re.findall('	([0-9]*?)	\.	',i)
            r4=re.findall('	ID=(Bacillus.sp.T61GL[0-9]{6});Name',i)
            f.write(r1[0]+'	'+r4[0]+'	'+r2[0]+'	'+r3[0]+"\n")
