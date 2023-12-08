# p8n-importer

## Overview
`p8n-importer` is a versatile dataset import tool designed to simplify the process of importing various dataset formats into the PropulsionAI platform. This tool supports multiple formats, including VOC, YOLO, and Label Studio, and enables seamless integration with the PropulsionAI ecosystem. This tool now includes enhanced functionalities such as verbose logging and dataset visualization before uploading.

Explore more about PropulsionAI at [PropulsionHQ](https://propulsionhq.com).

## Features
- **Multiple Format Support**: Easily import datasets in formats like VOC, YOLO, and Label Studio.
- **Direct Upload**: Upload datasets directly to the PropulsionAI platform with an easy-to-use command-line interface.
- **Flexibility**: Extendable to support additional dataset formats in the future.
- **Secure API Key Handling**: API keys are handled securely via environment variables or interactive input.
- **Verbose Logging**: Get detailed logs of the import process with the `--verbose` option.
- **Visualization**: Preview the dataset conversion result before uploading with the `--visualize` option.

## Installation
To install `p8n-importer`, you need Python 3.x and pip installed on your system. You can install `p8n-importer` directly from PyPI:

```bash
pip install p8n-importer
```

## Usage
`p8n-importer` is designed to be user-friendly and can be executed from the command line. Here’s how you can use it:

```bash
p8n-importer [format] [source_folder] [--verbose] [--visualize]
```

- `[format]`: The format of your dataset (e.g., `voc`, `yolo`).
- `[source_folder]`: Path to the source dataset folder.
- `--verbose` (optional): Enable verbose logging for detailed information during the import process.
- `--visualize` (optional): Visualize the dataset conversion result before uploading.

### Visualization Feature
When using the --visualize flag, you can preview how the dataset will look after conversion. This feature is particularly useful to verify annotations and dataset integrity before uploading it to the PropulsionAI platform.

### API Key and Dataset ID
The tool will prompt you for the API key and dataset ID. The API key can also be set as an environment variable `PROPULSIONAI_API_KEY`.

## Supported Formats
Currently, `p8n-importer` supports the following formats:
- VOC (Visual Object Classes)
- YOLO (You Only Look Once)
- Label Studio

More formats are planned for future releases.

## Contributing
Contributions to `p8n-importer` are welcome! If you're looking to contribute, please read our [Contributing Guidelines](LINK_TO_CONTRIBUTING_GUIDELINES).

## License
`p8n-importer` is available under the MIT license. See the [LICENSE](LINK_TO_LICENSE) file for more info.

## Contact
For support or any questions, feel free to contact us at [info@propulsionhq.com](mailto:info@propulsionhq.com).