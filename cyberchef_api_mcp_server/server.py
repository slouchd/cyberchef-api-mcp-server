#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import httpx
import logging
from typing import Optional
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from cyberchef_api_mcp_server.cyberchefoperations import CyberChefOperations

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create an MCP server
mcp = FastMCP("CyberChef API MCP Server")

# Determine the CyberChef API URL
cyberchef_api_url = os.getenv("CYBERCHEF_API_URL")
if cyberchef_api_url is None:
    log.warning("There is no environment variable CYBERCHEF_API_URL defaulting to http://localhost:3000/")
    cyberchef_api_url = "http://localhost:3000/"


class CyberChefRecipeOperation(BaseModel):
    """Model for a recipe operation with or without arguments"""
    op: str
    args: Optional[list] = None


def create_api_request(endpoint: str, request_data: dict) -> dict:
    """
    Send a POST request to one of the CyberChef API endpoints to process request data and retrieve the response

    :param endpoint: API endpoint to retrieve data from
    :param request_data: data to send with the POST request
    :return: dict object of response data
    """
    api_url = f"{cyberchef_api_url.rstrip('/')}/{endpoint.lstrip('/')}"
    request_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        log.info(f"Attempting to send POST request to {api_url}")
        response = httpx.post(
            url=api_url,
            headers=request_headers,
            json=request_data
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as req_exc:
        log.error(f"Exception raised during HTTP POST request to {api_url} - {req_exc}")
        return {"error": f"Exception raised during HTTP POST request to {api_url} - {req_exc}"}


@mcp.resource("data://cyberchef-operations-categories")
def get_cyberchef_operations_categories() -> list:
    """Get updated Cyber Chef categories for additional context / selection of the correct operations"""
    cyberchef_ops = CyberChefOperations()
    return cyberchef_ops.get_all_categories()


@mcp.resource("data://cyberchef-operations-by-category/{category}")
def get_cyberchef_operation_by_category(category: str) -> list:
    """
    Get list of Cyber Chef operations for a selected category

    :param category: cyber chef category to get operations for
    :return:
    """
    cyberchef_ops = CyberChefOperations()
    return cyberchef_ops.get_operations_by_category(category=category)


@mcp.tool()
def bake_recipe(input_data: str, recipe: list[CyberChefRecipeOperation]) -> dict:
    """
    Bake (execute) a recipe (a list of operations) in order to derive an outcome from the input data

    :param input_data: the data in which to perform the recipe operation(s) on
    :param recipe: a pydantic model of operations to 'bake'/execute on the input data
    :return:
    """
    request_data = {
        "input": input_data,
        "recipe": [op.model_dump() for op in recipe]
    }
    response_data = create_api_request(endpoint="bake", request_data=request_data)

    # If the response has a byte array, decode and return
    data_type = response_data.get("type")
    if data_type is not None and data_type == "byteArray":
        decoded_value = bytes(response_data["value"]).decode()
        response_data["value"] = decoded_value
        response_data["type"] = "string"
        return response_data
    else:
        return response_data


@mcp.tool()
def batch_bake_recipe(batch_input_data: list[str], recipe: list[CyberChefRecipeOperation]) -> dict:
    """
    Bake (execute) a recipe (a list of operations) in order to derive an outcome from a batch of input data

    :param batch_input_data: the batch of data in which to perform the recipe operation(s) on
    :param recipe: a list of operations to 'bake'/execute on the input data
    :return:
    """
    request_data = {
        "input": batch_input_data,
        "recipe": [op.model_dump() for op in recipe]
    }
    response_data = create_api_request(endpoint="batch/bake", request_data=request_data)

    # If any of the responses have a byte array, decode and return
    for response in response_data:
        data_type = response.get("type")
        if data_type is not None and data_type == "byteArray":
            decoded_value = bytes(response["value"]).decode()
            response["value"] = decoded_value
            response["type"] = "string"

    return response_data


@mcp.tool()
def perform_magic_operation(
        input_data: str,
        depth: int = 3,
        intensive_mode: bool = False,
        extensive_language_support: bool = False,
        crib_str: str = ""
) -> dict:
    """
    CyberChef's magic operation is designed to automatically detect how your data is encoded and which operations can be
    used to decode it

    :param input_data: the data in which to perform the magic operation on
    :param depth: how many levels of recursion to attempt pattern matching and speculative execution on the input data
    :param intensive_mode: optional argument which will run additional operations and take considerably longer to run
    :param extensive_language_support: if this is true all 245 languages are supported opposed to the top 38 by default
    :param crib_str: argument for any known plaintext string or regex
    :return:
    """
    request_data = {
        "input": input_data,
        "args": {
            "depth": depth,
            "intensive_mode": intensive_mode,
            "extensive_language_support": extensive_language_support,
            "crib": crib_str
        }
    }
    return create_api_request(endpoint="magic", request_data=request_data)


def main():
    """Initialize and run the server"""
    log.info("Starting the CyberChef MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
