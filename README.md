# <p align="center">**Parkinson Disease Detection**
###### <p align='center'>*Transforming Diagnosis, Empowring Life with Precision*

<p align = 'center'><img alt="Static Badge" src="https://img.shields.io/badge/90%25-Python-blue"> <img alt="Static Badge" src="https://img.shields.io/badge/language-12-blue">
(https://img.shields.io/github/license/dipenmrana99/ParkinsonDiseaseDetection)
(https://img.shields.io/github/stars/dipenmrana99/ParkinsonDiseaseDetection?style=social)

<p align="center">
  <img src="assets/overview.gif" width="600"/>
</p>

### 🚀 What is ParkinsonDiseaseDetection?
ParkinsonDiseaseDetection is a Python-based ML project for detecting Parkinson’s Disease using audio/motion datasets.

**Highlights:**
- ✅ Multiple classification models: Random Forest, SVM, KNN, XGBoost...
- 🎯 Uses UCI Parkinson’s dataset
- 📈 Includes EDA, preprocessing, balancing, model comparison
- 🌐 Optional: Flask web app for live detection (if applicable)

### 🛠️ Installation
```bash
git clone https://github.com/dipenmrana99/ParkinsonDiseaseDetection.git
cd ParkinsonDiseaseDetection
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app_knn.py
```

---

### 5. **Model Metrics & Comparison Table**
Add a table summarizing model performance:
| Model                | Accuracy | F1 Score | Notes           |
|----------------------|----------|----------|-----------------|
| Random Forest        | 99.6%    | 0.96     | Best overall    |
| SVM                  | 98.0%    | 0.94     | Lightweight     |
| KNN                  | 96.5%    | 0.92     | Good baseline   |

Explain why RF may overfit vs simpler models.

---

### 6. **Dataset Info with Links**
```md
## 📂 Dataset
- Source: [UCI Machine Learning Repository – Parkinson’s dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data)
- Description: 23 voice measurements from 197 instances
```

#### ScreenShots:
---
User Dashboard
![user_dashboard](https://github.com/user-attachments/assets/ac3bc1d2-1dfb-43cb-86c7-1eec50c8cedd)

Admin Dashboard
![admin_dashboard](https://github.com/user-attachments/assets/5c75dab6-874f-4e54-b78f-2416d402310b)


