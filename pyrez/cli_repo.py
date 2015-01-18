import click
from .models import Repo
from . import session

def select_server(text="Which repository do you want to remove?"):
  for id in session.query(Repo.id).all():
    click.echo("* %s" % id)
  return click.prompt(text, prompt_suffix=" ")


@click.group(name="repo", invoke_without_command=True)
@click.pass_context
def group(ctx):
  """Repository management utilities"""
  if ctx.invoked_subcommand is None:
    show()


@group.command()
@click.argument('uri', required=False)
@click.option('--no-activate', is_flag=True, default=False)
def add(uri, no_activate):
  """Add a repository by its URI"""
  if not uri:
    uri = click.prompt("Repository URI", default="http://127.0.0.1:9876/index.json")
  server = Repo(uri, activate=(not no_activate))
  session.add(server)
  session.commit()


@group.command()
@click.argument('repo_id', required=False)
@click.option('-t', '--delete-tracks', is_flag=True, default=None)
@click.option('-y', '--yes', is_flag=True, default=False, help="Assume 'yes' on the confirmation prompt")
def remove(repo_id, delete_tracks, yes):
  """Remove a repository, optionally deleting its tracks as well"""
  if repo_id is None:
    repo_id = select_server("Which repository do you want to remove")

  if yes or click.confirm("Do you really want to remove server %s?" % repo_id):
    session.delete(session.query(Repo).filter(Repo.id == repo_id).first())
    session.commit()
    click.echo("Deleted!")

    if delete_tracks or click.confirm("Do you want to delete tracks as well?"):
      click.echo("NIY")

  else:
    click.echo("Aborted.")


@group.command()
@click.argument('repo_id', required=False)
def activate(repo_id):
  """Activate a repository"""
  if repo_id is None:
    repo_id = select_server("Which repository do you want to activate?")

  session.query(Repo).filter(Repo.id == repo_id).first().active = True
  session.commit()


@group.command()
@click.argument('repo_id', required=False)
def deactivate(repo_id):
  """Deactivate a repository"""
  if repo_id is None:
    repo_id = select_server("Which repository do you want to deactivate?")

  session.query(Repo).filter(Repo.id == repo_id).first().active = False
  session.commit()


@group.command("set-uri")
@click.argument('repo_id', required=False)
@click.argument('newuri', required=False)
def set_uri(repo_id, newuri):
  """Change repository's URI"""
  if repo_id is None:
    repo_id = select_server("Which repository do you want to modify?")

  repo = session.query(Repo).filter(Repo.id == repo_id).first()

  if newuri is None:
    newuri = click.prompt("New URI", default=repo.uri)
  
  server.uri = newuri
  session.commit()


@group.command()
@click.argument('repo_id', required=False)
def show(repo_id):
  """Display information about a repository or list all repositories"""
  CHECKED = click.style("[✓]", fg='green')
  UNCHECKED = click.style("[✗]", fg='red')

  q = session.query(Repo)
  if repo_id is not None:
    q.filter(Repo.id == repo_id)

  for r in q.all():
    click.echo( "%s %s" % (CHECKED if r.active else UNCHECKED, r.id))
    click.echo("    %s" % r.uri)