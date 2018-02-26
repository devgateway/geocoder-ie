
AutoGecoder
=====
 AutoGeocoder tool reads through text provided in various document formats (PDF, DOC, TXT) to identify activity locations, and then produces a final list of georeferenced location names. The tool has been fully developed in Python 3, and combines well-known tools and libraries such as NLTK and scikit-learn.


## Installation steps
### Requirements
- Python3.
- Anaconda or pip (pyhton-devel is required).

### Installation steps
1. Install dependencies usin pip or anaconda
```
(Linux pip)
pip install -r requirements

(Anaconda)
conda install --yes --file requirements.txt
```
2. Download Stanford NER from https://nlp.stanford.edu/software/CRF-NER.shtml#Download
3. Start Standford NER Server

```
java -mx400m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer
-loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 9094

```
4. Run python setup.py to get NLKT data.
5. Update Stanford setting in geocoder.ini
```
[standford]
host = localhost
port = 9094
```

## Using the tool

### Command line help

```
geocoder.sh --help

sage: main.py [-h] [-c {geocode,download,generate,train}]
               [-f FILE [FILE ...]] [-p ORGANISATION] [-t COUNTRIES]
               [-l LIMIT] [-n NAME]

Auto-geocode activity projects

optional arguments:
  -h, --help            show this help message and exit
  -c {geocode,download,generate,train}, --command {geocode,download,generate,train}
                        Use geocode to auto-geocode file. Use download to get
                        raw data from IATI registry. Use generate to generate
                        a corpora. Use train to train a new classifier
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Use together with -c geocode to pass a file to
                        process, The file can be a IATI activities file, pdf
                        document, odt document or txt file
  -p ORGANISATION, --publisher ORGANISATION
                        Use together with -c download to download data of
                        specific IATI Publisher
  -t COUNTRIES, --countries COUNTRIES
                        Use together with -c geocode to filter geonames search
                        Use together with -c download to download data of
                        specific countries
  -l LIMIT, --limit LIMIT
                        Use together with -c download to limit the Number of
                        activities to download for each publisher/country
  -n NAME, --name NAME  set the new classifier name
  -o {xml,tsv,json}, --output {xml,tsv,json}
                        Set output format, default json
```

```
geocoder.sh -f example.pdf -tGN
example.pdf will be geocoded
(geocoder) C:\projects\clean_copy>geocoder.sh  -f example.pdf -tGN -otsv
example.pdf will be geocoded
2017-09-07 10:17:04,637 root         INFO     Detecting document language
2017-09-07 10:17:05,152 root         INFO     Splitting document in sentences

Reading pdf pages  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30

2017-09-07 10:17:08,970 root         INFO     There are 380 sentences to process, split took 4.321118570914758ms
2017-09-07 10:17:08,985 root         INFO     80 geographical sentences found
2017-09-07 10:17:10,080 root         INFO     NER extraction took 1.0949942523466651ms
2017-09-07 10:17:11,106 root         INFO     fouta djallon was geocode as RGN with coordinates 11.5,-12.5
2017-09-07 10:17:11,666 root         INFO     gaoual was geocode as ADM2 with coordinates 11.75,-13.2
2017-09-07 10:17:12,241 root         INFO     koundara was geocode as ADM2 with coordinates 12.41667,-13.16667
2017-09-07 10:17:12,921 root         INFO     middle guinea was geocode as RGN with coordinates 11,-12.5
2017-09-07 10:17:13,469 root         INFO     Wasn't able to geocode  niger
2017-09-07 10:17:13,470 root         INFO     Let's try using others parameters
2017-09-07 10:17:14,029 root         INFO     niger was geocode as PRK with coordinates 10.5,-10.2
2017-09-07 10:17:14,572 root         INFO     guinea was geocode as PCLI with coordinates 10.83333,-10.66667
2017-09-07 10:17:15,194 root         INFO     republic of guinea was geocode as PCLI with coordinates 10.83333,-10.66667
2017-09-07 10:17:15,749 root         INFO     conakry was geocode as ADM1 with coordinates 9.60703,-13.597
2017-09-07 10:17:16,447 root         INFO     koundara prefectures was geocode as ADM2 with coordinates 12.41667,-13.16667
2017-09-07 10:17:16,447 root         INFO     ua Too short location name
2017-09-07 10:17:17,034 root         INFO     Wasn't able to geocode  atlantic ocean
2017-09-07 10:17:17,034 root         INFO     Let's try using others parameters
2017-09-07 10:17:17,613 root         INFO     Wasn't able to geocode  atlantic ocean
2017-09-07 10:17:18,174 root         INFO     upper guinea was geocode as RGN with coordinates 10.5,-9.5
Results were saved in out.tsv
```


Output format (-o)

xml: is only supported when processing a iati xml file, and the output is a copy of the original xml file  with new locations embedded.
tsv and json can be used for any input file.

## Web interface
AutoGeocoder tool provides a simple user interface to upload, geocode documents, review and see the geocoding results and its related texts.

### Setup
1. Install PostgresSQL
2. Create the geocoder database  database
```
createdb -Upostgres autogeocoder
```
3. Run sql script
```
psql -Upostgres -dautogeocoder -f sql/geocoder.sql

```
4. Database configuration (geocoder.ini)
```
[postgres]
 user_name=postgres
 password=postgres
 port=5432
 host=localhost
 db_name=geocoder
```


5. Web configuration (uwsgi.ini)
```
[uwsgi]
project = autogeocoder
module = wsgi
wsgi-file=/src/wsgi.py
master = true
processes = 5
socket = 0.0.0.0:9095
protocol = http
callable = app
chdir=/home/sdimunzio/projects/geocoder-ie/src/
virtualenv=/home/sdimunzio/envs/geocoder/
die-on-term = true
```

6. Run python server.py and open http://localhost:9095

## Training your own text classifier
The text classifier attempts to reduce the number of false positives by eliminating those paragraph that shouldn’t be passed to the  named entity extraction phase, you can train your own classifier and make it learn about your documents.


## Classifier Training
The default classifier has been trained with a small dataset, 
so it is recommended that users train their own text classifiers to achieve enhanced precision.

Before following  bellow steps you should ensure AutoGeocoder's database is already configured.


1. Download iati data from IATI registry
```
African Development Bank publisher code is 46002
geocoder.sh –c download --publisher=46002 --countries=ALL

```
2. Generate corpora table
```
geocoder.sh –c generate

```
3. Go to web interface and open training data manager link
4. Look for sentences that contains your geographical information and flag it as Geography
5. Look for other sentences and flag it as None
6. Train a new classifier
```
geocoder.sh -c train -n my_classifier
```
7. Eedit geocoder.ini and change default classifier name
```
[ie]
default_classifier= my_classifier
```
8. Geocode your documents
```
geocoder.sh -f mydocument.pdf
```


## AutoGeocoder process workflow


![Alt text](workflow-image.png?raw=true "Workflow")

## Geocoder Suite Technical Guide
For detailed installation instructions please look at the technical guide https://drive.google.com/file/d/1QhGoI_syJq3FqO0lm3Zc7j5ziuWro5TK/view
