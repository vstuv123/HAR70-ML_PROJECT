<<<<<<< HEAD
# HAR70+ Activity Recognition — Streamlit App

Interactive web application for Human Activity Recognition using the HAR70+ wearable sensor dataset.

## Quick Start

### 1. Link your trained model files
Copy your `.pkl` files into the `models/` folder:
```
har70_app/
└── models/
    ├── random_forest.pkl   ← trained Random Forest model
    ├── svm_linear.pkl      ← trained SVM (Linear) model
    └── har_scaler.pkl      ← StandardScaler from preprocessing
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
cd har70_app
streamlit run app.py
```

---

## Features

| Page | Description |
|------|-------------|
| 🏠 Home | Dataset overview, model status, pipeline summary |
| 🎛️ Manual Input | Enter sensor values via sliders or number fields, get instant prediction with probability chart |
| 📂 Batch Upload | Upload a CSV of raw sensor data, predict activity for every window, download results |
| ℹ️ About | Architecture docs, model comparison, deployment guide |

## Project Structure

```
har70_app/
├── app.py                     ← Entry point
├── requirements.txt
├── models/                    ← Place .pkl files here
│   ├── random_forest.pkl
│   ├── svm_linear.pkl
│   └── har_scaler.pkl
├── pages_src/
│   ├── home.py
│   ├── manual_input.py
│   ├── batch_upload.py
│   └── about.py
└── utils/
    ├── model_loader.py        ← pkl loading with caching
    ├── feature_extractor.py   ← 60-feature extraction
    ├── predictor.py           ← prediction + chart rendering
    └── styles.py              ← custom CSS
```

## Deploy to Streamlit Community Cloud

1. Push this folder to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New App → set main file to `har70_app/app.py`
4. Commit your `models/` folder to the repo (if files < 100 MB)
=======
# HAR70-ML_PROJECT
>>>>>>> b124034f6c9b598ba3cb2225fdfc8dd460f6d7cf
