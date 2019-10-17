## Vision
A prototype Python application for testing Google Vision's image processing.

### Install
Start virtualenv and install requirements
```
virtualenv vision_env -p python3
source vision_env/bin/activate
cd vision
pip install -r requirements.txt
```
Put your images into the directory /images and start the application with
```bash
python start.py
```

NOTE: The folder already contains a few images sourced from Google Open Images. 
If you need more free images you can find quite a few more there.

Detailed information about the capabilities of Google Vision and how to start using them can be found [here](https://cloud.google.com/vision/docs/how-to).

### Configure
Before you can access the service you need to enable the Vision API for your Google Project. For more information about 
how to do this, read [Before You Begin](https://cloud.google.com/vision/docs/before-you-begin).
 
When all is set, provide authentication credentials to your application code by setting the environment variable 
GOOGLE_APPLICATION_CREDENTIALS. Replace [PATH] with the file path of the JSON file that contains your service account key, 
and [FILE_NAME] with the filename. This variable only applies to your current shell session, so if you open a new session, 
set the variable again.
```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

