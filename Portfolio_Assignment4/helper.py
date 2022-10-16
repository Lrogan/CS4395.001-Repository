"""
Usage:
    python allennlp_srl.py \
    https://s3-us-west-2.amazonaws.com/allennlp/models/srl-model-2017.09.05.tar.gz \
    examples.json
Note:
    each line in examples.json is one sentence, such as:
        Which NFL team represented the AFC at Super Bowl 50?
        Where did Super Bowl 50 take place?
        Which NFL team won Super Bowl 50?
        What color was used to emphasize the 50th anniversary of the Super Bowl?
        What was the theme of Super Bowl 50?
        What day was the game played on?
        What is the AFC short for?
        What was the theme of Super Bowl 50?
        What does AFC stand for?
        What day was the Super Bowl played on?
        Who won Super Bowl 50?
        What venue did Super Bowl 50 take place in?
"""

from allennlp.predictors.predictor import Predictor


if __name__ == '__main__':

  text = 'There is no way I can beat the barbershop and obtain obscene bullion.'

  predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz")
  results = predictor.predict(
    sentence=text
  )

  results.keys()

  for i in range(len(results['verbs'])):
    print(results['verbs'][i]['description'] + "\n")