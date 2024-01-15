from ..formats import COCOImporter, VOCImporter, YOLOv8Importer, ImageClassificationImporter, TabularImporter

def setup_importer(format, source_folder, output_folder):
    if format == "coco_json":
        return COCOImporter(source_folder, output_folder)
    elif format == "voc":
        return VOCImporter(source_folder, output_folder)
    elif format == "yolov8":
        return YOLOv8Importer(source_folder, output_folder)
    elif format == "image_classification":
        return ImageClassificationImporter(source_folder, output_folder)
    elif format == "tabular":
        return TabularImporter(source_folder, output_folder)
    else:
        raise ValueError("Format not supported")