# 🔍 Semantic Search Engine

A powerful hybrid search engine that combines traditional keyword-based search with AI-driven semantic search. This project leverages **Elasticsearch** and **TensorFlow** to deliver highly relevant search results.

---

## 🌟 Features

✅ **Hybrid Search:**
   - **Keyword Search:** Uses Elasticsearch’s TF-IDF scoring.
   - **Semantic Search:** Employs Universal Sentence Encoder (USE) embeddings.
   - **Ranked Results:** Combines keyword and semantic relevance for optimal ranking.

✅ **Scalable Data Processing:**
   - Efficient indexing for **200,000+** questions.
   - **Bulk operations** for Elasticsearch indexing.

✅ **Modern Technology Stack:**
   - **Elasticsearch 7.7** for scalable search.
   - **TensorFlow Hub** for AI-powered embeddings.
   - **Flask Web Interface** for user-friendly search.

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-7.7-005571?logo=elasticsearch)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-2.0-000000?logo=flask)

---

## 🚀 Quick Start

### 🔧 Prerequisites

- Python **3.8+**
- Docker Desktop
- **8GB RAM** (recommended)

### 📥 Installation

#### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/semantic-search-engine.git
cd semantic-search-engine
```

#### 2️⃣ Set Up Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Start Elasticsearch Container
```bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name es-container elasticsearch:7.7.0
```

#### 5️⃣ Verify Elasticsearch Setup
```bash
curl -X GET "localhost:9200/_cat/indices?v"
```

---

## 📂 Data Pipeline

#### 🏗 Preprocess Data
```bash
python scripts/clean_data.py
```

#### 📊 Create Elasticsearch Index
```bash
python scripts/create_index.py
```

#### 📌 Index Questions
```bash
python scripts/index_data.py
```

---

## 🖥 Run Web Interface
```bash
export FLASK_APP=scripts/searchES_FlaskAPI.py
flask run --host=0.0.0.0 --port=5000
```
🔗 Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 📂 Project Structure
```
semantic-search-engine/
├── data/               # Dataset storage
│   ├── raw/            # Original StackOverflow CSVs
│   ├── processed/      # Cleaned datasets
│   └── models/         # TensorFlow Hub models
├── scripts/
│   ├── create_index.py # ES schema configuration
│   ├── index_data.py   # Embedding generation & indexing
│   └── searchES_FlaskAPI.py # Web interface logic
├── templates/          # Jinja2 templates
│   ├── index.html      # Search interface
│   └── results.html    # Results display
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## 🚨 Troubleshooting

### ❌ Elasticsearch Connection Failures
```bash
# Check running containers
docker ps -a

# View container logs
docker logs es-container
```

### ❌ TensorFlow Compatibility Issues
```bash
# Remove conflicting installations
pip uninstall tensorflow tensorflow-hub

# Install correct versions
pip install tensorflow==2.6.0 tensorflow-hub==0.12.0
```

### ❌ Missing Templates
- Ensure `templates/` folder is correctly named.
- Check Flask’s `template_folder` path configuration.

---

## 📈 Future Roadmap

🚀 Add **search filters** (date range, score threshold)  
📜 Implement **pagination** for results  
🔐 User **authentication system**  
📊 **Query analytics** dashboard  
📦 Full **Docker Compose** setup  

---

## 📜 License
**MIT License** - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Google Research** for Universal Sentence Encoder
- **Elasticsearch** for scalable search
- **Stack Overflow Dataset** for sample questions

---

🚀 *Happy Searching!* 🔍

