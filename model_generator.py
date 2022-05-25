# https://towardsdatascience.com/serving-keras-models-locally-using-tensorflow-serving-tf-2-x-8bb8474c304e

# Helper libraries
import numpy as np
import os


try:
    import tensorflow as tf
    print(tf.__version__)
except:
    print("tensorflow is not installed!")    

#creating a dataset
X = np.arange(-10.0, 10.0, 1e-2)
np.random.shuffle(X)
y = 2 * X + 1

train_end = int(0.6 * len(X))
test_start = int(0.8 * len(X))

X_train, y_train = X[:train_end], y[:train_end]
X_test, y_test = X[test_start:], y[test_start:]
X_val, y_val = X[train_end:test_start], y[train_end:test_start] 

# Then we build our model. Since it is a simple linear relationship, a single neuron is enough.

tf.keras.backend.clear_session()
linear_model = tf.keras.models.Sequential([
                                        tf.keras.layers.Dense(units=1, input_shape=[1], name='Single')
                                        ])
linear_model.compile(optimizer=tf.keras.optimizers.SGD(), loss=tf.keras.losses.mean_squared_error)
linear_model.summary()

# We now train our model for 20 epochs. After 20 epochs, our model’s losses were around 2e-12 for training as well as validation. Then, we evaluate our model on the test data. Our test loss came out to be around 2e-12. You can try predicting some values to verify the results like I did here. The output I received is 15.866.

linear_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20)
print(linear_model.evaluate(X_test, y_test, verbose=0))
print(round(linear_model.predict([7.443]).tolist()[0][0], 4))    # expected: 15.886

#Everything looks great.Let’s now save and download our model in the SavedModel format.
# From this step onwards, the process would be independent of the type of input and output data used. It could be numeric arrays, texts, images, audios or videos. In Colab, you should be able to see a folder named ‘linear_model’ created in your directory. The ‘export_path’ variable here indicates that our model is named ‘linear_model’ and this is the first version of it. Having a version number is mandatory for deploying using TensorFlow Serving so ensure that you have your ‘export_path’ in the form of {MODEL}/{VERSION}, where VERSION is numeric without any alphabets or special characters.
# Now to download this model, we will zip this folder and then use ‘google.colab.files’ to download the zip file.

export_path = 'linear_model/1/'
tf.saved_model.save(linear_model, export_path)

# Once you extract this zip file on your local machine, you should be able to see a folder named ‘linear_model’, which contains a folder named ‘1’, which contains your variables and model architecture.

# installing tensorflow with docker
# https://www.tensorflow.org/tfx/serving/docker




