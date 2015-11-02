#参数设置

variable_list=['scaffold1','scaffold2','scaffold3','scaffold5']
evalue='20'
species_name='Bacillus.sp.T61'
query_len=80

import re

def find_gene_downstream(position_tuple):
    if '-' in position_tuple:
        n='inside'
        for i in open(variable+'.gff','r').readlines():
            element_list=i.split('	')
            if ((int(element_list[1].strip())-int(position_tuple[1])<0 and int(element_list[2].strip())-int(position_tuple[1])>0) or (int(element_list[1].strip())-int(position_tuple[2])<0 and int(element_list[2].strip())-int(position_tuple[2])>0)):
                return 'inside'
            else:
                if (int(element_list[2].strip())-int(position_tuple[1]))>0:
                    return n
                else:
                    n=element_list[0]
    else:
        for i in open(variable+'.gff','r').readlines():
            element_list=i.split('	')
            if ((int(element_list[1].strip())-int(position_tuple[1])<0 and int(element_list[2].strip())-int(position_tuple[1])>0) or (int(element_list[1].strip())-int(position_tuple[2])<0 and int(element_list[2].strip())-int(position_tuple[2])>0)):
                return 'inside'
            else:
                if (int(element_list[1].strip())-int(position_tuple[2]))>0:
                    return element_list[0]

def find_gene_upstream(position_tuple):
    if '-' in position_tuple:
        n='inside'
        for i in open(variable+'.gff','r').readlines():
            element_list=i.split('	')
            if ((int(element_list[1].strip())-int(position_tuple[1])<0 and int(element_list[2].strip())-int(position_tuple[1])>0) or (int(element_list[1].strip())-int(position_tuple[2])<0 and int(element_list[2].strip())-int(position_tuple[2])>0)):
                return 'inside'
            else:
                if (int(element_list[1].strip())-int(position_tuple[2]))>0:
                    return element_list[0]
    else:
        for i in open(variable+'.gff','r').readlines():
            element_list=i.split('	')
            if ((int(element_list[1].strip())-int(position_tuple[1])<0 and int(element_list[2].strip())-int(position_tuple[1])>0) or (int(element_list[1].strip())-int(position_tuple[2])<0 and int(element_list[2].strip())-int(position_tuple[2])>0)):
                return 'inside'
            else:
                if (int(element_list[2].strip())-int(position_tuple[1]))>0:
                    return n
                else:
                    n=element_list[0]

annotation_dict={}
count_dict={}

for i in open('Bacillus.sp.T61.annotation.table','r').readlines():
    lin=re.findall('(Bacillus.sp.T61GL[0-9]{6})	({.*})',i)
    annotation_dict[lin[0][0]]=lin[0][1]

for variable in variable_list:

    out_down=open('result_e'+evalue+'_'+variable+'_down.th','w')
    out_up=open('result_e'+evalue+'_'+variable+'_up.th','w')

    f=open('e'+evalue+'_'+variable+'.th','r').read()

    range_list=f.split('Range ')
    position_match=[]

    for i in range_list:
        if i:
            n=0
            if 'Minus' in i:
                position_min_list=re.findall(': ([0-9]*?) to',i)
                position_max_list=re.findall(' to ([0-9]*?)GraphicsNext',i)
                number=re.findall('^([0-9]*?): ',i)
                position_match_tuple=re.findall('Query  ([0-9]*?)[^0-9]*?([0-9]*?)\n',i)
                gene_name_down=find_gene_downstream(('-',position_min_list[0],position_max_list[0]))
                gene_name_up=find_gene_upstream(('-',position_min_list[0],position_max_list[0]))
                if 'inside' not in gene_name_down:
                    out_down.write(variable+'	'+'Range '+number[0]+'	'+gene_name_down+'	'+annotation_dict[gene_name_down]+"\n")
                    n+=1
                if 'inside' not in gene_name_up:
                    out_up.write(variable+'	'+'Range '+number[0]+'	'+gene_name_up+'	'+annotation_dict[gene_name_up]+"\n")
                    n+=1
            else:
                position_min_list=re.findall(': ([0-9]*?) to',i)
                position_max_list=re.findall(' to ([0-9]*?)GraphicsNext',i)
                number=re.findall('^([0-9]*?): ',i)
                position_match_tuple=re.findall('Query  ([0-9]*?)[^0-9]*?([0-9]*?)\n',i)
                gene_name_down=find_gene_downstream(('+',position_min_list[0],position_max_list[0]))
                gene_name_up=find_gene_upstream(('+',position_min_list[0],position_max_list[0]))
                if 'inside' not in gene_name_down:
                    out_down.write(variable+'	'+'Range '+number[0]+'	'+gene_name_down+'	'+annotation_dict[gene_name_down]+"\n")
                    n+=1
                if 'inside' not in gene_name_up:
                    out_up.write(variable+'	'+'Range '+number[0]+'	'+gene_name_up+'	'+annotation_dict[gene_name_up]+"\n")
                    n+=1
            if n!=0:
                for p in position_match_tuple:
                    position_match.append(p)

    out_down.close
    out_up.close

    for i in position_match:
        for n in [str(x) for x in range(int(i[0]),int(i[1])+1)]:
            if n in count_dict.keys():
                count_dict[n]+=1
            else:
                count_dict[n]=1

out_R=open('count_plot.R','w')
out_R.write('x=c(')
for k in [x for x in range(0,query_len)]:
    if k==query_len-1:
        out_R.write(str(k+1)+')\n')
    else:
        out_R.write(str(k+1)+',')
out_R.write('y=c(')
for l in [x for x in range(0,query_len)]:
    if l==query_len-1:
        if str(l) in count_dict.keys():
            out_R.write(str(count_dict[str(l)])+')\n')
        else:
            out_R.write('0'+')\n')
    else:
        if str(l) in count_dict.keys():
            out_R.write(str(count_dict[str(l)])+',')
        else:
            out_R.write('0'+',')
out_R.write('plot(x,y,type="h",main="abundance: '+species_name+'",xlab="query_seq",ylab="hit_number")')
out_R.close