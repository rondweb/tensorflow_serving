# Setting up your machine
## This is a one-time setup activity.

To start our local server we need a TensorFlow Serving instance on our local machine. Instead of downloading and installing all the necessary libraries, we shall use the recommended way of using Docker.

You can read more details about it in the Guide here.

We won’t be following all the steps mentioned in the Guide, as some of the things are specific for TF 1.0 and some things are specific to reusing already available models.

Once you download Docker on your system from here, go ahead and finish the installation steps. You would need to restart your system so save all your work.

Once the installation is finished successfully, go to Command Prompt (Mac and Linux users, kindly use appropriate tools) and type

# Installing docker image

```sh
docker pull tensorflow/serving
```


That’s it! Let’s now proceed to deploy our model.

#Deploying your Keras Model on localhost
What if I told you that deploying the model is just one line of command script.

All you need is the absolute path to your ‘linear_model’ folder. Do not forget to use the absolute path as this would cause errors that you would need to spend time and break your head to solve.

My ‘linear_model’ was saved inside ‘D:/my_own_models/’. So my command looked like:

```sh
docker run -p 8038:8501 --mount type=bind,source=I:\PROJECTS\PAPERS\tensorflow_serving\linear_model,target=/models/linear_model -e MODEL_NAME=linear_model -t tensorflow/serving
```

This is all a single line. For your subsequent models, you need to just change your ‘source’ path. Changing your ‘target’ and MODEL_NAME is optional, but, of course, necessary based on the context.

Now let us try to understand what the above command script indicates. The generic form of this script is

```sh
docker run -p {LOCAL_PORT}:8501 — mount type=bind,source={ABSOLUTE_PATH},target=/models/{MODEL_NAME} -e MODEL_NAME={MODEL_NAME} -t tensorflow/serving
```
{LOCAL_PORT}: This is the local port of your machine, so make sure you do not have anything else running there. We are mapping it to the 8501 port exposed for REST API calls by TensorFlow Serving

{ABSOLUTE_PATH}: This is the absolute path for your model. This tells the TensorFlow Serving where your model is located at (obviously).

{MODEL_NAME}: This is the service end-point for your REST API call with the prefix ‘/models/’. Do not change the ‘/models/’ prefix in the target variable and only change the {MODEL_NAME} part based on your need

Once you see the below message in your command window, your model has been hosted successfully. You can also see a container running successfully in your Docker dashboard.

```sh
[evhttp_server.cc : 238] NET_LOG: Entering the event loop …
```

Testing our Model
I used Postman for testing my queries, but you can use any form of API calls.

[Note: You won’t be able to make direct calls from browser or any other host to your REST API since CORS is not enabled by TensorFlow Serving. However, there are ways to achieve a call from the browser to your model that I would cover in a separate post.]

You need a POST query to test our model. Our request URL looks like:

http://localhost:8509/v1/models/linear_model:predict

Again, the generic form is:
http://localhost:{LOCAL_PORT}}/v1/models/{MODEL_NAME}:predict

Add ‘Content-Type’ as ‘application/json’ in your header and your body as:

Ensure that your JSON key is ‘instances’ and your values are inside an array. Since our input is [0], we write it as [[0]].

Remember, that we created a model to predict y = 2x + 1 which means for input value 0, our prediction should have value 1 (or close to it).

Let’s send our query. The response looks like:
```sh
{
     "predictions": [[
          0.999998748
     ]]
}
```

Well, that looks pretty much like 1 to me. Play around with your model by making POST queries.

Conclusion
We were able to create a model from scratch and deploy it on our local server. This is a very good way to see if your model would work the same way in the real world as it does on your IDE.

As I previously mentioned, however, you won’t be able to make calls to this model apart from Postman (or similar tools). How to overcome that? I shall cover that in a separate post as this is already becoming too long.

If you have reached here, thanks for reading. If you have any queries, suggestions or comments, please feel free to comment on this post. This is my first blog on Machine Learning and I would gladly appreciate any and all feedback.

Reference: https://towardsdatascience.com/serving-keras-models-locally-using-tensorflow-serving-tf-2-x-8bb8474c304e
