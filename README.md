# p8n-importer

## Overview
`p8n-importer` is a versatile dataset import tool designed to simplify the process of importing various dataset formats into the PropulsionAI platform. This tool supports multiple formats, including VOC, YOLO, COCO, Image Classification, and Tabular data, and enables seamless integration with the PropulsionAI ecosystem. The tool now includes enhanced functionalities such as verbose logging and dataset visualization before uploading.

Explore more about PropulsionAI at [PropulsionHQ](https://propulsionhq.com).

## Features
- **Multiple Format Support**: Easily import datasets in formats like VOC, YOLO, COCO, Image Classification, and Tabular.
- **Direct Upload**: Upload datasets directly to the PropulsionAI platform with an easy-to-use command-line interface.
- **Flexibility**: Extendable to support additional dataset formats in the future.
- **Secure API Key Handling**: API keys are handled securely via environment variables or interactive input.
- **Verbose Logging**: Get detailed logs of the import process with the `--verbose` option.
- **Visualization**: Preview the dataset conversion result before uploading with the `--visualize` option.

## Installation
To install `p

8n-importer`, you need Python 3.x and pip installed on your system. You can install `p8n-importer` directly from PyPI:

```bash
pip install p8n-importer
```

## Usage

### Command-Line Interface
`p8n-importer` can be executed from the command line. Here’s how you can use it:

```bash
p8n-importer [format] [source_folder] [--verbose] [--no-upload] [--visualize]
```

- `[format]`: The format of your dataset (e.g., `voc`, `yolov8`, `coco_json`, `im_classification`, `tabular`).
- `[source_folder]`: Path to the source dataset folder.
- `--verbose` (optional): Enable verbose logging for detailed information during the import process.
- `--no-upload` (optional): Skip uploading the converted dataset to the platform.
- `--visualize` (optional): Visualize the dataset conversion result before uploading.

### Programmatic Use
`p8n-importer` also supports being used programmatically as shown in the example below:

```python
from P8nImporter import P8nImporter

importer = P8nImporter(
    api_key="YOUR_API_KEY",
    dataset_id="DATASET_ID",
)

image = "path/to/image.jpg"
annotation_path = "path/to/annotation.txt"

with open(annotation_path, "r") as f:
    annotation = f.read() # should be a string (multiline is supported)

label_names = ["label1", "label2"]

importer.import_task(
    format="yolov8",
    image=image,
    annotation=annotation,
    label_names=label_names,
)
```

### Supported Formats
The following table lists the formats currently supported by `p8n-importer`, along with their respective format codes:

| Format Code       | Format               | Input(s) | Action(s)                  | Description                                          |
|-------------------|----------------------|----------|----------------------------|------------------------------------------------------|
| voc               | VOC                  | Image    | Object Detection           | Visual                         |
| yolov8            | YOLOv8               | Image    | Object Detection           | You Only Look Once, version 8                        |
| coco_json         | COCO JSON            | Image    | Object Detection           | Common Objects in Context, JSON format               |
| im_classification | Image Classification | Image    | Classification             | Generic image classification datasets                |
| tabular           | Tabular              | Tabular  | Classification, Regression | Datasets in tabular formats like CSV, Excel, Parquet |

More formats are planned for future releases.

### Visualization Feature (Only supported on CLI)
When using the `--visualize` flag, you can preview how the dataset will look after conversion. This feature is particularly useful to verify annotations and dataset integrity before uploading it to the PropulsionAI platform.

### API Key and Dataset ID
The tool will prompt you for the API key and dataset ID. The API key can also be set as an environment variable `PROPULSIONAI_API_KEY`.

## Contributing
Contributions to `p8n-importer` are welcome! If you're looking to contribute, please read our [Contributing Guidelines](LINK_TO_CONTRIBUTING_GUIDELINES).

## License
`p8n-importer` is available under the MIT license. See the [LICENSE](LINK_TO_LICENSE) file for more info.

## Contact
For support or any questions, feel free to contact us at [info@propulsionhq.com](mailto:info@propulsionhq.com).