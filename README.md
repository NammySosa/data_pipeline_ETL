# /r/bapcsalescanada Dashboard - ETL Data Pipeline

A Looker dashboard powered by an automated, batch-processing ETL data pipeline.

Data from the /r/buildapcsalescanada subreddit is extracted, analyzed, and visualized. 

The pipeline features some tools used in modern data engineering stacks, including Terraform, Airflow (via Docker containers), and Amazon Redshift as the target cloud data warehouse.


## Project Inspiration

The purpose of this project was to learn and develop some data engineering & analyst skills, and to build an understanding of the end-to-end processes involved in the data lifecycle. 

This project provides insights into deals related to the Canadian computer hardware / peripherals market, via /r/buildapcsalescanada.

This project references [this project](https://github.com/ABZ-Aaron/Reddit-API-Pipeline) by [ABZ-Aaron](https://github.com/ABZ-Aaron).

## Data Pipeline Architecture

<img src="https://github.com/NammySosa/data_pipeline_ETL/blob/main/images/etl%20architecture.PNG" width=75% height=75%>

1. Infrastructure is created -- AWS Resources (S3 + Redshift) are deployed with code using Terraform
2. Docker containers are initiated -- Airflow executes DAG to begin ETL process
3. Extract - Data is extracted via the Reddit API
4. Transform - Transformations are done on the data in the python script, saved to CSV
5. Load - CSV file is loaded onto S3, and data from CSV is ingested into Redshift
6. Looker Dashboard connects to Amazon Redshift table


## Prerequisites 

For this project, one will need to set up and configure a few things.

- Python
- Reddit account, and create a [developer application](https://www.reddit.com/prefs/apps)
  - The application should provide you a client id and secret key, which will be used to access the reddit API via the python wrapper
- AWS account and AWS command line interface (CLI) [configured](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start)
- Install [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)


## Setup

If you're interested in setting up a similar project, I HIGHLY recommend following [Aaron's setup guide](https://github.com/ABZ-Aaron/Reddit-API-Pipeline#setup) as it is well-documented and beginner friendly. 

This project was set up in an Ubuntu 22.04.1 environment via WSL2, using Windows 10. It uses the free-tier AWS resources, so it costs nothing to run. 
Feel free to shoot me a message if you have any questions.

## Dashboard

[<img src="https://github.com/NammySosa/data_pipeline_ETL/blob/main/images/dashboardimg.PNG" width=60% height=60%>](https://lookerstudio.google.com/u/0/reporting/a6814946-0e45-4619-a19a-19347f8f07ab/page/p_uzcoiqdr4c)

## Final Notes / Improvements

Setting up our containers with the necessary dependencies/libraries with the _PIP_ADDITIONAL_REQUIREMENTS feature is a quick-start method to utilising Airflow which is great for testing/development, but should not be used in production-level works. [Source](https://github.com/apache/airflow/discussions/24809#discussioncomment-3071139)

The containers are being run locally, so technically the pipeline is automated so long as my PC stays on. The containers need to be re-started if my local machine is ever shut off.

Alternatively, an EC2 (or any other cloud computing service) instance could be used to run the containers but that would come at a higher cost.







