# autogeocoder
Automatically  geocode aid projects by applying natural language processing techniques, try it by executing geocode.py passing a valid iati activity identifier.


you need to have running standford ner server

java -mx400m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 1234

then run the geocode script passing a iati identifier as argument
python geocode.py  46002-P-GN-DB0-005


you will obtain a result like


+---------------------------------------+------------------------------------------------------------------------------------------------------+
| Location                              | Sentence                                                                                             |
+---------------------------------------+------------------------------------------------------------------------------------------------------+
| TUNIS                                 | Box 323  1002 TUNIS Belvdre Tel: (216) 71 10 20 34 Fax: (216) 71 33 26 95  PROJECT INFORMATION SHEET |
| Guinea                                | COUNTRY AND NAME OF PROJECT : Guinea: Tombo-Gbessia Road Improvement       Project  2.               |
| Conakry (Guinea                       | Box 581 Conakry (Guinea): Tel.                                                                       |
| Tombo-Gbessia Road                    | PROJECT DESCRIPTION  : The Project has the following components:  A - Works comprising:  a.1) the im |
| Kenien-Bonfi                          | PROJECT DESCRIPTION  : The Project has the following components:  A - Works comprising:  a.1) the im |
| Yimbaya                               | PROJECT DESCRIPTION  : The Project has the following components:  A - Works comprising:  a.1) the im |
| Guinea                                | B - Institutional support comprising: b.1) technical assistance to the National Road Investments Dep |
| UA                                    | OTHER FINANCING SOURCES * Agence franaise de dveloppement (AFD)   : UA 7.72 million  * Arab Bank for |
| Africa                                | OTHER FINANCING SOURCES * Agence franaise de dveloppement (AFD)   : UA 7.72 million  * Arab Bank for |
| UA                                    | OTHER FINANCING SOURCES * Agence franaise de dveloppement (AFD)   : UA 7.72 million  * Arab Bank for |
| Guinea                                | OTHER FINANCING SOURCES * Agence franaise de dveloppement (AFD)   : UA 7.72 million  * Arab Bank for |
| Tombo-Gbessia                         | International competitive bidding for road improvement works on the Tombo-Gbessia main road and cons |
| Kenien-Bonfi                          | International competitive bidding for road improvement works on the Tombo-Gbessia main road and cons |
| Yimbaya                               | International competitive bidding for road improvement works on the Tombo-Gbessia main road and cons |
| Africa                                |    iii   CURRENCY EQUIVALENTS / WEIGHTS AND MEASURES  Currency Equivalents (February 2005)  UA 1 = U |
| Guinea                                |    iii   CURRENCY EQUIVALENTS / WEIGHTS AND MEASURES  Currency Equivalents (February 2005)  UA 1 = U |
| United States                         |    iii   CURRENCY EQUIVALENTS / WEIGHTS AND MEASURES  Currency Equivalents (February 2005)  UA 1 = U |
| Tombo-Gbessia                         | PROJECT OBJECTIVE  2.1 a) Improve traffic fluidity and reduce transport costs and travel time on the |
| Conakry                               | PROJECT OBJECTIVE  2.1 a) Improve traffic fluidity and reduce transport costs and travel time on the |
| Madina                                | PROJECT OBJECTIVE  2.1 a) Improve traffic fluidity and reduce transport costs and travel time on the |
| Tombo-Gbessia                         | OUTCOMES  3.1 Tombo-Gbessia road completed, permanent structures constructed, feeder road constructe |
| Conakry                               | 3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
| Kenien-Bonfi                          | 3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
| Yimbaya                               | 3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
| Guinea                                | 3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
| Conakry                               | 3.2 New bus station constructed    3.1 Technical and operational capacity of the NRID and NDDPI stre |
| Tombo-Gbessia                         | ORIGIN AND HISTORY OF PROJECT  1.1 The Tombo-Gbessia road is a throughway that prolongs National Hig |
| Conakry Port                          | 1 (NH1) right up to Conakry Port.                                                                    |
| Conakry                               | It is the main connection between the Capital and the hinterland and is one of the major urban roads |
| Conakry                               | In a bid to improve traffic fluidity in Conakry and on Tombo-Gbessia road in particular, the Governm |
| Tombo-Gbessia                         | In a bid to improve traffic fluidity in Conakry and on Tombo-Gbessia road in particular, the Governm |
| Conakry                               | It stems from the recommendations of the Urban Development Master Plan for Conakry (UDM) prepared in |
| Tombo-Gbessia                         | Its specific objective is to: (i) improve traffic fluidity, cut costs and reduce travel time on the  |
| Conakry                               | Its specific objective is to: (i) improve traffic fluidity, cut costs and reduce travel time on the  |
| Tombo                                 | Brief Description of Project Achievements   To ensure attainment of the above-mentioned objectives,  |
| Gbessia                               | Brief Description of Project Achievements   To ensure attainment of the above-mentioned objectives,  |
| Kenien                                | Brief Description of Project Achievements   To ensure attainment of the above-mentioned objectives,  |
| Yimbaya                               | Brief Description of Project Achievements   To ensure attainment of the above-mentioned objectives,  |
| Tombo-Gbessia                         | 8 Conclusions and Recommendations   8.1 Conclusions   The Tombo-Gbessia road is part of the priority |
| Guinea                                | 8 Conclusions and Recommendations   8.1 Conclusions   The Tombo-Gbessia road is part of the priority |
| Conakrys                              | 8 Conclusions and Recommendations   8.1 Conclusions   The Tombo-Gbessia road is part of the priority |
| Guinea                                |  11 ORIGIN AND HISTORY OF PROJECT  1.1 Guinea has embarked on an economic recovery program to improv |
| Conakry                               | This policy was implemented in Conakry in 1989 through the development of the Urban Development Mast |
| Conakry                               | Given its central position, this road is a throughway that prolongs NH1 right through to Conakry por |
| Mali                                  | It is noteworthy that the NH1 drains two-thirds of the traffic from the hinterland to the capital, a |
| Tombo-Gbessia                         | The Tombo-Gbessia road is also part of the primary urban road network.                               |
| Yimbaya                               | The AFD also financed the study for the development of the Yimbaya bus station and the Kenien-Bonfi  |
| Kenien-Bonfi                          | The AFD also financed the study for the development of the Yimbaya bus station and the Kenien-Bonfi  |
| Guinea                                | Considering its socio-economic benefits, the project is in conformity with poverty reduction strateg |
| Guinea                                | TRANSPORT SECTOR   2.1 Transport System   2.1.1 Given its surface area of about 246.000 km2 and a se |
| Mali                                  | Opening up access to neighboring countries, especially landlocked Mali, is one of the priorities of  |
| Conakry Port                          | Opening up access to neighboring countries, especially landlocked Mali, is one of the priorities of  |
| Conakry Port                          | Creating such access has to start with the improvement of national and transnational highways as wel |
| Tombo-Gbessia                         | Creating such access has to start with the improvement of national and transnational highways as wel |
| Conakry                               | In a bid to address these constraints, the Government defined certain measures in its National Trans |
|