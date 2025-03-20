import os

def update_training_paths():
    training_dir = "trainingData"
    path_file = "trainingDataPath.txt"
    audio_paths = []

    # 遍历trainingData目录
    for root, _, files in os.walk(training_dir):
        for file in files:
            if file.endswith('.wav'):
                # 获取相对于trainingData的路径
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, training_dir)
                audio_paths.append(rel_path)

    # 将文件路径写入trainingDataPath.txt
    print(f"Writing paths to {path_file}")
    with open(path_file, 'w') as f:
        for path in sorted(audio_paths):
            f.write(f"{path}\n")

    print(f"Processing complete!")
    print(f"Total files found: {len(audio_paths)}")
    print(f"File paths have been written to {path_file}")

if __name__ == "__main__":
    update_training_paths() 