sls_package:
	npx serverless package --region $(AWS_REGION)
sls_info:
	npx serverless info --region $(AWS_REGION)
sls_deploy:
	npx serverless deploy --region $(AWS_REGION)
