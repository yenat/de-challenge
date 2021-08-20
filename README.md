
## Introduction
This project extracts daily information from Binance platform, stores the data into S3 and creates two api endpoint where a user can either request for information with regard to the latest daily price for these currencies ADABTC, ADAUSDT, BTCUSDT and also obtain information on the profit that could be made during the last 24 hours. The information in S3 is updated on an hourly basis.
## Methodology
A process is built that accesses Binance’s public API. In order to make this happen, one lambda function is created to extract information from Binance api and store the result in S3 for the purpose of ingestion. Another lambda function is also created to take the data from S3 as input and expose the result to user through api gateway endpoint. Four aws services were used to build the overall system: these are aws lambda, aws s3, aws api gateway and aws eventbridge.
### AWS Lambda:
Upload ingestion and server scripts and the required packages using update functions 
Add trigger, selecting API gateway from the server lambda function specifying the deployment stage of the api gateway
### AWS S3:
Store data extracted from binance endpoint in csv format
### AWS API Gateway:
Create stage name and deployment stage
Create two resources price and profit with each having a method of GET
Inside the method execution setting of ‘price’ resource, under URL Query String parameter, add the query string ‘currency’, whereas for the ‘profit, add ‘value’ and ‘currency’ as query string.
Inside the integration request, the server lambda function is specified including region, execution role. Under mapping templates, the content type is entered as application/json having a content of this: {"value":"$input.params('value')",
                                                                             "currency":"$input.params('currency')"}
After all these changes have been made, the action deploy api is executed which results in two urls for the two endpoints.
### AWS Eventbridge:
Create eventrule for the ingestion lambda function
This is set up to deploy the process such that it runs every hour to update S3 with the newest data
## Deliverables
The following schema shows the ingestion and also the server part of the system. At the top, the schema shows how the daily price of the three currencies are extracted from binance with lambda function and stored in S3 in csv file format and this process is scheduled to run every hour through eventbridge service. On the lower part, it shows how the data from S3 reaches the client using the api gateway for the request of one the latest price of the currencies and two how much profit would be made during the last 24 hours.


The system gives a status code of 500 for internal server errors or connection failure, for the cases of mismatched type of data, null/empty data the system gives status code 400. For the normal working of it, it shows a status code of 200 with the right results returned.
The source code for the implementation can be found here. The url for the two endpoints are the following.
[profit] (https://qga54ezbbl.execute-api.eu-central-1.amazonaws.com/challenge/profit?value=1000&currency=ADAUSDT)
[price] (https://qga54ezbbl.execute-api.eu-central-1.amazonaws.com/challenge/price?currency=ADAUSDT)
The lambda function is set up with python 3.7 configuration through installing the necessary packages such as pandas, numpy, requests, pytz and boto3. It also contains the python scripts for the ingestion and server side. 
For the lambda service, a tester can go into the lambda function, open the Test window and write the values (inputs) in the test event and click on Test. The service will be executed and either a failure or success with the result will be returned. In the api gateway, the tester can go into the Resources pane, choose the method to be tested. In the Method Execution pane, in the Client box, choose Test. Type values in any of the displayed boxes (such as Query Strings, Headers, and Request Body). From the user perspective, it can be tested through providing various use cases such as mismatched or empty data and including the right format of the data.
## Summary
In general, I have gained remarkable knowledge within this limited time working on this specific task. Starting from lambda functions, scheduling the function to deploying in the api gateway. Some of the challenges were with setting up the virtual environment for the lambda functions, the other one is identifying each piece of the api gateway for the purpose of integration with the lambda function and also the issues with permissions in the gateway and during scheduling in Eventbridge. All in all, I would say I definitely had so much fun working on this task, especially extracting the information from Binance as required and testing the lambda functions.
## References
[1] https://csguide.cs.princeton.edu/software/virtualenv

[2] https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
[3] https://steemit.com/python/@marketstack/how-to-download-historical-price-data-from-binance-with-python
[4] https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-with-lambda-integration.html
[5] https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
[6] https://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-code.html
[7] https://docs.amazonaws.cn/en_us/lambda/latest/dg/python-package.html
[8] https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html

