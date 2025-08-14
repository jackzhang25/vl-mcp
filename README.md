# Visual Layer MCP Server

A Model Context Protocol (MCP) server for Visual Layer SDK that provides tools for managing and searching datasets.

## Features

- **Dataset Management**: Get information about all available datasets
- **Health Monitoring**: Check the health status of the Visual Layer API
- **Dataset Details**: Retrieve detailed information about specific datasets
- **Label Search**: Search for images within datasets using various label operators

## Installation

### Prerequisites

- Python 3.8 or higher
- Visual Layer API credentials

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/visual-layer/vl-sdk.git
cd vl-sdk/mcp-server
```

2. Install the package:
```bash
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Set your Visual Layer API credentials as environment variables:

```bash
export VISUAL_LAYER_API_KEY="your_api_key"
export VISUAL_LAYER_API_SECRET="your_api_secret"
```

Or create a `.env` file in the project root:

```env
VISUAL_LAYER_API_KEY=your_api_key
VISUAL_LAYER_API_SECRET=your_api_secret
```

## Usage

### Running the MCP Server

```bash
python -m mcp_server.server
```

Or use the console script (after installation):

```bash
visual-layer-mcp
```

### MCP Configuration

Add the following to your MCP client configuration:

```json
{
    "mcpServers": {
        "visual-layer": {
            "command": "python",
            "args": ["-m", "mcp_server.server"],
            "env": {
                "VISUAL_LAYER_API_KEY": "${VISUAL_LAYER_API_KEY}",
                "VISUAL_LAYER_API_SECRET": "${VISUAL_LAYER_API_SECRET}"
            }
        }
    }
}
```

## Available Tools

### 1. get_all_datasets

Retrieves a list of all available datasets in Visual Layer.

**Returns**: Formatted list of datasets with ID, name, description, creation date, and status.

### 2. health_check

Checks the health status of the Visual Layer API.

**Returns**: API health status and confirmation message.

### 3. get_dataset_info

Gets detailed information about a specific dataset.

**Parameters**:
- `dataset_id` (str): The ID of the dataset to retrieve information about

**Returns**: Detailed dataset information including ID, name, description, creation date, status, type, and size.

### 4. search_by_labels

Searches for images within datasets using label criteria.

**Parameters**:
- `label_query` (str): The label or text to search for
- `dataset_id` (str, optional): Specific dataset ID to search within. If not provided, searches across all datasets
- `search_operator` (str, optional): Search operator to use. Options: "IS", "IS_NOT", "IS_ONE_OF", "IS_NOT_ONE_OF" (default: "IS_ONE_OF")

**Returns**: Search results with image details and available metadata.

## Development

### Setup Development Environment

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Linting

```bash
flake8 .
```

## Package Structure

```
mcp-server/
├── __init__.py          # Package initialization
├── server.py            # Main MCP server implementation
├── requirements.txt     # Runtime dependencies
├── setup.py            # Package setup script
├── pyproject.toml      # Modern Python packaging configuration
├── README.md           # This file
└── tests/              # Test files (if any)
```

## Dependencies

- **requests**: HTTP library for API calls
- **pathlib**: Path manipulation utilities
- **python-dotenv**: Environment variable management
- **PyJWT**: JWT token handling
- **pandas**: Data manipulation and analysis
- **mcp**: Model Context Protocol implementation

## License

MIT License - see the main repository for details.

## Support

For support and questions:
- Documentation: https://docs.visual-layer.com
- Issues: https://github.com/visual-layer/vl-sdk/issues
- Email: support@visual-layer.com 