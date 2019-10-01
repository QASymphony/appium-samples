This repo is our experiement with [Appium](http://appium.io/) and the feasibility to integrate it with [Universal Agent](https://support.qasymphony.com/hc/en-us/articles/360004704172-Universal-Agent-Overview). Please read the below statement carefully if you decided to integrate your test frammework built on top of Appium with Universal Agent.

We, by any mean, are not Appium experts and our knowledge of it is very limited. Despite that fact, we still want to explore the ability to integrate Appium with Universal Agent and share our journey with those who are considering integrating their Mobile test, which is built on top of Appium framework, with Universal Agent. 

This sample project and instructions to integrate it with Universal Agent are provided "AS IS". We reserve the right to do NOT provide any support and/or bug fixes to the sample code unless you meet ALL of the below conditions:

- You are a qTest Elite user
- You must have some experience with mobile test development using Appium. We are not providing support to those who does not have knowledge of Appium, or to those who never developed test automation with Appium
- You are using Appium whose version is the same with the version we use in the sample: 1.15.0, which is the latest version at the time of this writing
- The sample is developed and tested on MacOS Mojave 10.14. We will not provide support if your test framework run on a platform other than MacOS or on different MacOS version
- The sample test project uses python, which is originally cloned from [here](https://github.com/appium/appium). You should know Appium can be integrated with a wide range of test frameworks which are built using different programming languages. Again, our knowledge of test frameworks as well programming languages are limited, so we will NOT provide support if your issue is related to the framework that we do not have knowledge of and experience with. You're supposed to be the expert on the test framework you are using
- You Mac machine must have [Python 3.7.4+](https://www.python.org/downloads/release/python-374/) installed

If you meet all of above conditions and have issues with your integration, feel free to submit an issue to THIS github repo.

# Pre-requisites #

[Activate Automation Integration in qTest Manager](https://support.qasymphony.com/hc/en-us/articles/115002947946-Activate-Automation-Integration)

Installed below components in order for the sample to work

- [qTest Automation Host 2.3.2 or later](https://support.qasymphony.com/hc/en-us/articles/115005243923-Download-qTest-Automation-Host)
- Xcode 11.0 or later must be installed in the same machine with Automation Host
- [Appium 1.15.0](https://github.com/appium/appium/releases/tag/v1.15.0) must be installed in the same machine with Automation Host
- iOS Platform version: 13.0. Device name: iPhone 11 Pro Max. You can view and change these capabilties in the [helpers.py](https://github.com/QASymphony/appium-samples/blob/master/python/test/helpers.py) (look for the IOS_BASE_CAPS) to fit your test environment
- [Python 3.7.4](https://www.python.org/downloads/release/python-374/) needs to be installed in the same machine with Automation Host. It is highly recommended to install [pyenv](https://github.com/pyenv/pyenv) and use it to configure Python 3.7 to be the default Python program in your Mac machine
- [pytest](https://docs.pytest.org/en/latest/getting-started.html) framework is used to run our sample test and needs to be installed on the same machine with Automation Host
- [pytest-csv](https://pypi.org/project/pytest-csv/) needs to be installed on the same machine with Automation Host. Note: this module is required to generate test report under CSV format
- You test machine must have [git](https://git-scm.com/downloads) installed

# Clone Sample project and Install dependencies #

Clone sample project from this github repo to your loccal machine, e.g. at /usr/local/var/appium-samples

Open Terminal, navigate to your appium-samples directory with below command:

```
$ cd /usr/local/var/appium-samples/python
```

Still in the Terminal, execute below command to install dependencies:

```
/usr/local/var/appium-samples/python $ pip install -r requirements.txt
```

# Create Appium Universal Agent #

Access to Automation Host UI. Click on **+Add** button. From the New Agent dialog, enter the followings:

## General Information ##

- Agent Name: **Appium Universal Agent**
- qTest Manager Project: \<select a qTest Manager project that you are a member of\>
- Agent Type: **Universal Agent**

## Pre-Execute Script ## 

Enter the script below to Pre-Execute Script field

```bash
#!/bin/bash
if [ ! -d "/usr/local/var/appium-samples" ]
then
 cd "/usr/local/var"
 git clone https://github.com/QASymphony/appium-samples.git
else
 cd /usr/local/var/appium-samples
 git pull --all
fi
```

## Execute Command ## 

- Executor: **node**
- Working Directory: **/usr/local/var/appium-samples/python**
- Execute Command: enter the following to the Execute Command field. **Notes:** make sure you enter the actual value for the variable **pytestExecutablePath** following the comments in the scripts

```javascript

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// absolute path to pytest executable
// you can find the actual path by executing this command in Terminal: $ which pytest
// then replacing the value with the actual path returned from that command
const pytestExecutablePath = '<enter path to your pytest executable here>';

let workingDir = process.env.WORKING_DIR || '';
workingDir = workingDir.replace(/\\/g, "/");
console.log('--- Working directory: ', workingDir);

if (!fs.existsSync(workingDir)) {
  console.log("No working directory found.");
  return;
}

// this variable holds the path to test result directory
let resultsDir = path.resolve(`${workingDir}`, 'results');
// remove the directory if it exists, and re-create it 
// just to make sure we always have latest results from this execution
if (fs.existsSync(resultsDir)) {
  execSync(`rm -rf "${resultsDir}"`);
}
fs.mkdirSync(resultsDir);

// $TESTCASES_AC is a variable that holds automation content of scheduled test runs (if any) separated by a comma ','. 
// The values of $TESTCASES_AC is fetched by Universal Agent everytime Universal Agent executes.
let testcases_AC = $TESTCASES_AC;
// print automation content(s) to the execution log
console.log('*** testcases_AC: ' + testcases_AC);

// if testcases_AC has value, replace ',' with ' ' in its value then assign the result to scheduledTestcases var
// otherwise, assign empty string to scheduledTestcases
let scheduledTestcases = testcases_AC ? testcases_AC.replace(',', ' '): '';

try {
  var command = `${pytestExecutablePath} --csv ${resultsDir}/result.csv`;
  // if scheduledTestcases has value, the value will be used to specifiy which tests to be executed by pytest
  if (scheduledTestcases != '') {
    console.log(`*** scheduledTestcases: ${scheduledTestcases}`);
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

At this point, the Universal Agent does the followings to kick off our test:

- Run Pre-Execute Script: this script checks for the existence of the /usr/local/var/appium-samples directory, which contains the sample code. If the directory does not exist, the script runs a git command to clone the sample code from this github repo into that diretory. Meanwhile, if the directory already exists, the script pulls the latest code from this repo to that directory
- Run Execute Command: the execute command is the nodejs code that execute our appium sample tests

Screenshot below shows how the tests get executed: on the left is the Universal Agent printing its execution logs in its Console Log, on the right is the test application running on the Simulator naming *iPhone 11 Pro Max*. **Important note: at this point please do not switch back and forth between applications on your Mac machine until the test completely finished its execution. From our experience, some tests will failed unexpectedly if the Simulator lost focus due to being deactivated, which is caused by switching to other applications on Mac machine**

![Test Running](/docs/agent-running.png)

## Reporting test result to qTest Manager ##

Up to this point, we have configured the nodejs code in the Appium Universal Agent's Execute Command to kick off the *pytest* program and specify that the test should generate result under CSV format via the use of **--csv** parameter, as shown below.

```
...
  var command = `${pytestExecutablePath} --csv ${resultsDir}/result.csv`;
  if (scheduledTestcases != '') {
    console.log(`scheduledTestcases: ${scheduledTestcases}`);
    command = `${pytestExecutablePath} ${scheduledTestcases} --csv ${resultsDir}/result.csv`;
  }
  console.log(`execcute command: ${command}`);
  execSync(command, { stdio: 'inherit' });
...
```

In order to submit the test result to qTest Manager, we need to do 2 extra steps:

- Implement a custom parser to parse the result under CSV format and upload it to qTest Launch
- Update Appium Universal Agent to use the newly-created custom parser to parse the CSV result and so allow the Universal Agent to submit the result to qTest Manager

For demonstration purpose, we implemented the custom parser and included it in this repo at [pytest-csv-parser.zip](https://github.com/QASymphony/appium-samples/blob/master/pytest-csv-parser.zip). If you want to learn more about how to implement a custom parser to parse your test results, follow this article: [Develop Custom Test Result Parser for Universal Agent](https://support.qasymphony.com/hc/en-us/articles/360004711012-Develop-Custom-Test-Result-Parser-for-Universal-Agent)

Next, follow the below steps to upload the parser to qTest Launch and use it in Universal Agent.

- Download the custom parser at [pytest-csv-parser.zip](https://github.com/QASymphony/appium-samples/blob/master/pytest-csv-parser.zip)
- Login to qTest Manager if you haven't done so, then access to qTest Launch from 9-box
- From qTest Launch, click on the gear icon on the top right. The Settings dialog will show
- In the Settings dialog, make sure Universal Agent tab is selected. Click Add button to add custom parser. 

Next, enter the followings to upload the custom parsers:

- Name: **Pytest CSV Parser**
- Version: **1.0**
- Zip pakage: click Browse and select the customer parser that you just downloaded

The Add Parser dialog will now look like below.
![Add Parser](/docs/add-parser.png "Add Parser")

Click **SAVE** to finish adding new parser

Now, go back to Automation Host UI. Click **Poll Now** button. This will allow Automation Host to load latest updates from qTest Launch, inccluding the new parsers.

Next, we will edit Appium Universal Agent to use the custom parser. You'll do that by select **Edit** from Appium Universal Agent, as shown below.

![Edit Agent](/docs/edit-agent.png "Edit Agent")

In the edit Appium Universal Agent dialog, enter the followings:

- Path to Results: select path to the .csv result file, in our example it is **/usr/local/var/appium-samples/python/results/result.csv**
- Result Parser: select the custom parser we just uploaded to qTest Launch **Pytest CSV Parser**

Your agent will now look like below.

![Edit Parser](/docs/edit-agent-add-parser.png "Edit Parser")

Click **Save** to finish editing the Appium Universal Agent.

Now, select **Run now** from the Appium Universal Agent, then click Execute button to execute the agent. You'll see the test is being kicked off with the Simulator running. 

When the test finished execution, you'll see there are logs in the Universal Agent's Console Log indicating the results are submitted to qTest Manager, as below.

![Execution Results Submitted](/docs/execution-results-sumitted.png)

You will also see the submitted results in qTest Manager > Test Execution tab, as below.

![Execution Results Submitted in Manager](/docs/execution-results-sumitted-in-manager.png)

## Schedule Test Execution for Specific Tests ##

Sometimes you do not need the whole tests get executed but some tests only. For instances, when there are failed tests due to bugs in your application, you go ahead fixing the bugs, build the app then run the tests that failed previously instead of all the tests.

With qTest Launch, you can schedule test execution for specific tests only. You do that by selecting the test cases or test runs you want to be executed by Universal Agent.

Follow steps below to schedule test execution for some selected tests in our sample project.

1. Login to qTest Manager and navigate to Test Execution module then locate the Test Suite created from previous test execution
2. On the right panel select test runs you want to execute
3. Select MORE and then SCHEDULE. As below.

![Scchedule Test 1](/docs/schedule-test-1.png)

You will be naviated to qTest Launch where you'll schedule test execution for the selected test runs.
On the **Schedule Test Run: Select Cases** screen, enter the name of the schedule, e.g. Re-run tests, then click NEXT.

![Sehedule Test 2](/docs/schedule-test-2.png)

On the **Select Hosts and Agents** screen, search for Appium Universal Agent, select it and click on **RUN NOW** button.

![Schedule Test 3](/docs/schedule-test-3.png)

On **Test Result Summary** screen, click **DONE** to finish your test scheduling.

Now get back to the Automation Host UI. Click on **Poll Now** button to force the Automation Host to poll to qTest Launch to get updates. This time it will receive the job we just scheduled in qTest Launch and execute it. Wait for a while for the job execution to be finished then go to qTest Manager > Test Execution module to check for the result. This time you will see the 3 test runs having new test logs submitted to it (the LOGS column shows 2 as compared to 1 from other test runs, as shown below (if you would like, you can click on the ID of the test run ro view its details, including Execution History). 

![Schedule Test 4](/docs/schedule-test-4.png)

That's it. You have successfully integrate Appium tests with Universal Agent.


