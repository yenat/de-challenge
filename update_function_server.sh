#!/bin/bash
lambda_name="server-lambda-123" #server lambda function
zip_file="${lambda_name}.zip"

file="lambda_function.py" #filename for the server script

chmod -R 755 ${files}
zip -r "${zip_file}" pandas boto3 $file #required packages that are installed
# in the virtual environment zipped and loaded to lambda function

aws lambda update-function-code --region "eu-central-1" --function-name "${lambda_name}" --zip-file "fileb://${zip_file}" # since the lambda function
#has already been setup, it is updated with the above packages and the ingestion script


