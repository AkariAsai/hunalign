cat cross-lingual-index.txt | awk '{ print NF,NF*(NF-1)/2 }' | sort -n | uniq -c | awk '{ print $1,$2,$3,$1*$3 }' | tr ' ' '\t' | sort -n -k 3 | awk '{ s+=$4 ; print }  END { print s }'

22581	1	0	0
40480	2	1	40480
2090	3	3	6270
990	4	6	5940
627	5	10	6270
393	6	15	5895
248	7	21	5208
223	8	28	6244
329	9	36	11844
1876	10	45	84420
76234	11	55	4192870
5269	12	66	347754
258	13	78	20124
164	14	91	14924
225	15	105	23625
285	16	120	34200
374	17	136	50864
567	18	153	86751
2504	19	171	428184
2816	20	190	535040
912	21	210	191520
12321	22	231	2846151
18	23	253	4554
8949132


cd sentences
wget -r l2 http://optima.jrc.it/Resources/DCEP-2013/sentences/list.html

tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-strip-CS-pub.tar.bz2 > cout 2> cerr
tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-strip-CS-pub.tar.bz2 > cout2 2> cerr2
tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-DA-pub.tar.bz2 > cout 2> cerr
tar xjvf optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-CS-pub.tar.bz2 > cout2 2> cerr2

cat DCEP/strip/sgml/CS/QT/8369873__QT__H-2004-0355__CS.txt
cat DCEP/sentence/sgml/CS/QT/8369873__QT__H-2004-0355__CS.txt

# OMG stupid sentence segmenter fucks all dates.

cd DCEP/sentence # Now at ~/big/experiments/DCEP/sentences/DCEP/sentence
cat ../../../cross-lingual-index.txt | awk '{ s="" ; c=0 ; for (i=1;i<=NF;++i) { a=$i ; if ((a~/\/CS\//)||(a~/\/DA\//)) { s = s a " " ; ++c } } ; if (c==2) { print s } }' | sed "s/ $//" | sed "s/\.[a-z]*\.gz/.txt/g" | head -5 | while read a b ; do ls $a $b ; done

####

# The last effort was under ~/big/experiments/AcquisExtended2/raw
# , that's where all the nice scripts are. This is the hierarchy:

- alignallpairsforalldocs.sh
  - alignallpairs.sh
    - alignonepair.sh
      - hunalign
- bisentsforalllanguagepairs.sh
  - bisentsforlanguagepair.sh
    - ladder2text.sh
    - filteralign.sh
- dictsforalllanguagepairs.sh
  - dictforlanguagepair.sh
    - coocc
- alignallpairsforalldocs.withdic.sh
  - as to be expected
- convert to some output that everyone likes, originally ladder2jrc.allpairsforalldocs.sh and ladder2jrc.awk

####

# What's gonna be the document id? The cross-lingual-index.txt
# doesn't have this notion, per se.

cd ~/big/experiments/DCEP/sentences/DCEP/sentence
cat cross-lingual-index.txt | awk 'BEGIN { FS="/" }  { split($0,a,"__") ; s = $1 "." a[2] "." a[3] ; print s }' | sort > /tmp/x
diff /tmp/x <(uniq /tmp/x) | grep "^<" | wc -l
5945
cat cross-lingual-index.txt | awk 'BEGIN { FS="/" }  { split($0,a,"__") ; s = a[2] "." a[3] ; print s }' | sort > /tmp/y
diff /tmp/y <(uniq /tmp/y) | grep "^<" | wc -l
5945

# -> Oops, that's not a uniq id.

cat cross-lingual-index.txt | awk '{ printf("%06d\t%s\n", NR, $0) }' | less 


# Okay, let's unpack all of 'em.

cd DCEP/sentences # Now at ~/big/experiments/DCEP/sentences                                                                      
ls optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-* | cut -f4 -d'-' > langs.txt
# unzip does a tar jxvf for all strip and sentence files:
nohup bash unzip.sh > cout 2> cerr &

cd ~/big/experiments/DCEP/
cat cross-lingual-index.txt | awk '{ printf("%06d\t%s\n", NR, $0) }' > named-cross-lingual-index.txt 

# Moved ~/big/experiments/DCEP/ssplit and ssplit-DCEP.tar into ~/big/experiments/DCEP/Attic , they
# are obsoleted by Jaakko's versions.
# Moved Jaakko's versions from ~/big/experiments/DCEP/sentences/DCEP/ to ~/big/experiments/DCEP/tree
# Here tree refers to the original directory structure (sgml/OT/whatever), and flat will refer to my
# numerical id (did) based structure.
# The zipped ones stayed at ~/big/experiments/DCEP/sentences
mv sentences/DCEP/sentence tree 
mv sentences/DCEP/strip tree

# Let's do the tokenization still on the tree struct.
find tree/sentence -type d > struct-of-tree.txt # Takes 4 minutes even on kruso.
cat struct-of-tree.txt | sed "s/^tree\/sentence/tree\/tok/" | while read d ; do mkdir -p "$d" ; done
nohup bash hunalign/scripts/DCEP/tokenizeAll.sh > cout.tokenizeAll 2> cerr.tokenizeAll &
# Actually, I forgot the nohup but dropping the conn still didn't kill it somehow.
# I wonder if it will eventually realize it. Estimated to take 13 hours.

# Parallelly (having two strings to my bow) I unpacked it on my laptop,
# under ~/experiments/DCEP/DCEP. Will rename it to DCEP/tree and run the tokenizer. Seems to be OS X compatible.

# Both finished, the kruso one and the macbook one.
# macbook needed 5.5 hours for tok, and 3.5 hours to verify line counts.
# kruso needed 43.1 hours for tok, and randomly failed (produced 0 byte output) on 49 files,
# documented in cout.tokenizeAll. Also, it seems like the verification did not finish,
# the final "Done." line and date is missing from the output.
# I see no good reason to use kruso at this point.
