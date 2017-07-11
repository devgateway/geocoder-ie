__author__ = 'sebas'
# -*- coding: utf-8 -*-
import io
import nltk
from nltk.tokenize import TreebankWordTokenizer
from pdf.pdf_reader import Pdfreader
from util.file_util import create_folder

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = TreebankWordTokenizer()

samples = [
    '../../corpora/projects/AFDB/guinea/46002-P-GN-DB0-005/Guinea_-_Tombo-Gbessia_Road_Improvement_Project_-_Appraisal_Report.pdf',
    '../../corpora/projects/AFDB/zimbabwe/46002-P-ZW-DB0-005/Zimbabwe_-_National_Transport_Sector_Master_Plan_Study_-_Appraisal_Report.pdf',
    '../../corpora/projects/AFDB/zimbabwe/46002-P-ZW-E00-003/Zimbabwe_-_Urgent_Water_Supply_and_Sanitation_Rehabilitation_Project_-_Phase_2_-_Appraisal_Report.pdf'
]


for file in samples:
    reader = Pdfreader(file)
    reader.read()
    project= file.split('/')[-2]
    name = 0
    create_folder('../../corpora/sentences', project)
    for p in reader.get_pages_text():
        sentences = sentence_tokenizer.tokenize(p)
        for sentence in sentences:
            with io.open('../../corpora/sentences/%s/%s.txt' % (project,name), 'w', encoding='utf-8') as txt:
                txt.write(sentence.replace('\n',''))
                name += 1


