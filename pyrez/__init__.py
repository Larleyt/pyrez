import click
from sqlalchemy import text as literalSQL
import traceback
import os
from os import path

from .models import *
from .util import engine_and_session

APP_DIR = click.get_app_dir("Songbee")

try:
  os.makedirs(APP_DIR)
except OSError as e: # Dirs already exist
  pass

engine, session = engine_and_session("sqlite:///" + path.join(APP_DIR, "database.db"))
Base.metadata.create_all(engine)

CONTEXT_SETTINGS = {
  'help_option_names': ['-h', '--help']
}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
def cli():
  pass


@cli.command()
@click.argument('server_names', nargs=-1, required=False)
def update(server_names):
  """Update the track database."""
  if len(server_names) == 0:
    servers = session.query(Repo).filter_by(active=True)
  else:
    servers = session.query(Repo).filter(Repo.id.in_(server_names))

  for repo in servers:
    try:
      click.echo("Processing %s..." % repo.id)
      tracks = repo.get_tracks()

      with click.progressbar(session.query(Track).filter(Track.repo == repo).all(),
        label="Removing old tracks...") as old_tracks:
        for track in old_tracks:
          session.delete(track)

      with click.progressbar(tracks, label="Adding tracks...") as tracks:
        for track_info in tracks:
          session.add(Track(
            id="%s/%s" % (repo.id, track_info['id']),
            title=track_info['title'],
            artist=track_info['artist'],
            uri=track_info['uri'],
            repo=repo))

    except Exception as e:
      session.rollback()
      click.echo("Error while trying to update repo %s:" % repo.id)
      click.echo(traceback.format_exc())
      if click.confirm("Continue?"):
        continue
      else:
        break

    else:
      session.commit()


@cli.command()
@click.option('--artist')
@click.option('--title')
@click.option('--limit', type=int, default=5)
def lookup(artist, title, limit):
  """Find a track by its title or artist."""
  q = session.query(Track)
  if artist is not None:
    q = q.filter(literalSQL("lower(artist) like :query")).params(query=("%%%s%%" % artist).lower())
  if title is not None:
    q = q.filter(literalSQL("lower(title) like :query")).params(query=("%%%s%%" % title).lower())
  q = q.limit(limit)

  for track in q.all():
    click.echo("%s by %s" % (track.title, track.artist))
    click.echo("      %s" % track.uri)


from .cli_repo import group as cli_repo
cli.add_command(cli_repo)