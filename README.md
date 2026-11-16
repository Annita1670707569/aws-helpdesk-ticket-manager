# Helpdesk Ticket Manager (Serverless AWS)

A serverless web application built on AWS that allows users to submit repair/support tickets via a web form, store ticket records in a NoSQL database, and trigger instant email notifications.

## System Architecture
<img width="1376" height="768" alt="Gemini_Generated_Image_ahwp9lahwp9lahwp" src="https://github.com/user-attachments/assets/2292e48e-f265-4c93-8ea3-e2dede135593" />


**Workflow:** `User` ➔ `Amazon S3` ➔ `API Gateway` ➔ `AWS Lambda` ➔ `DynamoDB` & `Amazon SNS`

* **Frontend:** Amazon S3 Static Website Hosting (`index.html`)
* **API Layer:** Amazon API Gateway (`POST /tickets`)
* **Compute:** AWS Lambda (`Python 3.12`)
* **Database:** Amazon DynamoDB (`HelpdeskSystem2026`)
* **Notification:** Amazon SNS (`HelpdeskNotify2026`)

## Deployment Guide

To deploy this project in your own AWS account (`us-east-1` recommended):

1. **Amazon DynamoDB**
   * Create a table named `HelpdeskSystem2026` with Partition Key `TicketID` (String).

2. **Amazon SNS**
   * Create a Standard topic named `HelpdeskNotify2026`.
   * Create an Email subscription and confirm the subscription via your inbox.

3. **AWS Lambda**
   * Create a function (`ProcessHelpdesk2026`) using **Python 3.12**.
   * Deploy the code from `lambda_function.py` and update `SNS_TOPIC_ARN` to match yours.
   * Attach IAM permissions allowing `dynamodb:PutItem` and `sns:Publish`.

4. **Amazon API Gateway**
   * Create a REST API (`HelpdeskGateway2026`).
   * Create a `/tickets` resource with a `POST` method integrated with your Lambda function.
   * Enable **CORS** on the resource and deploy the API to get your Invoke URL.

5. **Amazon S3**
   * Update the API endpoint URL inside `index.html`.
   * Create an S3 bucket, enable **Static website hosting**, configure public read bucket policy, and upload `index.html`.
