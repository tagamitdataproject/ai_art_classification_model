import itertools
import os
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
print("TF version:", tf.__version__)
print("Hub version:", hub.__version__)
print("NP version:", np.__version__ )
print("PLT version:", plt.__version__ )
print("GPU is", "available" if tf.config.list_physical_devices('GPU') else "NOT AVAILABLE")
