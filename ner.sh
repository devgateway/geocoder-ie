#!/usr/bin/env bash
java -server -Xms256m -Xmx1024m -XX:MaxMetaspaceSize=256m -XX:+UseConcMarkSweepGC -XX:ReservedCodeCacheSize=128m -Djava.awt.headless=true -XX:+CMSParallelRemarkEnabled -XX:+ScavengeBeforeFullGC -XX:+CMSScavengeBeforeRemark -Xverify:none -noverify -cp stanford-ner-4.0.0.jar  edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/french-wikiner-4class.crf.ser.gz -port 9094


