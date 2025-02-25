"""`gen` tests under PEP 563."""
from __future__ import annotations

from attr import define

from cattr import GenConverter
from cattr.gen import make_dict_structure_fn, make_dict_unstructure_fn


# These need to be at the top level for `attr.resolve_types` to work.
@define
class Inner:
    a: int


@define
class Outer:
    inner: Inner


@define
class InnerB:
    a: int


@define
class OuterB:
    inner: InnerB


def test_roundtrip():
    converter = GenConverter()

    fn = make_dict_unstructure_fn(Outer, converter)

    inst = Outer(Inner(1))

    converter.register_unstructure_hook(Outer, fn)

    res_actual = converter.unstructure(inst)

    assert {"inner": {"a": 1}} == res_actual

    converter.register_structure_hook(
        OuterB, make_dict_structure_fn(OuterB, converter)
    )

    assert converter.structure({"inner": {"a": 1}}, OuterB) == OuterB(
        InnerB(1)
    )
