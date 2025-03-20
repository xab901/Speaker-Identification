import os
import shutil
from glob import glob

# 源目录和目标目录
source_dir = "LibriSpeech"
target_dir = "trainingData"
path_file = "trainingDataPath.txt"

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 用于存储所有音频文件的相对路径
audio_paths = []

# 遍历LibriSpeech目录
for speaker_dir in os.listdir(source_dir):
    speaker_path = os.path.join(source_dir, speaker_dir)
    if not os.path.isdir(speaker_path):
        continue
        
    print(f"Processing speaker: {speaker_dir}")
    
    # 在trainingData中创建说话人目录
    target_speaker_dir = os.path.join(target_dir, speaker_dir)
    os.makedirs(target_speaker_dir, exist_ok=True)
    
    # 查找所有flac文件
    for root, dirs, files in os.walk(speaker_path):
        for file in files:
            if file.endswith('.flac'):
                # 源文件路径
                src_file = os.path.join(root, file)
                
                # 目标文件路径（转换为wav）
                wav_file = os.path.splitext(file)[0] + '.wav'
                dst_file = os.path.join(target_speaker_dir, wav_file)
                
                # 使用ffmpeg转换格式
                print(f"Converting {src_file} to {dst_file}")
                os.system(f'ffmpeg -i "{src_file}" -acodec pcm_s16le -ar 16000 "{dst_file}" -y -loglevel error')
                
                # 存储相对路径
                rel_path = os.path.join(speaker_dir, wav_file)
                audio_paths.append(rel_path)

# 将文件路径写入trainingDataPath.txt
print(f"\nWriting paths to {path_file}")
with open(path_file, 'w') as f:
    for path in sorted(audio_paths):
        f.write(f"{path}\n")

print(f"\nProcessing complete!")
print(f"Total files processed: {len(audio_paths)}")
print(f"Files have been converted and copied to {target_dir}")
print(f"File paths have been written to {path_file}") 