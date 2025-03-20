import os
import random

def collect_test_files(source_dir="trainingData/dev-clean", num_files_per_speaker=3):
    # 存储每个说话人的音频文件
    speaker_files = {}
    
    # 遍历音频文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.wav'):
                # 从文件名中提取说话人ID
                speaker = file.split('-')[0]
                if speaker not in speaker_files:
                    speaker_files[speaker] = []
                
                # 获取相对于trainingData的路径
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, "trainingData")
                speaker_files[speaker].append(rel_path)

    # 为每个说话人随机选择指定数量的文件
    selected_files = []
    for speaker, files in speaker_files.items():
        if files:  # 如果该说话人有文件
            num_files = min(num_files_per_speaker, len(files))  # 确保不超过可用文件数
            selected = random.sample(files, num_files)
            selected_files.extend(selected)

    # 写入文件
    with open("testSamplePath.txt", "w") as f:
        for file_path in selected_files:
            f.write(f"{file_path}\n")

    print(f"Selected {len(selected_files)} test files from {len(speaker_files)} speakers")
    print(f"Test file paths have been written to testSamplePath.txt")

if __name__ == "__main__":
    collect_test_files() 