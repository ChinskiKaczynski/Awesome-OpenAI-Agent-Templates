def test_imports():
    import importlib
    assert importlib.import_module("openai") is not None
