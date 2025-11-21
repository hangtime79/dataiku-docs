import sys, os, os.path as osp

header ="""<?xml version='1.0' encoding='UTF-8'?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
         xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

sitemap = header

items = []

def append(dirpath, filename):
	global sitemap
	if filename == "index.html":
		items.append("<url><loc>https://doc.dataiku.com/dss/latest/%s</loc></url>" % dirpath)
	else:
		items.append("<url><loc>https://doc.dataiku.com/dss/latest/%s/%s</loc></url>" % (dirpath, filename))

append("", "index.html")

for t in os.walk("build/html"):
	#(dirpath, dirnames, filenames) = t
	dirpath = t[0]
	if not dirpath.startswith("build/html/"):
		continue
	dirpath = dirpath.replace("build/html/", "")
	if dirpath.startswith("_"):
		continue
	for filename in t[2]:
		append(dirpath, filename)

items.sort()

sitemap += "\n".join(items)

sitemap += """
</urlset>"""

print sitemap