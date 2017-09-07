
## Installation steps
### Requirements
- Python3.
- Anaconda or pyhton-devel for Linux with pip.

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
##Command line help

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
```

```
geocoder.sh -f example.pdf -tGN
example.pdf will be geocoded
```

## Web interface
The auto geocoder tool provides a simple user interface to upload , geocode documents, review and see the geocoding results and its related texts. 
The web interface also gives support to classifier training module

### Setup
1.Install PostgresSQL
2.Create the geocoder database  database
```
createdb -Upostgres autogeocoder
```
3.Run sql script
```
psql -Upostgres -dautogeocoder -f sql/geocoder.sql

```
4.Update geocoder.ini set web port and database configuration
```
[postgres]
user_name=postgres
password=postgres
port=5432
host=localhost
db_name=geocoder

[web]
port=9095
```
5. Run python server.py and open http://localhost:9095

## Training your own text classifier
The text classifier attempts to reduce the number of false positives by eliminating those paragraph that shouldn’t be passed to the  named entity extraction phase, you can train your own classifier and make it learn about your documents.

## Classifier Training (Database configuration required please see web interface steps)
1. Download iati data from IATI registry
```
African Development Bank publisher code is 46002
geocoder.sh –c download --publisher=46002 --countries=ALL

```
1. Generate corpora table
```
geocoder.sh –c generate

```
2. Go to web interface and open training data manager link
3. Look for sentences that contains your geographical information and flag it as Geography
4. Look for other sentences and flag it as None
5. Train a new classifier
```
geocoder.sh -c train -n my_classifier
```
6. Eedit geocoder.ini and change default classifier name
```
[ie]
default_classifier= my_classifier
```
7. Geocode your documents

## Geocoding IATI activities
If a iati xml file is provided as input, the system will geocoded each activity by following the next steps:

2. Extract activity description
3. Download all documents tagged with code 02 or 07
4. Extract all sentences from documents
5. Geocode all sentences
6. Generate a new XML file containing activities and locations information.




