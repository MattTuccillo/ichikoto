# Ichikoto 一事「いちこと」

---

## About

"Ichikoto" is an open-source Django application that sends the user a random Japanese word, its definition and a context sentence once per day through email. It also stores these words to prevent repeats. Sometimes it's hard to maintain learning habits but at least with ichikoto you take as much of the work out of the equation as possible. You just set it up and then check your email once a day.

---

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Obtaining an API Key from OpenAI](#obtaining-an-api-key-from-openai)
    - [Steps to Obtain an OpenAI API Key](#step-to-obtain-an-openai-api-key)
    - [Usage Costs](#usage-costs)
    - [Models](#models)
  - [Mailjet Setup](#mailjet-setup)
    - [Steps to Obtain a Mailjet API Key](#steps-to-obtain-a-mailjet-api-key)
  - [Email Whitelist Setup](#email-whitelist-setup)
    - [Gmail](#gmail)
  - [Installation](#installation)
  - [Using the App](#using-the-app)
    - [Monitoring the App](#monitoring-the-app)
- [Contribution Guidelines](#contribution-guidelines)
  - [Pull Requests](#pull-requests)
  - [Opening an Issue](#opening-an-issue)
  - [Logging](#logging)
  - [Testing](#testing)
    - [Writing Tests](#writing-tests)
    - [Running Tests](#running-tests)
    - [Considerations](#considerations)
- [Frequently Asked Questions (FAQs)](#frequently-asked-questions-faqs)
  - [What does "Ichikoto" mean?](#what-does-ichikoto-mean)
  - [What is lockfile.lock?](#what-is-lockfilelock)
  - [Why Django?](#why-django)
  - [Why only Japanese?](#why-only-japanese)
  - [Why threading over celery?](#why-threading-over-celery)
  - [Why manual mode tests for OpenAI API calls?](#why-manual-mode-tests-for-openai-api-calls)
  - [Why aren't the email formats consistent?](#why-arent-the-email-formats-consistent)
  - [Why won't my server start?](#why-wont-my-server-start)
  - [How do I run the tests?](#how-do-i-run-the-tests)
  - [How do I contribute?](#how-do-i-contribute)
  - [How do I get a new OpenAI API key?](#how-do-i-get-a-new-openai-api-key)
- [Future Plans](#future-plans)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Getting Started

### Prerequisites

Before you begin, make sure you have:

- Python 3.10
- Django 4.2.7
- A virtual environment tool like venv or virtualenv (recommended)
- Docker (optional)

### Obtaining an API Key from OpenAI

- To use the ChatGPT functionalities in this project, you will need an API key from OpenAI
- This key enables the application to communicate with OpenAI's services to generate responses
- Follow the steps below to obtain and configure your OpenAI API key

#### Steps to Obtain an OpenAI API Key

##### 1. Sign Up for an OpenAI Account

- Visit [OpenAI's website](https://openai.com/).
- If you don't already have an account, sign up by clicking on the **Sign Up** button and following the registration process.

##### 2. Access the API Dashboard

- Once logged in, you'll be asked to decide between **ChatGPT** and **API**, choose **API**.

##### 3. Generate an API Key

- Look for and press the **API Keys** option in the vertical navbar on the left side of the screen.
- Press the **Create new secret key** button to create a new API key for your application.
  - Name it something that is easy to associate with the application (e.g. ichikoto)

##### 4. Copy/Save Your API Key

- Once the key is generated, make sure to copy and save it securely you will need it during setup. This is important as you will likely be unable to view the key again after leaving the page.

#### Usage Costs

Currently, the OpenAI API is not free. You will be billed for credits with each call. However, it is worth mentioning that the price per API call is very low, almost negligible even. Below is some information to help you navigate through meeting this requirement.

- **Trial Credits**: OpenAI Typically offers free trial credits upon signing up. This should allow you to use the application for free, at least at first, if you did not have an OpenAI account prior.
- **No Credits**: If you already had an account, did not receive these credits, or have already exhausted them, then you will be required to purchase some credits.
- **Estimated Costs**: The amount of credits charged per API call in my personal testing has been extremely negligible, think less than \$0.01 USD. Coupled with the fact that the application is only intended to make a single call each day, this application could easily run year-round for less than \$5 USD.

#### Models

There are many different models available for the OpenAI API to utilize. However, the current default model for this application is **_gpt-3.5-turbo_** which is also the only one that has been tested and verified to work as of this time. If you intend to use any other models, please be aware of the potential for issues to occur.

### Mailjet Setup

This project uses Mailjet for sending emails. To utilize Mailjet, you'll need to create a Mailjet account and obtain your API credentials. Mailjet was chosen specifically because it is easy to create an account and should not incur costs for our specific usage in this project.

#### Steps to Obtain a Mailjet API Key

##### 1. Sign Up for a Mailjet Account

- Visit the [Mailjet website](https://www.mailjet.com/) and sign up for an account.
- Follow the on-screen instructions to complete the account setup, which includes verifying your email address.
- The email address you use to create the account will be the default sender address initially.

##### 2. Obtain Your API Credentials

- Once your account is set up, log in to the Mailjet dashboard.
- Press on your name in the top-right corner of the screen and navigate to **Account Settings** through the dropdown menu
- From here navigate to **API Key Management** in the **REST API** section of **Account Settings**
- Here, you will find your **API Key** (Public Key) and **Secret Key** (Private Key). These are used to authenticate email requests from the application.
- If you do not see a **Secret Key** then you will need to press the button to generate one.

##### 3. Copy/Save Your API And Secret Keys

- Once you can see both keys, make sure to copy and save them securely as you will need them during setup.

##### 4. Add/Verify Sender Email Address

If you used your desired sender email address to sign up for Mailjet then you can skip this step. Otherwise, continute to add and verify a new email address to send from.

- Press on your name in the top-right corner of the screen and navigate to **Account Settings** through the dropdown menu
- From here navigate to **Add a Sender Domain or Address** in the **Senders & Domains** section of **Account Settings**
- Here, you will find your sender email addresses. The email you signed up with should be listed by default.
- If you want to add a new email address to the list press **Add a sender address** and enter a label, the email to add, and set it as "Both / I don't know".
- The email will then be added to the list and you will need to check the inbox of that email address to verify it before Mailjet will validate it.

### Email Whitelist Setup

To ensure that the automated emails sent by "Ichikoto" are not marked as spam, especially given they contain Japanese characters, it's recommended to add the sender's email to your email provider's whitelist. Below are the steps for popular email providers:

#### Gmail

1. Go to your Gmail inbox.
2. Press the gear icon in the top right corner and select **See all settings**.
3. Navigate to the **Filters and Blocked Addresses** tab.
4. Click **Create a new filter**.
5. Enter the sender's email address in the **From** field.
6. Click **Create filter**, select **Never send it to Spam**, and then click **Create filter** again.

_More email providers will be added over time. Contributions to this section are welcome!_

### Installation

To install and run "Ichikoto" on your local machine, follow these steps:

1. **Clone the Repository**:

   ```
   git clone https://github.com/MattTuccillo/ichikoto.git
   cd ichikoto
   ```

2. **Set Up a Virtual Environment** (Recommended):

   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       .\venv\Scripts\activate
       ```
     - On Unix or MacOS:
       ```
       source venv/bin/activate
       ```

3. **Run Setup Script**:

   - This script creates a `.env` file and installs required packages.

   ```
   python setup.py
   ```

4. **Configure the `.env` File**:

   - Add all of your keys and email settings

     ```
     OPENAI_API_KEY = "YourAPIKeyHere"
     OPENAI_API_MODEL = "gpt-3.5-turbo"

     MAILJET_API_KEY = "YourMailjetAPIKeyHere"
     MAILJET_SECRET_KEY = "YourMailjetSecretKeyHere"
     MAILJET_SENDER_EMAIL = "YourMailjetSenderEmailHere"
     RECIPIENT_EMAIL = "YourEmailHere"
     ```

   - Set what time you want to receive the email each day (24-hour time)
     - if invalid hour is entered, it reverts to 12
     - if invalid minutes are entered, it reverts to 0
     - if you enter a time that is within **60 seconds** of the current time, it will add a 24-hour buffer before executing
     ```
     # 0-11 ==> am
     # 12-23 ==> pm
     EMAIL_SCHEDULER_HOUR = 12
     EMAIL_SCHEDULER_MINUTES = 0
     ```

5. **Start the Server**:
   Before starting the server, ensure that your `.env` file is properly configured with all the necessary environment variables.

   **To start the server manually:**

   - Activate your virtual environment (if you're using one):
     ```
     source venv/bin/activate  # On Unix or MacOS
     venv\Scripts\activate     # On Windows
     ```
   - Run the Django server:
     ```
     python manage.py runserver
     ```

   **To start the server using Docker:**

   - Ensure Docker is installed and running

   - Build the Docker image (if it's your first time or if there are updates):
     ```
     docker-compose build
     ```
   - Run the server:
     ```
     docker-compose up
     ```
   - Run the server in detached mode:
     ```
     docker-compose up -d
     ```

### Using the App

If everything worked correctly and the server was able to start up then you're all set! You can leave it running and it will sleep until the timer signals that it's time to execute each day. Each time it executes your word list will expand.

#### Monitoring the App

- Locate the _logfile.log_ file in the root directory of the project
- Watch as the logger continues to build upon the file while the server is running
- Both failures and successes are logged so it is easy to follow what is happening at each step.

---

## Contribution Guidelines

There is an intended direction for this project and you can read more about it in the [Future Plans](#future-plans) section. Issues will be posted describing bugs that need to be fixed or potential feature plans so that it is easy to find a place to start contributing. If you have an unlisted idea for a feature or discover a bug you'd like to document, feel free to open an issue and I will review it at my earliest convenience. I reserve the right to deny your contribution if I feel it does not align with the current direction of the project, however, even still, I'd be delighted to see it implemented in your own forked repo. That being said, if you are interested in contributing in any form, below are some guidelines to help you get started.

### Pull Requests

- Ensure your feature branch is up to date with the _master_ branch
- Ensure that all tests pass
  - `python manage.py test`
- Provide a concise and appropriate title for the pull request
- In the description field:
  - Provide a list highlighting the major changes made to the code
  - List any files that have been added with rationale
  - Provide rationale for changes to any pre-existing code

### Opening an Issue

- Provide a concise and appropriate title for the issue
- Set appropriate labels for the issue
- In the description field:
  - Provide a summary of the issue
  - Provide instructions to reproduce the issue (if applicable)
  - Provide generalized criteria for the completion of the issue. (What does completion look like?)
  - Provide any helpful information about solving the issue (optional)
- Check an existing issue to get a better idea of the expected content and formatting. [Issue #1](https://github.com/MattTuccillo/ichikoto/issues/1)

### Logging

- **Every file that contains code that will be executed should contain logging in some form. Strong rationale must be given if it does not.**
- Use common sense and add logging in such a way that the logfile can be used to follow the general flow of the code's execution.
- Don't be afraid of going overboard, it is easier to pick logging lines to remove than it is to ask you to add more.

### Testing

Testing is a critical part of development and should be included whenever possible. Proper testing allows us to build confidence in our code before it is executed meaning we are less likely to encounter errors when running the server or implementing new features that utilize old methods. As such, it is imperative that tests are built with purpose and that they provide some degree of confidence through their successful execution. Repeated or irrelevant tests will not be accepted.

#### Writing Tests

- **Naming Conventions**: Follow the already established naming conventions in the existing test files. Test method names should be descriptive and reflect what they are testing. For example, `test_send_query_email_with_invalid_subject`.
- **Test Isolation**: Each test should be independent and not rely on the state created by another test. Use setup and teardown methods where necessary to create a consistent test environment.
- **Mock External Services**: External services (like email sending or API calls) should be mocked to avoid incurring any unnecessary costs and also avoid dependency on any external factors.
- **Test Coverage**: Aim for 100% coverage. Consider edge cases, limitations, successful or failed executions. Get creative.
- **Use Assertions Effectively**: Use the appropriate assertion methods to check that test results are what you expected.
- **Documentation**: Commenting should be sparse as the code should generally be written in such a way that it is easily understood. However, it is still preferential to add a comment to clarify rationale or intention when it may be unclear. There is also a current commenting convention in place for tests that provides a short summary of the tests objective above each test method.

#### Running Tests

- Before submitting a pull request, always ensure that all tests run and pass locally. You can run the tests using the following command: `python manage.py test`

#### Considerations

- **Code Changes**: Ensure that existing tests are still running successfully when making any changes to existing code.
- **Test Data**: Use representative sample data for tests. Never use sensitive or real user data.

---

## Frequently Asked Questions (FAQs)

#### What does "Ichikoto" mean?

The idea for the project revolves around learning one word each day. In Japanese, "one word" would translate to 一つ言葉 (hitotsu kotoba). In Japanese, it is also common to shorten two words and combine them together to produce a single word that is quicker to say. An example being パソコン (pasokon) which was derived from パーソナルコンピューター (paasonaru-konpyuutaa) meaning personal computer or laptop. Taking this word fusion idea I ended up on 一事 (hitokoto) meaning one thing but ended up preferring the (ichi) reading for 一 over the (hito) reading. So we ended up on 一事 (ichikoto) meaning "one thing". It's not quite the same as "one word" but I think the spirit is still there and it's a bit more catchy.

#### What is lockfile.lock?

This could easily be an error on my part but on server launch I would consistently have two threads running despite only intending to have one. I added flags and tried a few variations of that sort of solution to attempt to deter the second thread from running. Despite the flag seeming to be correctly implemented the issue would not resolve. Eventually, I landed on this idea of a lock file and decided to give it a try. It checks if a _lockfile.lock_ exists when the thread is executed. If it doesn't then it creates one then executes. If the _lockfile.lock_ already exists it will not execute. The file is then deleted on server shutdown. It may not be the best way to handle this but it workss for the time being and has no noticeable impact on performance.

#### Why Django?

Initially, I found myself wondering the same thing. There was no backend being utilized and I began to feel like this would've been better off as a desktop application. Maybe it still is? I really don't know. But I initially chose Django because I thought this would be a fun opportunity to familiarize with it. While learning it I stumbled upon SQLite and after digging deeper realized I wanted to implement it into the project. So although, the initial idea didn't actually need to be written in Django, it did end up benefitting because I was able to easily implement the backend for keeping track of learned words.

#### Why only Japanese?

I personally am learning Japanese so of course I made a project that would benefit me. However, I did my best to write the code in a way that would make it easier to add options for other languages in the future. It is my hope that over time contributors may add support for more languages.

#### Why threading over celery?

In this specific case threading just feels more appropriate. Celery would require more resources, external dependencies, and introduce more complexity into the project. With the small scale of this project threading is able to carry out the same functionality with less resource usage and more simplicity. However, if plans to add more asynchronous task scheduling arise then Celery would be up for consideration.

#### Why manual mode tests for OpenAI API calls?

I struggled implementing mock API calls for the openai python library in the tests for gpt_service.py. For whatever reason, despite mocking them in what I believed was the proper way, the actual API calls were still being made. The cost of an API call is negligible with OpenAI but I still didn't like the idea of incurring charges every time tests were run. As a result, I ended up on the idea of manual tests, at least until a better solution can be devised. While the manual mode tests aren't significantly raising confidence in the code I feel they still provide some benefits. They do still raise some confidence in the logic being used in the code as well as the codes ability to execute. At the very least, it's better than nothing.

#### Why aren't the email formats consistent?

In my testing, the current prompt produces relatively consistent responses from the OpenAI API. Despite this, it is really difficult to build a prompt with a 100% consistent response format. It will sometimes spit out responses that contain slight differences regardless of how specific the prompt is. At the current time, I don't feel it's worth incurring the extra cost by increasing the prompt size to push for a small increase in consistency when the rate of consistency is already as high as it is. As such, the short answer is, "because that's the response gpt felt like giving you that day".

#### Why won't my server start?

- Check and watch the logs during execution for anything abnormal.
- Try to run the tests.
  - `python manage.py test`
- Check keys and scheduled times are correct in `.env`
- If nothing helps, open an issue.

#### How do I contribute?

Please check the [Contribution Guidelines](#contribution-guidelines) section to understand what requirements must be met to make a contribution and then follow these steps when you're ready to make a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m 'Add some YourFeature'`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

#### How do I get a new OpenAI API key?

- If you lost your OpenAI API key simply repeat the steps outlined in the [Obtaining an API Key from OpenAI](#obtaining-an-api-key-from-openai) section.
- When you reach step 3, delete the old key and create a new key.
- Then replace the old key with the new key in the `.env` file.

---

## Future Plans

- Add option to set a scheduled time range to pick a random time from each day
- Add support for more languages
- Handling existing issues

---

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## Acknowledgments

- OpenAI's ChatGPT API
- Mailjet's Email Service
- Django Community
- All Contributors and Supporters
