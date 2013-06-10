import json

print "CARREGANDOOS OS DADOS"
with open( 'libras_signs_videos_bkp.json', 'rb' ) as fp:
  data = json.load( fp )

print len(data)

for d in data:
  print "\n" + d + ":",
  for e in data[d]:
    print e,
