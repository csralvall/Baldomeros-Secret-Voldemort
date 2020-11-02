# Baldomeros-Secret-Voldemort

# Development

## First of all

```bash
git clone https://github.com/csralvall/Baldomeros-Secret-Voldemort.git
```

## To run the Back-End server

### For the first time

```bash
cd Baldomeros-Secret-Voldemort/server/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### From now on

```bash
cd server/
source venv/bin/activate
cd Baldomeros-Secret-Voldemort/
uvicorn server.main:app --host 0.0.0.0 --reload
```

### For testing

```bash
cd server/
source venv/bin/activate 
cd Baldomeros-Secret-Voldemort/
pytest 
```

## To run the Front-End server

### For the first time

```bash
sudo apt update
sudo apt install nodejs
sudo apt install npm
sudo npm install -g npm@latest
cd Baldomeros-Secret-Voldemort/app/
sudo npm install
```

### From now on

```bash
sudo npm start
```
Then, open `http://localhost:3000/` on your browser

### For testing

```bash
cd Baldomeros-Secret-Voldemort/app/
sudo npm run test
```
