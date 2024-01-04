import discogs_client
import json

from collections import OrderedDict
from operator import getitem


USER_AGENT = 'DiscogsUtils'

def sort_collection_by_master_version_release_year(
    user_token: str,
    reverse: bool = False,
    user_agent: str = None,
) -> dict:
    '''
    Sort a user's collection by year of the album's initial release (as opposed to the release of
    the particular pressing in the collection).
    '''

    client = discogs_client.Client(USER_AGENT, user_token=user_token)

    items = dict()
    print('Gathering info about....')
    for item in client.identity().collection_folders[0].releases:
        release = item.release
        master = release.master
        print(f'"{item.release.title}" by {release.artists[0].name}')
        items[release.id] = {
            'artists': [ artist.name for artist in release.artists ],
            'title': release.title,
            'item_id': release.id or 0,
            'item_year': release.year or 0,
            'master_id': master.id if master else 0,
            'master_year': master.year if master and master.year > 0 else release.year,
        }

    with open('data.json', 'w') as fh:
        fh.write(json.dumps(items, indent=2))

    return OrderedDict(sorted(items.items(),
        key=lambda x: getitem(x[1], 'master_year'),
        reverse=reverse))

