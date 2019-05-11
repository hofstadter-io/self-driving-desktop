import click

from self_driving_desktop import parser as P
from self_driving_desktop import recorder as R


@click.command()
@click.argument('playlist')
@click.option('--record', is_flag=True, help='Record to a playlist.')
def drive(playlist, record):
    if record is True:
        doRecord(playlist)
    else:
        doPlay(playlist)


def doPlay(playlist):
    P.run(playlist)


def doRecord(playlist):
    R.do(playlist)
