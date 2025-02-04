import os
import json
import matplotlib.pyplot as plt
import numpy as np

# 1. ตั้งค่าโฟลเดอร์ที่มีไฟล์ JSON
folder_path = 'tesseract_ocr_report'  # เปลี่ยนเป็น path ของคุณ
file_names = []
cer_values = []
add_counts = []
delete_counts = []
ocr_lengths = []
ground_truth_lengths = []

# 2. อ่านไฟล์ทั้งหมดในโฟลเดอร์
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):  # ตรวจสอบเฉพาะไฟล์ .json
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # โหลดข้อมูล JSON
            
            # 3. ดึงค่าที่ต้องการจาก JSON
            file_names.append(file_name)
            cer_values.append(data[0]['CER Value'])
            add_counts.append(len(data[0]['add']))  # ตัวอักษรที่เพิ่ม
            delete_counts.append(len(data[0]['delete']))  # ตัวอักษรที่ลบ
            ocr_lengths.append(len(data[0]['tesseract_wrong']))  # ความยาวข้อความ OCR
            ground_truth_lengths.append(len(data[0]['answer']))  # ความยาวข้อความจริง

# 4. สร้างรูปแบบหลายกราฟในหน้าเดียว
fig, axs = plt.subplots(3, 1, figsize=(10, 15))  # 3 แถว 1 คอลัมน์
fig.tight_layout(pad=6.0)

# 5. Plot กราฟ CER
axs[0].bar(file_names, cer_values, color='orange', alpha=0.7)
axs[0].set_title('Character Error Rate (CER)')
axs[0].set_ylabel('CER Value')
axs[0].set_xlabel('File Name')
axs[0].tick_params(axis='x', rotation=45)
axs[0].grid(axis='y', linestyle='--', alpha=0.7)

# 6. Plot กราฟคำที่เพิ่ม/ลบ
x = np.arange(len(file_names))  # ตำแหน่งแกน X
width = 0.35  # ความกว้างของกราฟ
axs[1].bar(x - width/2, add_counts, width, label='Add', color='green', alpha=0.7)
axs[1].bar(x + width/2, delete_counts, width, label='Delete', color='red', alpha=0.7)
axs[1].set_xticks(x)
axs[1].set_xticklabels(file_names, rotation=45, ha='right')
axs[1].set_title('Number of Added and Deleted Characters')
axs[1].set_ylabel('Count')
axs[1].set_xlabel('File Name')
axs[1].legend()
axs[1].grid(axis='y', linestyle='--', alpha=0.7)

# 7. Plot กราฟความยาวข้อความ OCR vs Ground Truth
axs[2].plot(file_names, ocr_lengths, label='OCR Length', marker='o', color='blue')
axs[2].plot(file_names, ground_truth_lengths, label='Ground Truth Length', marker='o', color='purple')
axs[2].set_title('Comparison of Text Lengths')
axs[2].set_ylabel('Length of Text')
axs[2].set_xlabel('File Name')
axs[2].tick_params(axis='x', rotation=45)
axs[2].legend()
axs[2].grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

print("file_names:", file_names)
print("cer_values:", cer_values)
print("add_counts:", add_counts)
print("delete_counts:", delete_counts)
print("ocr_lengths:", ocr_lengths)
print("ground_truth_lengths:", ground_truth_lengths)

average = sum(cer_values) / len(cer_values)
print(f"ค่าเฉลี่ยของ cer_values คือ: {average:.6f}")

std_dev = np.std(cer_values)
print(f"ส่วนเบี่ยงเบนมาตรฐานของ cer_values คือ: {std_dev:.6f}")



# # Plot histogram
# plt.hist(cer_values, bins=10, edgecolor='black')
# plt.title("Distribution of cer_values")
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# plt.show()

