#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cyberchef_api_mcp_server import server
from cyberchef_api_mcp_server.server import (
    bake_recipe, batch_bake_recipe, perform_magic_operation, CyberChefRecipeOperation
)


def test_create_api_request_normalises_base_url(monkeypatch):
    captured = {}

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": True}

    def fake_post(url, headers, json):
        captured["url"] = url
        return DummyResponse()

    monkeypatch.setattr(server, "cyberchef_api_url", "http://127.0.0.1:3000")
    monkeypatch.setattr(server.httpx, "post", fake_post)

    response = server.create_api_request(endpoint="bake", request_data={"input": "flag", "recipe": []})

    assert response == {"ok": True}
    assert captured["url"] == "http://127.0.0.1:3000/bake"


def test_bake_recipe():
    test_input = "64 47 56 7a 64 41 3d 3d"
    test_recipe = [
        CyberChefRecipeOperation(op="From Hex", args=["Auto"]),
        CyberChefRecipeOperation(op="From Base64")
    ]
    recipe_response = bake_recipe(input_data=test_input, recipe=test_recipe)

    assert recipe_response["value"] == "test"


def test_batch_bake_recipe():
    test_input = [
        "64 47 56 7a 64 41 3d 3d",
        "64 47 56 7a 64 44 49 3d"
    ]
    test_recipe = [
        CyberChefRecipeOperation(op="From Hex", args=["Auto"]),
        CyberChefRecipeOperation(op="From Base64")
    ]
    recipe_response = batch_bake_recipe(batch_input_data=test_input, recipe=test_recipe)
    recipe_response_parse = [value.get("value") for value in recipe_response]

    assert recipe_response_parse == ["test", "test2"]


def test_perform_magic_operation():
    test_input = "64 47 56 7a 64 41 3d 3d"
    recipe_response = perform_magic_operation(input_data=test_input)

    assert recipe_response["value"][0]["data"] == "test"
    assert recipe_response["value"][1]["data"] == "dGVzdA=="
    assert recipe_response["value"][2]["data"] == test_input
