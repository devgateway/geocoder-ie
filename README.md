## Installation steps.

Python 3 is required.

For Windows, use anaconda to install prebuilt dependencies.

For Linux, you need to have pyhton devel package installed.

### Installation steps

1. Install dependencies by running
```
pip install -r requirements
```
2. Download Stanford CoreNLP from http://nlp.stanford.edu/software and run it with the following command
```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9094 -timeout 15000
```
3. Run python setup.py to download NLKT data
4. Update Stanford setting in geocoder.ini
 ```
  [standford]
  host = localhost
  port = 9094
```
## Using the tool
 ```
geocoder.sh -f example.pdf –countries=
example.pdf will be geocoded
Creating pdf reader for file example.pdf
Detecting document language
Splitting document in sentences
Reading pdf pages  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
There are 380 sentences to process, split took 4.390625451791191ms
31 geographical sentences found
NER extraction took 14.84089016175976ms
Fouta Djallon was geocode as RGN with coordinates 11.5,-12.5
Gaoual was geocode as ADM2 with coordinates 11.75,-13.2
Koundara was geocode as ADM2 with coordinates 12.41667,-13.16667
Guinea was geocode as PCLI with coordinates 10.83333,-10.66667
Republic of Guinea was geocode as PCLI with coordinates 10.83333,-10.66667
Conakry was geocode as ADM1 with coordinates 9.60703,-13.597
Koundara Prefectures was geocode as ADM2 with coordinates 12.41667,-13.16667
UA Too short location name
Wasn't able to geocode  Cheick Amadou
Let's try using others parameters
Wasn't able to geocode  Cheick Amadou
Results were saved in out.tsv
 ```

## Web interface

The auto geocoder tool also offers a simple user interface.

The interface allows to upload and geocode documents, review and see the geocoding results and its related texts. The web interface also gives support to classifier training module

### Setup
1.	Install PostgresSQL
2.	Create a new database
createdb -Upostgres autogeocoder
3.	Run db.sql file
 ```
   psql -Upostgres -dautogeocoder -f sql/db.sql
 ```
4.	Update geocoder.ini set web port and database configuration
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

One of the key pieces of the tool is the text classification module.
The classifier attempts to reduce the number of false positives by eliminating those paragraph that shouldn’t be passed the named entity extraction phase, you can train your own classifier and make it learn about your documents.
Classifier Training (Database configuration required please see web interface steps)

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

2)	Extract activity description
3)	Download all documents tagged with code 02 or 07
4)	Extract all sentences from documents
5)	Geocode all sentences
6)	Generate a new XML file containing activities and locations information.




