import os
import pickle
import numpy as np
from scipy.io.wavfile import read
from featureextraction import extract_features
#from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time

"""
#path to training data
source   = "development_set/"   
modelpath = "speaker_models/"
test_file = "development_set_test.txt"        
file_paths = open(test_file,'r')

"""
#path to training data
source = "SampleData"   

#path where training speakers will be saved
modelpath = "Speakers_models"

gmm_files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]

#Load the Gaussian gender Models
models    = {}
speakers   = []

print("Loading models...")
for fname in gmm_files:
    try:
        speaker = os.path.splitext(os.path.basename(fname))[0]
        with open(fname, 'rb') as f:
            models[speaker] = pickle.load(f)
            speakers.append(speaker)
        print(f"Loaded model for speaker: {speaker}")
    except Exception as e:
        print(f"Error loading model {fname}: {str(e)}")

print("\nTesting all files in SampleData directory...")
total_tests = 0
correct_predictions = 0

# 测试SampleData目录中的所有音频文件
for file in os.listdir(source):
    if file.endswith('.wav'):
        path = file
        print(f"\nTesting audio: {path}")
        
        try:
            # 从文件名中提取实际说话人ID
            actual_speaker = file.split('-')[0]
            
            # 读取音频文件
            audio_path = os.path.join(source, path)
            sr, audio = read(audio_path)
            vector = extract_features(audio, sr)
            
            # 对每个模型计算得分
            scores = {}
            for speaker, gmm in models.items():
                scores[speaker] = np.sum(gmm.score(vector))
            
            # 找出得分最高的说话人
            predicted_speaker = max(scores.items(), key=lambda x: x[1])[0]
            
            # 更新统计
            total_tests += 1
            if actual_speaker == predicted_speaker:
                correct_predictions += 1
            
            # 输出结果
            print(f"Actual Speaker    : {actual_speaker}")
            print(f"Predicted Speaker : {predicted_speaker}")
            print(f"Result           : {'Correct!' if actual_speaker == predicted_speaker else 'Wrong!'}")
            
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")

# 输出最终统计
if total_tests > 0:
    accuracy = (correct_predictions / total_tests) * 100
    print(f"\nTotal tests: {total_tests}")
    print(f"Correct predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.2f}%")
else:
    print("\nNo tests were performed successfully.")

print("\nSpeaker identification completed successfully!")
