import os, itertools
import numpy as np
from config import args
from random import randint
import matplotlib.pyplot as plt


def draw_accloss(history):
  plt.plot(history.history['accuracy'])
  plt.plot(history.history['val_accuracy'])
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model acc & loss')
  plt.xlabel('epoch')
  plt.ylabel('acc & val')
  plt.legend(['acc', 'val_acc', 'loss', 'val_loss'], loc='upper left')
  plt.savefig(os.path.join(args.data_dir, args.name, f'{args.model}.best.acc&loss.png'))
  plt.show()


def draw_confusion_matrix(cm):
  labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
  title='Confusion matrix'
  plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
  plt.title(title)
  plt.colorbar()
  tick_marks = np.arange(len(labels))
  plt.xticks(tick_marks, labels, rotation=45)
  plt.yticks(tick_marks, labels)
  fmt = '.2f'
  thresh = cm.max() / 2.
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, format(cm[i, j], fmt),
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")

  plt.ylabel('True label')
  plt.xlabel('Predicted label')
  plt.tight_layout()
  plt.savefig(os.path.join(args.data_dir, args.name, f'{args.model}.confusion_map.png'))
  plt.show()

def draw_pred_sample(xtest, ytest, truey, predy, yh):
  labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
  sample = [randint(0, len(ytest)) for _ in range(10)]
  label_sample = [truey[i] for i in sample]
  pred_sample = [predy[i] for i in sample]
  prob_sample =  [max(yh[i]) for i in sample]
  image_sample = np.empty((0, 48, 48, 1))

  for i in sample:
    image_sample = np.append(image_sample, np.expand_dims(xtest[i], axis=0), axis=0)

  image_sample = np.squeeze(image_sample, axis=3)

  plt.figure(figsize=(8,4))
  for i in range(10):
    plt.subplot(2, 5, i+1)
    plt.grid(False)
    plt.imshow(image_sample[i], cmap='gray')
    p = round(prob_sample[i] * 100)
    pred = labels[np.argmax(pred_sample[i])]
    answer = labels[label_sample[i]]
    label = f'predict: {pred}\n prob: {p}%\nanswer: {answer}'
    color = 'blue' if answer == pred else 'red'
    plt.xlabel(label, color=color)
  plt.savefig(os.path.join(args.data_dir, args.name, f'{args.model}.pred_sample.png'))
  plt.show()