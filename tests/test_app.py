from geese.app import App, Processor

def test_get_components():
    app = App()
    app._components[1] = (1, "SomeInt")
    app._components[2] = (1, "SomeInt", False)

    assert (1, (1, "SomeInt")) in app.get_components(int, str)

    # Only returns strict matches
    assert (2, (1, "SomeInt", False)) not in app.get_components(int, str)
    assert (2, (1, "SomeInt", False)) in app.get_components(int, str, bool)
    assert (1, (1, "SomeInt")) not in app.get_components(int, str, bool)
