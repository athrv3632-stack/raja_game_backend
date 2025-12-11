# Raja-Mantri-Chor-Sipahi Game Backend  
Backend implementation for the classic **Raja–Mantri–Chor–Sipahi** guessing game, built as part of the CodeChef-VIT Recruitment Task.

---

## 🎯 Overview  
This project provides a simple REST API that simulates the traditional Indian role-assignment game.  
Players join a room → roles are assigned → Mantri tries to guess the Chor → points are awarded accordingly → leaderboard updates automatically.

---

## 🚀 Features  
- Room creation  
- Player joining  
- Random role assignment (Raja, Mantri, Sipahi, Chor)  
- Scoring system  
- Guess submissions  
- Leaderboard generation  
- Persistent storage in `storage.json`  
- Built completely using **Python + Flask**

---

## 🛠 Tech Stack  
- **Python 3.9+**  
- **Flask** (API framework)  
- **JSON file storage** for simplicity  
- No database required  

---

## 📁 Project Structure  
├── app.py              # Main Flask server
├── storage.json        # Local storage for players & rounds
├── requirements.txt    # Dependencies
├── .gitignore
└── README.md
## 🔧 Setup Instructions (Local)

### 1. Clone the repository
git clone https://github.com/athrv3632-stack/raja_game_backend.git
cd raja_game_backend

### 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the server
python app.py
