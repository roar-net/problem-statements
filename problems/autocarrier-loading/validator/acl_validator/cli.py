# This script validates an ACL solution against a given instance file.
# It checks if the solution is in the correct format and prints a success message.
# Usage:
# python acl-validator.py instance.json solution.json

import sys
import json
import click
from typing import TextIO
from . models import AutocarrierLoadingProblem, AutocarrierLoadingSolution

@click.group()
def cli() -> None:
    """
    Command line interface for ACL solution validation.
    """
    pass

@cli.command()
@click.argument('instance_file', type=click.File('r'))
@click.argument('solution_file', type=click.File('r'))
def validate_solution(instance_file : TextIO, solution_file : TextIO) -> None:
    """
    Validate the ACL solution against the instance file.
    """
    try:
        instance = json.load(instance_file)
    except json.JSONDecodeError as e:
        click.secho(f"🤦 Error reading JSON file {instance_file.name}: {e}", file=sys.stderr, fg="red", bold=True)
        sys.exit(1)
    try:
        solution = json.load(solution_file)
    except json.JSONDecodeError as e:
        click.secho(f"🤦 Error reading JSON file {solution_file.name}: {e}", file=sys.stderr, fg="red", bold=True)
        sys.exit(1)
    click.secho("Validating ACL Solution...", fg="blue", bold=True)

    try:
        instance = AutocarrierLoadingProblem(**instance)
    except Exception as e:
        click.secho(f"🤦 Error validating instance: {e}", file=sys.stderr, fg="red", bold=True)
        sys.exit(1)
#    try:
    solution = AutocarrierLoadingSolution(instance=instance, assigned_decks=solution)
#    except Exception as e:
#        click.secho(f"🤦 Error validating solution: {e}", file=sys.stderr, fg="red", bold=True)
#        sys.exit(1)

    print(solution.route_leg_loads)

    # Here you would implement the actual validation logic
    click.secho("✅  ACL Solution is valid.", fg="green", bold=True)
    sys.exit(0) 

