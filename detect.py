from ultralytics import YOLO

MODEL_PATH = "my_model.pt"

model = YOLO(MODEL_PATH)

image_path = input("Enter image name or path: ").strip()

results = model(image_path, conf=0.1, imgsz=1280)

output = {
    "image": image_path,
    "total_objects": 0,
    "objects": {},
    "details": []
}

for r in results:
    img_h, img_w = r.orig_shape
    img_area = img_h * img_w

    for box in r.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        # temporary correction
        if label == "tool":
            label = "table"

        x1, y1, x2, y2 = box.xyxy[0].tolist()
        width = x2 - x1
        height = y2 - y1
        area = width * height
        ratio = area / img_area

        if ratio < 0.01:
            size = "small"
        elif ratio < 0.04:
            size = "medium"
        else:
            size = "big"

        material = "unknown"

        output["objects"][label] = output["objects"].get(label, 0) + 1
        output["total_objects"] += 1

        output["details"].append({
            "type": label,
            "material": material,
            "size": size
        })

print("\n=== RESULT ===")
print(f"Image: {output['image']}")
print(f"Total Objects: {output['total_objects']}")

print("\nObject Summary:")
for obj, count in output["objects"].items():
    print(f"  - {obj}: {count}")

print("\nDetails:")
for i, item in enumerate(output["details"], 1):
    print(f"  {i}. Type: {item['type']}")
    print(f"     Size: {item['size']}")