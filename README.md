### Install

```
pip install --upgrade requirements.txt
```

### Configure
Provide authentication credentials to your application code by setting the environment variable GOOGLE_APPLICATION_CREDENTIALS. Replace [PATH] with the file path of the JSON file that contains your service account key, and [FILE_NAME] with the filename. This variable only applies to your current shell session, so if you open a new session, set the variable again.
```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```
