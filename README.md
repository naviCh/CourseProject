# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

## Installation
From project root directory, run: 
```bash
pip install -r requirements.txt
```

## Setup 
### Secrets
Go to https://www.reddit.com/prefs/apps/ to get a `client_id`,`client_secret`, and `user_agent`.
The file `secrets` should contain key-value pairs of the format `key=value` and should be placed in the project root directory. The secrets needed are:

* `client_id` - Client ID for personal script use 
* `client_secret` - Secret
* `user_agent` - Reddit Username