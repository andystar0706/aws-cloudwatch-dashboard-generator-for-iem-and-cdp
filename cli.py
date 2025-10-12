# cli.py
import argparse
import os

def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog='generator',
        description='CloudWatch Dashboard Generator - Generate CloudWatch Dashboard from CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''

Usage Examples:
  # Set environment variables (recommended)
  export AWS_ACCESS_KEY_ID=<your-access-key>
  export AWS_SECRET_ACCESS_KEY=<your-secret-key>
  
  # Basic usage - Kafka cluster
  python generator.py --region us-east-1 --name cluster-01 --namespace AWS/Kafka
  
  # ElasticSearch with custom output
  python generator.py --region us-east-1 --name cluster-01 --namespace AWS/ES --dashboard-name my-es-dashboard --output dashboard.json
  
  # Generate JSON only (no upload to CloudWatch)
  python generator.py --region us-east-1 --name cluster-01 --namespace AWS/Kafka --no-upload

  # Custom CSV file path
  python generator.py --region us-east-1 --name cluster-01 --namespace AWS/ES --csv /path/to/my-custom-metrics.csv
        '''
    )
    parser._optionals.title = 'Optional arguments'

    parser.add_argument('--region', type=str, required=True, help='AWS region (e.g., us-east-1, ap-east-1)')
    parser.add_argument('--name', type=str, required=True, help='Resource name (e.g., cluster-01)')
    parser.add_argument('--namespace', type=str, required=True, help='CloudWatch namespace (e.g., AWS/Kafka, AWS/EC2)')

    #parser.add_argument('--aws-access-key-id', type=str, required=True, help='AWS Access Key ID')
    #parser.add_argument('--aws-secret-access-key', type=str, required=True, help='AWS Secret Access Key')
    A = ''
    parser.add_argument('--aws-access-key-id', type=str, default=os.environ.get('AWS_ACCESS_KEY_ID'), help='AWS Access Key ID (default: read from environment variable AWS_ACCESS_KEY_ID)')
    parser.add_argument('--aws-secret-access-key', type=str, default=os.environ.get('AWS_SECRET_ACCESS_KEY'), help='AWS Secret Access Key (default: read from environment variable AWS_SECRET_ACCESS_KEY)')
    parser.add_argument('--csv', type=str, default=None, help='CSV file path')
    parser.add_argument('--output', type=str, default='dashboard.json', help='Output file path (default: dashboard.json)')
    parser.add_argument('--dashboard-name', type=str, default=None, help='Custom Dashboard name (default: auto-generated)')
    parser.add_argument('--no-upload', action='store_true', help='Do not upload to CloudWatch')
    
    return parser

def parse_args():
    """解析并返回命令行参数"""
    parser = create_parser()
    return parser.parse_args()