# Birthday notifier

# Why this project

When you are not using social medias, it might be hard to remember all important dates such as birthdays.
Especially if your calendar provider do not want to send reminder to your real email adress (I'm looking at you google),
or if you are sometimes off-line for hours at a time.

## How does it work

I made the `notifyBirthDays.py` lambda function to check if we are on a *special day* and send notifications using AWS Simple 
Notification Service if needed.

The special days are stored in AWS DynamoDB using a very simple data structure:

{{{
Item = {
    "date": "<day>-<month>",
    "label": "<message>"
}
}}}

An AWS Cloudwatch trigger will start the lambda three times a day, which make sure that I will receive at least 3 messages, just in case. 

The AWS SNS topic that will be used to send the message is configured to send an email ***and*** a SMS to my phone (SNS is awesome).

If I still manage to forget about any of these I will really have no excuses...

## A small bonus

I've been playing with the AWS Gateway API to manage the DynamoDB table. I created the `AddBirthDay.py` to be used with this service. 
A REST call can then be used to run the lambda and add an element to the table.
