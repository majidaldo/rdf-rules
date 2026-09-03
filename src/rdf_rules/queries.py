
def align(s):
    _ = s
    _ = _.split('\n')
    _ = (l.strip() for l in _)
    _ = '\n'.join(_)
    return _

from .prefixes import prefixes as p
_ = f"""
prefix meta:<{p['meta']}>
construct {{?s ?p ?o}}
where {{
# mapped data
{{
    << ?s ?p ?o>> meta:path ?pth.
    FILTER(STRENDS(lcase(STR(?pth)), ".mapping.rq") || STRENDS(lcase(STR(?pth)), ".mapping.sparql") )
    }}
# inferred data
union
{{
        << ?s ?p ?o>> meta:shaclmode "inference".
    }}
}}
"""
mapped_and_inferred = align(_)


_ = f"""
prefix meta:<{p['meta']}>
construct {{?s ?p ?o}}
where {{
{{
<< ?s ?p ?o>> meta:shaclmode "validation".
}}
}}
"""
validation = align(_)


from pyoxigraph import Store
def query(db: Store, query: str):
    """small convenience"""
    if query in globals():
        q = globals()[query]
    else:
        q = query
    _ = db.query(q)
    return _

del _
del align