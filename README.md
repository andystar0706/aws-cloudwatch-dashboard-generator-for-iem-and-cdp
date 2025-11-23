# aws-cloudwatch-dashboard-generator-for-iem-and-cdp

This tool enables users to easily monitor resource usage during IEM and CDP events. All metrics have been carefully reviewed and validated by our experts. Additionally, users can customize the metrics to fit their specific requirements.

## How to install and run the tool ?

STEP 1. Create one IAM User/Role with the following IAM Permission.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutDashboard",
                "cloudwatch:ListMetrics"
            ],
            "Resource": "*"
        }
    ]
}
```

STEP 2. Download the code from Git.
```
$ git clone https://github.com/andystar0706/aws-cloudwatch-dashboard-generator-for-iem-and-cdp.git
```

STEP 3. Install python dependencies.
```
$ cd aws-cloudwatch-dashboard-generator-for-iem-and-cdp
$ pip3 install -r requirements.txt
```

STEP 4. Run --help and --list.
```
$ python3 dashboard-generator.py --help

usage: python3 dashboard-generator.py --region REGION --name NAME --namespace NAMESPACE [-h] [--aws-access-key-id AWS_ACCESS_KEY_ID] [--aws-secret-access-key AWS_SECRET_ACCESS_KEY] [--csv CSV] [--output OUTPUT]
                                      [--dashboard-name DASHBOARD_NAME] [--no-upload] [--list]
CloudWatch Dashboard Generator - Generate CloudWatch Dashboard from CSV

Required arguments:
  --region REGION       AWS region (e.g., us-east-1, ap-east-1)
  --name NAME           Resource name (e.g., cluster-01)
  --namespace NAMESPACE
                        CloudWatch namespace (e.g., AWS/Kafka, AWS/EC2)

Optional arguments:
  -h, --help            show this help message and exit
  --aws-access-key-id AWS_ACCESS_KEY_ID
                        AWS Access Key ID (default: read from environment variable AWS_ACCESS_KEY_ID)
  --aws-secret-access-key AWS_SECRET_ACCESS_KEY
                        AWS Secret Access Key (default: read from environment variable AWS_SECRET_ACCESS_KEY)
  --csv CSV             CSV file path
  --output OUTPUT       Output file path (default: dashboard.json)
  --dashboard-name DASHBOARD_NAME
                        Custom Dashboard name (default: <Service>_<Region>_<Name>_<Timestamp>)
  --no-upload           Do not upload to CloudWatch
  --list                List all supported namespaces and regions
```
```
$ python3 dashboard-generator.py --list
================================================================================
CloudWatch Dashboard Generator - Supported Resources
================================================================================

SUPPORTED REGIONS:

['af-south-1', 'ap-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3'...]

SUPPORTED NAMESPACES:

['AWS/AmplifyHosting', 'AWS/ApiGateway', 'AWS/AppStream', 'AWS/AppSync'...]
```

STEP 5. Setup credentials
```
$ export AWS_ACCESS_KEY_ID=<your-access-key>
$ export AWS_SECRET_ACCESS_KEY=<your-secret-key>
```

⚠️ If you don't have AWS access key, please check "How do I create an AWS access key" blog below?
https://repost.aws/knowledge-center/create-access-key

STEP 6. Generate dashboard.json to create cloudwatch dashboard.
```
$ python3 dashboard-generator.py --region us-east-1 --name aos-cluster --namespace AWS/ES

[INFO] adding metric: AWS/ES us-east-1 CPUUtilization
[INFO] adding metric: AWS/ES us-east-1 WarmCPUUtilization
[INFO] adding metric: AWS/ES us-east-1 ClusterStatus.green
[INFO] adding metric: AWS/ES us-east-1 ClusterStatus.red
...
[INFO] adding metric: AWS/ES us-east-1 ThroughputThrottle
[INFO] adding metric: AWS/ES us-east-1 IopsThrottle
Dashboard Saved Successfully: dashboard.json
Dashboard Created Successfully: ES_us-east-1_aos-cluster_1760332258
```

STEP 7. Go to AWS Console, and CloudWatch and then click Dashboards button which shows on the top left side.  
STEP 8. You may see the dashobard that we just created, and Open it.

## Demo

![Demo](https://github.com/andystar0706/aws-cloudwatch-dashboard-generator-for-iem-and-cdp/blob/main/cw-dashboard-sample.png)

## How to customized the dashboard ?

1. Copy the template CSV from the recommendation folder: aws-cloudwatch-dashboard-generator-for-iem-and-cdp/recommendation/template-recommended-metrics.csv
2. The template contains the following table structure:

|Threshold|Statistic|Metric|||
| ------------- | ------------- | ------------- | ------------- | ------------- |
| {number} | {Average,Sum,Maximum,Minimum,SampleCount,p99} | Metric 1 | {Metric 2}| {Metric n}|
| 80  | Maximum  | CPUUtilization|WarmCPUUtilization||
| 0  || ClusterStatus.green|||
|||Nodes||

The only required column is **Metric 1**, and other columns with `{}` are optional.

**Adding Metrics:**
- To create a **stacked chart**, add metrics in the same row. For example, CPUUtilization and WarmCPUUtilization
- To add a **separate chart**, add a new row. For example, CPUUtilization, ClusterStatus.green and Nodes.
