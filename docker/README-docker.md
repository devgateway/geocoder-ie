
AMP Geocoder with Docker
=====

### Installation steps
1. Create dir geocoder
```
mkdir amp-geocoder
```

2. Pull the geocoder code from github and checkout the amp branch
```
git clone https://github.com/devgateway/geocoder-ie.git
git checkout amp
```

3. Prepare NER server
- Create dir ner inside amp-geocoder folder
```
mkdir ner
```
- download the needed files
```
- Download standford ner archive https://nlp.stanford.edu/software/stanford-ner-4.0.0.zip and extract it.
- Download french models: http://nlp.stanford.edu/software/stanford-corenlp-4.0.0-models-french.jar 
- Extract the file french-wikiner-4class.crf.ser.gz from stanford-corenlp-4.0.0-models-french.jar
- Copy french-wikiner-4class.crf.ser.gz into stanford-ner-4.0.0/classifiers folder
- Copy ner.sh from ./geocoder-ie/docker
```
- the ner folder should look like this:
```
geocoder/ner$ ls 
classifiers  lib  ner.sh  stanford-ner-4.0.0.jar
```
4. Configure docker by copying the ./geocoder-ie/docker files into the main geocoder folder
- Dockerfile
- amp-geocoder-up.sh
- amp-geocoder-down.sh
- docker-compose.yml

5. Update hosts for standford and postgres in /geocoder-ie/geocoder.ini
```
[standford]
host = ner
...

[postgres]
...
host = db
...
```
6. Run script ./amp-geocoder-up.sh

7. The server should be available on local: http://localhost:5000
