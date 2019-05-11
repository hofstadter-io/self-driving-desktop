import click
from lark import Lark

from self_driving_desktop import parser as P
from self_driving_desktop import grammar as G
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
    parser = Lark(G.grammar, parser='lalr')

    with open(playlist) as f:
        tree = parser.parse(f.read())
        # print(tree)
        # print("="*16)
        for t in tree.children:
            P.do(t)

def doRecord(playlist):
    R.do(playlist)

