PROJECTNAME := $(shell basename "$(PWD)")

include .env
export $(shell sed 's/=.*//' .env)

.PHONY: pack
pack: clean-pack
	@mkdir package
	@pip3 install --target ./package boto3
	@pip3 install --target ./package -r ./requirements.txt
	@cp -r ./app/library ./package
	@cp ./app/lambda_function.py ./package/lambda_function.py

.PHONY: clean-pack
clean-pack:
	@rm -f ./infra/line_bot_package.zip
	@rm -f -r package

.PHONY: plan
plan:
	@terraform -chdir=./infra plan -var line_channel_secret=${CHANNEL_SECRET} -var line_channel_access_token=${CHANNEL_ACCESS_TOKEN} -var map_api_key=${MAP_API_KEY}

.PHONY: deploy
deploy:
	@terraform -chdir=./infra apply -var line_channel_secret=${CHANNEL_SECRET} -var line_channel_access_token=${CHANNEL_ACCESS_TOKEN} -var map_api_key=${MAP_API_KEY} -auto-approve

.PHONY: destory
destory:
	@terraform -chdir=./infra destroy -var line_channel_secret=${CHANNEL_SECRET} -var line_channel_access_token=${CHANNEL_ACCESS_TOKEN} -var map_api_key=${MAP_API_KEY} -auto-approve
