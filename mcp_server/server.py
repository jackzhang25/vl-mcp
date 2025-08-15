#!/usr/bin/env python3
"""
MCP Server for Visual Layer SDK
Provides functionality to manage and search datasets.
"""

from typing import Any
import os
import logging
from pathlib import Path
import sys

# Add the parent src directory to the Python path
current_dir = Path(__file__).parent
parent_src = current_dir.parent.parent / "src"
sys.path.insert(0, str(parent_src))

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("visual-layer")

# Constants
VISUAL_LAYER_API_KEY = os.getenv("VISUAL_LAYER_API_KEY")
VISUAL_LAYER_API_SECRET = os.getenv("VISUAL_LAYER_API_SECRET")


def get_client():
    """Get the Visual Layer client with proper error handling."""
    if not VISUAL_LAYER_API_KEY or not VISUAL_LAYER_API_SECRET:
        raise ValueError(
            "API credentials not found. Please set VISUAL_LAYER_API_KEY and VISUAL_LAYER_API_SECRET"
        )

    try:
        from visual_layer_sdk.client import VisualLayerClient

        return VisualLayerClient(VISUAL_LAYER_API_KEY, VISUAL_LAYER_API_SECRET)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Visual Layer client: {e}")


@mcp.tool()
async def get_all_datasets() -> str:
    """Get a list of all available datasets.

    Returns a formatted list of all datasets available in Visual Layer.
    """
    try:
        client = get_client()
        datasets_df = client.get_all_datasets()
        datasets_list = datasets_df.to_dict("records")

        if not datasets_list:
            return "No datasets found."

        # Format the datasets into a readable format
        formatted_datasets = []
        for i, dataset in enumerate(datasets_list, 1):
            formatted_dataset = f"""
Dataset {i}:
ID: {dataset.get('id', 'N/A')}
Name: {dataset.get('display_name', 'N/A')}
Description: {dataset.get('description', 'No description available')}
Created: {dataset.get('created_at', 'N/A')}
Status: {dataset.get('status', 'N/A')}
"""
            formatted_datasets.append(formatted_dataset)

        return f"Found {len(datasets_list)} datasets:\n" + "\n---\n".join(
            formatted_datasets
        )

    except Exception as e:
        return f"Error getting datasets: {str(e)}"


@mcp.tool()
async def health_check() -> str:
    """Check the health of the Visual Layer API.

    Returns the health status of the Visual Layer API.
    """
    try:
        client = get_client()
        health_status = client.healthcheck()

        return f"""
Visual Layer API Health Check:
Status: {health_status}
Message: API is healthy and responding
"""

    except Exception as e:
        return f"Health check failed: {str(e)}"


@mcp.tool()
async def get_dataset_info(dataset_id: str) -> str:
    """Get detailed information about a specific dataset.

    Args:
        dataset_id: The ID of the dataset to get information about
    """
    try:
        client = get_client()
        dataset_info = client.get_dataset(dataset_id)

        # Convert to dict if it's a DataFrame
        if hasattr(dataset_info, "to_dict"):
            dataset_info = (
                dataset_info.to_dict("records")[0] if len(dataset_info) > 0 else {}
            )

        if not dataset_info:
            return f"No dataset found with ID: {dataset_id}"

        formatted_info = f"""
Dataset Information:
ID: {dataset_info.get('id', 'N/A')}
Name: {dataset_info.get('name', 'N/A')}
Description: {dataset_info.get('description', 'No description available')}
Created: {dataset_info.get('created_at', 'N/A')}
Status: {dataset_info.get('status', 'N/A')}
Type: {dataset_info.get('type', 'N/A')}
Size: {dataset_info.get('size', 'N/A')}
"""

        return formatted_info

    except Exception as e:
        return f"Error getting dataset info: {str(e)}"


