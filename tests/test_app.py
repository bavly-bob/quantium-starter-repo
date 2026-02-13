from dash import dcc, html
from dash.development.base_component import Component
from dash.testing.application_runners import import_app


def _walk_components(component):
    if component is None:
        return

    yield component

    children = getattr(component, "children", None)
    if children is None:
        return

    if isinstance(children, (list, tuple)):
        for child in children:
            if isinstance(child, Component):
                yield from _walk_components(child)
    elif isinstance(children, Component):
        yield from _walk_components(children)


def _get_layout_components():
    dash_app = import_app("app")
    return list(_walk_components(dash_app.layout))


def test_header_is_present():
    components = _get_layout_components()
    assert any(
        isinstance(component, html.H1)
        and component.children == "Pink Morsel Sales Visualizer"
        for component in components
    )


def test_visualisation_is_present():
    components = _get_layout_components()
    assert any(
        isinstance(component, dcc.Graph)
        and getattr(component, "id", None) == "sales-line-chart"
        for component in components
    )


def test_region_picker_is_present():
    components = _get_layout_components()
    assert any(
        isinstance(component, dcc.RadioItems)
        and getattr(component, "id", None) == "region-filter"
        for component in components
    )
