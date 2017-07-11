import os

from dg.geocoder.classification.trainer import Trainer
from dg.geocoder.data.loader import FileDataLoader

dir = os.path.dirname(__file__)

target = os.path.normpath(os.path.join(dir, '../categorized'))

loader = FileDataLoader(target)

trainer = Trainer(loader.build_data_frame())

trainer.kfold_train()

trainer.plot_stats()

classifier=trainer.get_classifier()

print(classifier.predict(['Project area covers two towns in Cordoba City and Municipality','Eating at London wa snice']))
