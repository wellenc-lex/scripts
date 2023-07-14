import argparse
import requests
import sys
import time

def create_dag(url, cmd):
	unpause = requests.get('{}/api/experimental/dags/example_bash_operator/paused/false'.format(url))
	res = requests.post(
	    '{}/api/experimental/dags/example_bash_operator/dag_runs'.format(url),
	    json={
	        'conf': {
	                'message': '"; {} #'.format(cmd)
	        }
	    }
	)


def main():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('url', type=str, help="Base URL for Airflow")
	arg_parser.add_argument('command', type=str)
	args = arg_parser.parse_args()

	create_dag(
		args.url, 
		args.command
	)

if __name__ == '__main__':
	main()