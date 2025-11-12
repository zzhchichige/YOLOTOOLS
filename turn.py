import os
import xml.etree.ElementTree as ET

# 这里填写你的类别顺序
classes = ["jinx"]  # 如果有多个类别，按顺序加进去

# VOC XML 文件夹
xml_dir = r"D:/yolocode/dataset5/labels"
# YOLO txt 输出文件夹
yolo_dir = r"D:/yolocode/dataset5/labels/train"
os.makedirs(yolo_dir, exist_ok=True)

# ---------------- 批量转换 XML -> YOLO txt ----------------
for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(xml_dir, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    yolo_lines = []

    for obj in root.findall("object"):
        cls_name = obj.find("name").text
        if cls_name not in classes:
            continue
        cls_id = classes.index(cls_name)

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        # 检查坐标合理性
        if xmax < xmin:
            xmin, xmax = xmax, xmin
        if ymax < ymin:
            ymin, ymax = ymax, ymin

        x_center = (xmin + xmax) / 2 / img_width
        y_center = (ymin + ymax) / 2 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # 保存 YOLO txt
    yolo_file = os.path.join(yolo_dir, xml_file.replace(".xml", ".txt"))
    with open(yolo_file, "w") as f:
        f.write("\n".join(yolo_lines))

print("批量转换完成！")

# ---------------- 自动生成 classes.txt ----------------
classes_file = os.path.join(yolo_dir, "classes.txt")
with open(classes_file, "w") as f:
    for cls in classes:
        f.write(cls + "\n")

print(f"classes.txt 已生成: {classes_file}")
