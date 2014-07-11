# pydepend

Python dependency graph

## Usage

    >>> a = Dependency('a')
    >>> b = Dependency('b')
    >>> c = Dependency('c')
    >>> d = Dependency('d')
    >>> a.depends_on([b, c])
    >>> b.depends_on(d)
    >>> a.ordered_deps
    ['d', 'b', 'c']
    