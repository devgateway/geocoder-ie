#!/usr/bin/env bash
java -server -Xms256m -Xmx2048m -XX:MaxMetaspaceSize=256m -Djava.awt.headless=true -XX:+CMSParallelRemarkEnabled -XX:+ScavengeBeforeFullGC -XX:+CMSScavengeBeforeRemark -Xverify:none -noverify -cp  stanford-ner-3.9.2.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/eunews.fr.crf.gz -port 9094
