from openalea.stocatree.file_tools import File_Index

dir = "PararunResults/"

subdirs = ["1994_6_30/", "1995_6_30/", "1996_6_30/", "1997_6_30/", "1998_6_30/",]

for d in subdirs:
	fi = File_Index(dir+d)
	print d, len(file_list("mtg")), len(file_list("lpk")), len(file_list("bgeom"))