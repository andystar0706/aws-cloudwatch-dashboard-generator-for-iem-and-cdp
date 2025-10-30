import boto3
import csv
import json
from typing import List, Dict, Any
from utils import is_integer, is_valid_word, is_valid_statistic, save_to_json, get_current_timestamp, get_logger
from cli import parse_args

class DashboardGenerator:
    def __init__(self, config: Dict[str, str]):
        self.region = config['region']
        self.resource_name = str(config['resource_name'])
        self.namespace = config['namespace']
        self.client = boto3.client('cloudwatch',
                                 region_name=config['region'],
                                 aws_access_key_id=config['aws_access_key_id'],
                                 aws_secret_access_key=config['aws_secret_access_key'])
        self.period = 60
        
        # Dashboard layout settings
        self.x = 0
        self.y = 0
        self.width = 12
        self.height = 6
        self.dashboard = {"widgets": []}
        self.dashboard_name = config['namespace'].replace('AWS/','')+'_'+config['region']+'_'+config['resource_name'].replace('/','')+'_'+get_current_timestamp()
        
        # Logger settings
        self.logger = get_logger(self.dashboard_name)

    def get_metrics(self, metric_name: str) -> List[List[str]]:
        """獲取指定 metric 的所有維度"""
        metrics = []
        metric_list = self.client.list_metrics(
            Namespace=self.namespace, 
            MetricName=metric_name
        )

        for metric in metric_list['Metrics']:
            for i in range (len(metric['Dimensions'])):
                if metric['Dimensions'][i]['Value'] == self.resource_name: ## 每個 Resource Name 處於不同維度
                    tmp = [
                        metric['Namespace'],
                        metric['MetricName']
                    ]
                    for dimension in metric['Dimensions']:
                        tmp.extend([dimension['Name'], dimension['Value']])
                    metrics.append(tmp)
                    break

        return metrics

    def update_position(self):
        """更新 widget 位置"""
        if self.x == self.width:
            self.x = 0
            self.y += self.height
        else:
            self.x = self.width

    def add_widget(self, metrics: List[List[str]], threshold: int = None, statistic: str = None):
        """添加 widget 到 dashboard"""
        widget = {
            "type": "metric",
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "properties": {
                "metrics": metrics,
                "view": "timeSeries",
                "region": self.region,
                "period": self.period
            }
        }

        if statistic is not None:
            widget["properties"]["stat"] = statistic

        if threshold is not None:
            widget["properties"]["annotations"] = {
                "horizontal": [{
                    "value": threshold,
                    "label": "Threshold"
                }]
            }

        self.dashboard["widgets"].append(widget)
        self.update_position()

    def process_csv(self, csv_path: str):
        """處理 CSV 文件"""
        with open(csv_path, newline='') as csvfile:
            rows = list(csv.reader(csvfile))

        for row in rows[1:]:  # Skip header
            metrics = []
            threshold = int(row[0]) if is_integer(row[0]) else None
            statistic = row[1] if is_valid_statistic (row[1]) else None

            for metric_name in row[2:]:
                if is_valid_word(metric_name):
                    print(f'[INFO] adding metric: {self.namespace} {self.region} {metric_name}')
                    self.logger.info(f'adding metric: {self.namespace} {self.region} {metric_name}')
                    metric_data = self.get_metrics(metric_name)
                    if metric_data:
                        metrics.extend(metric_data)
                    else:
                        print(f'[ERROR] no metric was found: {self.namespace} {self.region} {metric_name}')
                        self.logger.warning(f'no metric was found: {self.namespace} {self.region} {metric_name}')

            if metrics:
                self.add_widget(metrics, threshold, statistic)

    def save_dashboard(self, output_path: str):
        """保存 dashboard 配置"""
        if len(self.dashboard['widgets']) == 0:
            print("No widgets to save, please check if the conifugration is correct.")
            self.logger.warning("No widgets to save, skipping save operation")
            return False
            
        if save_to_json(self.dashboard, output_path):
            print("Dashboard Saved Successfully: " + output_path)
            self.logger.info("Dashboard Saved Successfully: " + output_path)
            return True
        else:
            print("Failed to save dashboard")
            self.logger.error("Failed to save dashboard")
            return False

    def put_dashboard(self, dashboard_name=None):
        """上傳 dashboard 配置"""
        if len(self.dashboard['widgets']) == 0:
            print("No widgets to upload")
            self.logger.warning("No widgets to upload, skipping upload operation")
            return False
            
        if dashboard_name is not None:
            self.dashboard_name = dashboard_name

        self.client.put_dashboard(DashboardName=self.dashboard_name, DashboardBody=json.dumps(self.dashboard))
        print("Dashboard Created Successfully: " + self.dashboard_name)
        self.logger.info("Dashboard Created Successfully: " + self.dashboard_name)
        return True

def main():

    # 解析命令行參數
    args = parse_args()
    
    # Configuration
    config = {
        'aws_access_key_id': args.aws_access_key_id,
        'aws_secret_access_key': args.aws_secret_access_key,
        'region': args.region, # e.g us-east-1
        'resource_name': args.name, # e.g your-resource-name
        'namespace': args.namespace # e.g AWS/Kafka
    }

    #print(config)  ### For Debugging

    # Initialize and run
    generator = DashboardGenerator(config)

    if args.csv is None:
        generator.process_csv('./recommendation/'+str(args.namespace).replace('AWS/','').lower()+'-recommended-metrics.csv')
    else:
        generator.process_csv(args.csv)

    # Save and upload
    if generator.save_dashboard(args.output):
            if not args.no_upload:
                generator.put_dashboard(dashboard_name=args.dashboard_name)
            else:
                print("Skipped uploading to CloudWatch (--no-upload flag set)")
                generator.logger.info("Skipped uploading to CloudWatch (--no-upload flag set)")

if __name__ == "__main__":
    main()