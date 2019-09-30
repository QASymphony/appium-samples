Please read the below statement carefully if you decided to integrate [Appium](http://appium.io/) test with [Universal Agent](https://support.qasymphony.com/hc/en-us/articles/360004704172-Universal-Agent-Overview).

We, by any mean, are not Appium experts and our knowledge of it is very limited. Despite that fact, we still want to experiement the ability to integrate Appium with Universal Agent and share our journey with those who are considering integrating their Mobile test, which is built on top of Appium framework, with Universal Agent. 

This sample project and instructions to integrate it with Universal Agent are provided "AS IS". We reserve the right to do NOT provide any support and/or bug fixes to the sample code unless you meet ALL of the below conditions:

- You are a qTest Elite user
- You must have some experience with mobile test development using Appium. We are not providing support to those who does not has knowledge of Appium, or to those who never develloped test automation with Appium
- You are using Appium whose version is the same with the version we use in the sample: 1.15.0
- The sample is developed and tested on MacOS. We will not provide support if your test framework run on a platform other than MacOS
- The sample test project uses python, which is originally cloned from [here](https://github.com/appium/appium). You should know Appium can be integrated with a wide varieties of test frameworks which are built on top of different programming languages. We are open to learning new things but our knowledge of test frameworks are limited, so we reserve a right to NOT provide support to your test framework, even it is built using Python. You're supposed to be the expert on the test framework you use
- You Mac machine must have [Python 3.7.4+](https://www.python.org/downloads/release/python-374/) installed

# Pre-requisites #

Below components must be installed and configured in order for the sample to work

- [Activate Automation Integration](https://support.qasymphony.com/hc/en-us/articles/115002947946-Activate-Automation-Integration)
- [Download and Install qTest Automation Host 2.3.2 or later](https://support.qasymphony.com/hc/en-us/articles/115005243923-Download-qTest-Automation-Host)
- [Appium 1.15.0](https://github.com/appium/appium/releases/tag/v1.15.0) needs to be installed in the same machine with Automation Host
- [Python 3.7.4](https://www.python.org/downloads/release/python-374/) needs to be installed in the same machine with Automation Host
- [pytest](https://docs.pytest.org/en/latest/getting-started.html) needs to be installed in the same machine with Automation Host
- [pytest-csv](https://pypi.org/project/pytest-csv/). needs to be installed in the same machine with Automation Host. Note: this module is required to generate test report under CSV format
- You test machine should have [git](https://git-scm.com/downloads) installed

# Clone Sample project and Setup environment #

Clone sample project from this github repo to your loccal machine, e.g. /usr/local/var/appium-samples
Open Terminal, navigate to your appium-samples directory using below command:

```
$ cd /usr/local/var/appium-samples/python
```

Still in the Terminal, execute below command to install requirements:

```
/usr/local/var/appium-samples/python $ pip install -r requirements.txt
```

# Create Appium Universal Agent #

Access to Automation Host UI. Click on **+Add** button. From the New Agent dialog, enter the followings:

## General Information ##

- Agent Name: **Appium Universal Agent**
- qTest Manager Project: [select a qTest Manager project that you are a member of]
- Agent Type: **Universal Agent**

## Pre-Execute Script ## 

Enter the script below to Pre-Execute Script field

```bash
#!/bin/bash
if [ ! -d "/usr/local/var/appium-samples" ]
then
 cd "/usr/local/var"
 git clone git@github.com:QASymphony/appium-samples.git
else
 cd /usr/local/var/appium-samples
 git pull --all
fi
```

## Execute Command ## 

- Executor: **node**
- Working Directory: **/usr/local/var/appium-samples/python**
- Execute Command: enter the following to the Execute Command field

```javascript

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// path to pytest executable 
// you must find the acctual path by execute this command in Terminal: which pytest 
// then replace the value with the actual path in your machine
const pytestExecutablePath = '<enter path to your pytest executable here>';

let workingDir = process.env.WORKING_DIR || '';
workingDir = workingDir.replace(/\\/g, "/");
console.log('--- Working directory: ', workingDir);

if (!fs.existsSync(workingDir)) {
  console.log("No working directory found.");
  return;
}

// results folder contains execution results to submit logs to qTest
// NOTE: by default, the result fill be located at ${working directory}/test-results
let resultsDir = path.resolve(`${workingDir}`, 'results');
// create test results folder. If it already exists, deletes it and re-create it again.
if (fs.existsSync(resultsDir)) {
  execSync(`rm -rf "${resultsDir}"`);
}
fs.mkdirSync(resultsDir);

let scheduledTestcases = '';
// get automation content from magic variable TESTCASES_AC
let testcases_AC = $TESTCASES_AC;
// print automation content(s) to the execution log
console.log('*** testcases_AC: ' + testcases_AC);

testcases_AC = testcases_AC ? testcases_AC.split(',') : [];
if (testcases_AC && testcases_AC.length > 0) {
  let tcArray = [];
  for (let tc of testcases_AC) {
    tcArray.push(tc);
  }
  scheduledTestcases = tcArray.join(' ');
}

try {
  var command = `${pytestExecutablePath} --csv ${resultsDir}/result.csv`;
  if (scheduledTestcases != '') {
    console.log(`scheduledTestcases: ${scheduledTestcases}`);
    command = `${pytestExecutablePath} ${scheduledTestcases} --csv ${resultsDir}/result.csv`;
  }
  console.log(`execcute command: ${command}`);
  execSync(command, { stdio: 'inherit' });
} catch (err) {
  // pytest command exit code is 1 if some testcases failed
  console.log(`Test execution error: ${err}`);
  return 0;
}
```

Your Universal Agent will loook like below:
![Create New Agent](/docs/new-agent.png "Create New Agent")

Click **Save** to finish creating Universal Agent.
Next step is to kick off our sample test project with Universal Agent.

## Kick off test project with Universal Agent ## 

If Appium is not running, open Terminal and execute below command:

```
$ appium
```
The Terminal will now look like below
![Run Appium](/docs/appium.png "Run Appium")

Now, access to Automation Host UI. Locate the **Appium Universal Agent** in the Agent list. Click on action icon group and select **Run now**. As shown below.
![Run Agent](/docs/run-now.png "Run Agent")


From the opening Appium Universal Agent dialog, click on **Execute** button to execute the agent.
![Execute Agent](/docs/execute-agent.png "Execute Agent")


