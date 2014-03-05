import os
from openalea.stocatree.file_tools import File_Index, Merge

output_dir = "PararunResults/"

fi = File_Index("PararunResults/*/")

#The structure of dic is like:
"""
    {
        "1.txt":["c:/a/1.txt", "c:/b/1.txt"],
        "2.txt":["c:/a/2.txt", "c:/b/2.txt"]
    }

"""
dic = {}
for p in fi.path_list("csv"):
    (d,f) = os.path.split(p)
    if f not in dic.keys():
        dic.update({f:[p]})
    else:
        dic[f].append(p)

for f,p_list in dic.iteritems():
    mg = Merge(src_files=p_list, dst_file=output_dir+f,
                header="Grwoth_Date")

