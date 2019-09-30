Please read the below statement carefully if you decided to integrate [Appium](http://appium.io/) test with [Universal Agent](https://support.qasymphony.com/hc/en-us/articles/360004704172-Universal-Agent-Overview).

We, by any mean, are not Appium experts and our knowledge of it is very limited. Despite that fact, we still want to experiement the ability to integrate Appium with Universal Agent and share our journey with those who are considering integrating their Mobile test, which is built on top of Appium framework, with Universal Agent. 

This sample project and instructions to integrate it with Universal Agent are provided "AS IS". We reserve the right to do NOT provide any support and/or bug fixes to the sample code unless you meet ALL of the below conditions:

- You are a qTest Elite user
- You must have some experience with mobile test development using Appium. We are not providing support to those who does not has knowledge of Appium, or to those who never develloped test automation with Appium
- You are using Appium whose version is the same with the version we use in the sample: 1.15.0
- The sample is developed and tested on MacOS. We will not provide support if your test framework run on a platform other than MacOS
- The sample test project uses python, which is originally cloned from [here](https://github.com/appium/appium). You should know Appium can be integrated with a wide varieties of test frameworks which are built on top of different programming languages. We are open to learning new things but our knowledge of test frameworks are limited, so we reserve a right to NOT provide support to your test framework, even it is built using Python. You're supposed to be the expert on the test framework you use
- You Mac machine must have Python 3.7.x installed

# Pre-requisites #

Below components must be installed and configured in order for the sample to work

- [Activate Automation Integration](https://support.qasymphony.com/hc/en-us/articles/115002947946-Activate-Automation-Integration)
- [Download and Install qTest Automation Host 2.3.2 or later](https://support.qasymphony.com/hc/en-us/articles/115005243923-Download-qTest-Automation-Host)
- [Appium 1.15.0](https://github.com/appium/appium/releases/tag/v1.15.0)
- [Python 3.7.4](https://www.python.org/downloads/release/python-374/)
- [pytest](https://docs.pytest.org/en/latest/getting-started.html)
- [pytest-csv](https://pypi.org/project/pytest-csv/). Note: this is required to generate test report under CSV format
- You test machine should have [git](https://git-scm.com/downloads) install

# Create Appium Universal Agent  #

