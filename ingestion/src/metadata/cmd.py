#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging
import os
import pathlib
import sys

import click
from pydantic import ValidationError

from metadata.config.common import load_config_file
from metadata.ingestion.api.workflow import Workflow

logger = logging.getLogger(__name__)

logging.getLogger("urllib3").setLevel(logging.WARN)

# Configure logger.
BASE_LOGGING_FORMAT = (
    "[%(asctime)s] %(levelname)-8s {%(name)s:%(lineno)d} - %(message)s"
)
logging.basicConfig(format=BASE_LOGGING_FORMAT)


@click.group()
def check() -> None:
    pass


@click.group()
@click.option("--debug/--no-debug", default=False)
def metadata(debug: bool) -> None:
    if os.getenv("METADATA_DEBUG", False):
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger("metadata").setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)
        logging.getLogger("metadata").setLevel(logging.INFO)


@metadata.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="Workflow config",
    required=True,
)
def ingest(config: str) -> None:
    """Main command for ingesting metadata into Metadata"""
    config_file = pathlib.Path(config)
    workflow_config = load_config_file(config_file)

    try:
        logger.info(f"Using config: {workflow_config}")
        if workflow_config.get('cron'):
            del workflow_config['cron']
        workflow = Workflow.create(workflow_config)
    except ValidationError as e:
        click.echo(e, err=True)
        sys.exit(1)

    workflow.execute()
    workflow.stop()
    ret = workflow.print_status()
    sys.exit(ret)

@metadata.command()
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="Workflow config",
    required=True,
)
def report(config: str) -> None:
    """Report command to generate static pages with metadata"""
    config_file = pathlib.Path(config)
    workflow_config = load_config_file(config_file)
    file_sink = {'type': 'file', 'config': {'filename': '/tmp/datasets.json'}}

    try:
        logger.info(f"Using config: {workflow_config}")
        if workflow_config.get('cron'):
            del workflow_config['cron']
        if workflow_config.get('sink'):
            del workflow_config['sink']
        workflow_config['sink'] = file_sink
        ### add json generation as the sink
        workflow = Workflow.create(workflow_config)
    except ValidationError as e:
        click.echo(e, err=True)
        sys.exit(1)

    workflow.execute()
    workflow.stop()
    ret = workflow.print_status()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metadata_server.openmetadata.settings')
    try:
        from django.core.management import call_command
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        call_command('runserver', 'localhost:8000')
    except ImportError as exc:
        logger.error(exc)
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

metadata.add_command(check)
