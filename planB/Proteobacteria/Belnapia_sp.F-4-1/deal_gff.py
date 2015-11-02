import re

f=open('gff.th','w')

for i in open('Belnapia_sp.F-4-1.glimmer.gff','r').readlines():
    if 'glimmer	mRNA	' in i:
        r1=re.findall('^(Scaffold[0-9]*?)	glimmer',i)
        r2=re.findall('glimmer	mRNA	([0-9]*?)	',i)
        r3=re.findall('	([0-9]*?)	\.	',i)
        r4=re.findall('ID=(Belnapia_sp.F-4-1GL[0-9]{6});Name',i)
        f.write(r1[0]+'	'+r4[0]+'	'+r2[0]+'	'+r3[0]+"\n")