@mcp.tool()
async def search_by_labels(
    label_query: str, dataset_id: str = None, search_operator: str = "IS_ONE_OF"
) -> str:
    """Search for images within datasets using label criteria.

    Args:
        label_query: The label or text to search for in dataset labels
        dataset_id: Optional specific dataset ID to search within. If not provided, searches across all datasets.
        search_operator: Search operator to use. Options: "IS", "IS_NOT", "IS_ONE_OF", "IS_NOT_ONE_OF"
    """
    try:
        client = get_client()

        # Validate search operator
        valid_operators = ["IS", "IS_NOT", "IS_ONE_OF", "IS_NOT_ONE_OF"]
        if search_operator not in valid_operators:
            return f"Invalid search operator '{search_operator}'. Valid options are: {', '.join(valid_operators)}"

        if dataset_id:
            # Search within a specific dataset
            try:
                dataset = client.get_dataset_object(dataset_id)

                # Import SearchOperator enum
                from visual_layer_sdk.dataset import SearchOperator

                # Map string to SearchOperator enum
                operator_map = {
                    "IS": SearchOperator.IS,
                    "IS_NOT": SearchOperator.IS_NOT,
                    "IS_ONE_OF": SearchOperator.IS_ONE_OF,
                    "IS_NOT_ONE_OF": SearchOperator.IS_NOT_ONE_OF,
                }

                search_op = operator_map[search_operator]

                # Use the Searchable interface for label search
                searchable = dataset.search()

                # Handle single label vs multiple labels
                if isinstance(label_query, str):
                    labels = [label_query]
                else:
                    labels = label_query

                searchable = searchable.search_by_labels(
                    labels, search_operator=search_op
                )

                # Get the results
                results_df = searchable.get_results()

                if results_df.empty:
                    return f"No images found with label '{label_query}' using operator '{search_operator}' in dataset {dataset_id}"

                # Show all available columns in the results
                available_columns = list(results_df.columns)

                # Format the results - show all available data
                formatted_results = []
                for i, (idx, row) in enumerate(results_df.iterrows(), 1):
                    formatted_result = f"""
Result {i}:
"""
                    # Add all available columns
                    for col in available_columns:
                        value = row.get(col, "N/A")
                        # Truncate very long values for readability
                        if isinstance(value, str) and len(value) > 200:
                            value = value[:200] + "..."
                        formatted_result += f"{col}: {value}\n"

                    formatted_results.append(formatted_result)

                return (
                    f"Found {len(results_df)} images with label '{label_query}' using operator '{search_operator}' in dataset {dataset_id}.\n\nAvailable columns: {', '.join(available_columns)}\n\nResults:\n"
                    + "\n---\n".join(formatted_results)
                )

            except Exception as e:
                return f"Error searching dataset {dataset_id}: {str(e)}"
        else:
            # Search across all datasets
            datasets_df = client.get_all_datasets()
            datasets_list = datasets_df.to_dict("records")

            if not datasets_list:
                return "No datasets found to search through."

            # Search through datasets for matching labels
            matching_datasets = []
            for dataset in datasets_list:
                # Check various fields that might contain label information
                dataset_text = f"{dataset.get('name', '')} {dataset.get('description', '')} {dataset.get('type', '')}".lower()
                if label_query.lower() in dataset_text:
                    matching_datasets.append(dataset)

            if not matching_datasets:
                return f"No datasets found matching the label query: '{label_query}'"

            # Format the matching datasets
            formatted_results = []
            for i, dataset in enumerate(matching_datasets, 1):
                formatted_dataset = f"""
Dataset {i}:
ID: {dataset.get('id', 'N/A')}
Name: {dataset.get('name', 'N/A')}
Description: {dataset.get('description', 'No description available')}
Type: {dataset.get('type', 'N/A')}
Status: {dataset.get('status', 'N/A')}
"""
                formatted_results.append(formatted_dataset)

            return (
                f"Found {len(matching_datasets)} datasets matching '{label_query}':\n"
                + "\n---\n".join(formatted_results)
            )

    except Exception as e:
        return f"Error searching datasets by labels: {str(e)}"


def main():
    """Main entry point for the MCP server."""
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
