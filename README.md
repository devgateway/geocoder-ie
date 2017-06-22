# autogeocoder
Automatically  geocode aid projects by applying natural language processing techniques, try it by executing geocode.py passing a valid iati activity identifier.


you need to have running standford ner server

java -mx400m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 1234

then run the geocode script passing a iati identifier as argument



python geocode.py  46002-P-GN-DB0-005


you will obtain a result like

 Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md] [PlDb] |
| Github | [plugins/github/README.md] [PlGh] |
| Google Drive | [plugins/googledrive/README.md] [PlGd] |
| OneDrive | [plugins/onedrive/README.md] [PlOd] |
| Medium | [plugins/medium/README.md] [PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md] [PlGa] |

 Place | Text |
| ------ | ------ |
|Guinea |                  COUNTRY AND NAME OF PROJECT : Guinea: Tombo-Gbessia Road Improvement       Project  2.|
|Tombo-Gbessia Road |      PROJECT DESCRIPTION  : The Project has the following components:  A - Works comprising:  a.1) the im |
|Kenien-Bonfi       |     PROJECT DESCRIPTION  : The Project has the following components:  A - Works comprising:  a.1) the im |
|Madina             |     PROJECT OBJECTIVE  2.1 a) Improve traffic fluidity and reduce transport costs and travel time on the |
|Tombo-Gbessia      |     OUTCOMES  3.1 Tombo-Gbessia road completed, permanent structures constructed, feeder road constructe |
|Conakry            |     3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
|Kenien-Bonfi       |     3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
|Yimbaya            |     3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
