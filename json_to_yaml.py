import json
import os

import yaml

# Load the COCO dataset
with open('Wider/COCO_train.json', 'r') as json_file:
    coco_data_train = json.load(json_file)
with open('Wider/COCO_val.json', 'r') as json_file:
    coco_data_val = json.load(json_file)

# Prepare the data for YOLOv5 YAML format
dataset = {
    'train': 'Wider/images/train',
    'val': 'Wider/images/val',
    'nc': len(coco_data_train['categories']),
    'names': [category['name'] for category in coco_data_train['categories']]
}

# Create a directory to store YOLO formatted labels
os.makedirs('Wider/labels/train', exist_ok=True)
os.makedirs('Wider/labels/val', exist_ok=True)


# Helper function to convert COCO bbox format to YOLO format
def coco_to_yolo_bbox(image_width, image_height, bbox):
    x_min, y_min, width, height = bbox
    x_center = x_min + width / 2
    y_center = y_min + height / 2
    # Normalize the values by image dimensions
    x_center /= image_width
    y_center /= image_height
    width /= image_width
    height /= image_height
    return [x_center, y_center, width, height]


# Parse image and annotation data and create YOLO annotation files
image_annotations_train = {image['id']: [] for image in coco_data_train['images']}
image_annotations_val = {image['id']: [] for image in coco_data_val['images']}

for annotation in coco_data_train['annotations']:
    image_id = annotation['image_id']
    image_data = next(image for image in coco_data_train['images'] if image['id'] == image_id)
    yolo_bbox = coco_to_yolo_bbox(image_data['width'], image_data['height'], annotation['bbox'])
    class_id = annotation['category_id'] - 1  # YOLO class indexing starts at 0
    image_annotations_train[image_id].append([class_id] + yolo_bbox)

for annotation in coco_data_val['annotations']:
    image_id = annotation['image_id']
    image_data = next(image for image in coco_data_val['images'] if image['id'] == image_id)
    yolo_bbox = coco_to_yolo_bbox(image_data['width'], image_data['height'], annotation['bbox'])
    class_id = annotation['category_id'] - 1  # YOLO class indexing starts at 0
    image_annotations_val[image_id].append([class_id] + yolo_bbox)

# Save YOLO label files
for image in coco_data_train['images']:
    image_id = image['id']
    image_name = os.path.splitext(image['file_name'])[0]

    # Extract the base file name without any directory structure
    base_image_name = os.path.basename(image_name)

    # Write annotations to a YOLO label file
    with open(f'Wider/labels/train/{base_image_name}.txt', 'w') as label_file:
        for annotation in image_annotations_train[image_id]:
            label_file.write(' '.join(map(str, annotation)) + '\n')

for image in coco_data_val['images']:
    image_id = image['id']
    image_name = os.path.splitext(image['file_name'])[0]

    # Extract the base file name without any directory structure
    base_image_name = os.path.basename(image_name)

    # Write annotations to a YOLO label file
    with open(f'Wider/labels/val/{base_image_name}.txt', 'w') as label_file:
        for annotation in image_annotations_val[image_id]:
            label_file.write(' '.join(map(str, annotation)) + '\n')

# Save the data to a YAML file
with open('Wider/COCO_train.yaml', 'w') as yaml_file:
    yaml.dump(dataset, yaml_file, default_flow_style=False)


print("Conversion to YOLOv5 format complete.")
