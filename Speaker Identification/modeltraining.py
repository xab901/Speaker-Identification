import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture 
from featureextraction import extract_features
import warnings
import os
from tqdm import tqdm
warnings.filterwarnings("ignore")

#path to training data
source = "trainingData"   
dest = "Speakers_models"

# Create directories if they don't exist
os.makedirs(source, exist_ok=True)
os.makedirs(dest, exist_ok=True)

train_file = "trainingDataPath.txt"        
file_paths = open(train_file,'r')

# 按说话人组织音频文件
speaker_files = {}
for path in file_paths:    
    path = path.strip()
    # 从文件名中提取说话人ID（第一个连字符前的数字）
    filename = os.path.basename(path)  # 获取文件名
    speaker = filename.split('-')[0]   # 提取说话人ID
    if speaker not in speaker_files:
        speaker_files[speaker] = []
    speaker_files[speaker].append(path)

print(f"Found {len(speaker_files)} speakers")

# 为每个说话人训练模型
for speaker, files in tqdm(speaker_files.items(), desc="Training speakers"):
    print(f"\nProcessing speaker: {speaker}")
    print(f"Number of files: {len(files)}")
    
    features = np.asarray(())
    
    # 处理该说话人的所有文件
    for path in tqdm(files, desc=f"Processing {speaker}'s files", leave=False):
        try:
            # 读取音频文件
            audio_path = os.path.join(source, path)
            sr, audio = read(audio_path)
            
            # 提取特征
            vector = extract_features(audio, sr)
            
            # 添加到特征集
            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
                
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")
            continue
    
    # 如果成功提取了特征，训练模型
    if features.size > 0:
        try:
            print(f"Training model for speaker {speaker} with {features.shape[0]} samples...")
            
            # 调整GMM参数以加快训练速度
            gmm = GaussianMixture(
                n_components=8,  # 减少组件数量
                max_iter=100,    # 减少最大迭代次数
                covariance_type='diag',
                n_init=1,        # 减少初始化次数
                random_state=0   # 固定随机种子
            )
            gmm.fit(features)
            
            # 保存模型
            model_path = os.path.join(dest, f"{speaker}.gmm")
            with open(model_path, 'wb') as f:
                pickle.dump(gmm, f)
            print(f"Model saved to {model_path}")
            
        except Exception as e:
            print(f"Error training model for speaker {speaker}: {str(e)}")
    else:
        print(f"No valid features extracted for speaker {speaker}")

print("\nTraining completed!")
print(f"Models have been saved to {dest}")
