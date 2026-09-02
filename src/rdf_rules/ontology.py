# no need to load in data
from pathlib import Path

class types:
    class path:
        from typing import Annotated
        from beartype.vale import Is
        type = Annotated[Path, Is[lambda p: str(p).endswith('ontology.ttl')]  ]
        # so you can have like s223-ontology.ttl if you want to distinguish
    from typing import Literal
    modes = Literal['inference'] | Literal['validation']

from pyoxigraph import Store
from .base import BaseMeta
class Shifty(BaseMeta):
    def __init__(self, 
            mode: types.modes,
            ontology: types.path.type = Path('ontology'),
            additional_params = {},
                   ) -> None:
        self.mode = mode
        self.ontology = ontology
        self.additional_params = additional_params

    def params(self):
        return {
            'shaclmode':  self.mode,
            'ontology': self.ontology.as_posix(),
                **self.additional_params }
    
    def data(self, db: Store):
        from .queries import mapped_and_inferred
        d = db.query(mapped_and_inferred)
        from pyoxigraph import serialize, parse, RdfFormat
        # to get the diff, bc shifty doesn't give it out
        if self.mode == 'inference': d = frozenset(d)
        _ = serialize(d,
                format=RdfFormat.TURTLE)
        if self.mode == 'inference':
            from shifty import infer
            _ = infer(_, self.ontology)
            # quads out
            _ = parse(_.graph_ntriples, format=RdfFormat.N_TRIPLES)
            _ = (q.triple for q in _)
            _ = frozenset(_) - frozenset(d)
        else:
            assert(self.mode == 'validation')
            from shifty import validate
            conforms, report_graph, results_text = \
                validate(_, self.ontology,
                    infer=False,
                    sort_results=False,)
            _ = report_graph.serialize()  # why this rdflib graph?!
            self.conforms = conforms
            _ = parse(_, format=RdfFormat.TURTLE)
            _ = (q.triple for q in _)
        yield from _

