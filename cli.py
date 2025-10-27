# cli.py
import argparse
import os
from utils import load_json_config

def create_parser():
    """創建命令行參數解析器"""
    parser = argparse.ArgumentParser(
        prog='python3 dashboard-generator.py',  # ← 修改這裡
        description='CloudWatch Dashboard Generator - Generate CloudWatch Dashboard from CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog='''
Usage Examples:
  # Set environment variables (recommended)
  export AWS_ACCESS_KEY_ID=<your-access-key>
  export AWS_SECRET_ACCESS_KEY=<your-secret-key>
  
  # Basic usage - Kafka cluster
  python3 dashboard-generator.py --region us-east-1 --name cluster-01 --namespace AWS/Kafka
  
  # ElasticSearch with custom output
  python3 dashboard-generator.py --region us-east-1 --name cluster-01 --namespace AWS/ES --dashboard-name my-es-dashboard --output dashboard.json
  
  # Generate JSON only (no upload to CloudWatch)
  python3 dashboard-generator.py --region us-east-1 --name cluster-01 --namespace AWS/Kafka --no-upload

  # Custom CSV file path
  python3 dashboard-generator.py --region us-east-1 --name cluster-01 --namespace AWS/ES --csv /path/to/my-custom-metrics.csv
        '''
    )
    
    required = parser.add_argument_group('Required arguments')
    required.add_argument('--region', type=str, required=True, help='AWS region (e.g., us-east-1, ap-east-1)')
    required.add_argument('--name', type=str, required=True, help='Resource name (e.g., cluster-01)')
    required.add_argument('--namespace', type=str, required=True, help='CloudWatch namespace (e.g., AWS/Kafka, AWS/EC2)')

    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument('-h', '--help', action='help', help='show this help message and exit')  # ← 手動添加 help
    optional.add_argument('--aws-access-key-id', type=str, default=os.environ.get('AWS_ACCESS_KEY_ID'), help='AWS Access Key ID (default: read from environment variable AWS_ACCESS_KEY_ID)')
    optional.add_argument('--aws-secret-access-key', type=str, default=os.environ.get('AWS_SECRET_ACCESS_KEY'), help='AWS Secret Access Key (default: read from environment variable AWS_SECRET_ACCESS_KEY)')
    optional.add_argument('--csv', type=str, default=None, help='CSV file path')
    optional.add_argument('--output', type=str, default='dashboard.json', help='Output file path (default: dashboard.json)')
    optional.add_argument('--dashboard-name', type=str, default=None, help='Custom Dashboard name (default: <Service>_<Region>_<Name>_<Timestamp>)')
    optional.add_argument('--no-upload', action='store_true', help='Do not upload to CloudWatch')
    optional.add_argument('--list', action=ListAction, help='List all supported namespaces and regions')
    
    return parser


def parse_args():
    """解析並返回命令行參數"""
    parser = create_parser()
    return parser.parse_args()

def display_all_supported_resources():
    print("=" * 80)
    print("CloudWatch Dashboard Generator - Supported Resources")
    print("=" * 80)
    print()

    # Display Regions
    regions_data = load_json_config('./definitions/regions.json')
    print("SUPPORTED REGIONS:")
    print()
    print(regions_data)
    print()

    # Display Namespaces
    namespaces_data = load_json_config('./definitions/namespaces.json')
    print("SUPPORTED NAMESPACES:")
    print()
    print(namespaces_data)
    
    print("=" * 80)
    print("\nUsage Example:")
    print("  python3 dashboard-generator.py --region us-east-1 --name cluster-01 --namespace AWS/Kafka")
    print("\nFor more help:")
    print("  python3 dashboard-generator.py --help")
    print()

class ListAction(argparse.Action):
    """Custom action for --list that exits immediately like --help"""
    def __init__(self, option_strings, dest, **kwargs):
        super(ListAction, self).__init__(
            option_strings, 
            dest, 
            nargs=0,
            default=argparse.SUPPRESS,
            **kwargs
        )
    
    def __call__(self, parser, namespace, values, option_string=None):
        display_all_supported_resources()
        parser.exit(0)  # 退出碼 0 表示成功