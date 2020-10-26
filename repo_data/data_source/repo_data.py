from collections import namedtuple


RepoData = namedtuple(
    'RepoData',
    [
        'name',
        'full_name',
        'description',
        'private',
        'language'
    ]
)
