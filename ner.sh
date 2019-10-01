#!/usr/bin/env bash
java -server -Xms256m -Xmx1024m -XX:MaxMetaspaceSize=256m -XX:+UseConcMarkSweepGC -XX:ReservedCodeCacheSize=128m -Djava.awt.headless=true -XX:+CMSParallelRemarkEnabled -XX:+ScavengeBeforeFullGC -XX:+CMSScavengeBeforeRemark -Xverify:none -noverify -cp stanford-ner-3.8.0.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 9094


java -server -Xms256m -Xmx2048m -XX:MaxMetaspaceSize=256m -Djava.awt.headless=true -XX:+CMSParallelRemarkEnabled -XX:+ScavengeBeforeFullGC -XX:+CMSScavengeBeforeRemark -Xverify:none -noverify -cp  stanford-ner-3.9.2.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 9094