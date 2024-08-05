
# FAST - Todo App




## Run locally
1. Clone the project

```bash
  git clone https://link-to-project
```
'or'

Download Zip file

2. Go to the project directory

```bash
  cd my-project
```

3. Setup virtual environment 
```bash
python -m venv venv
```

4. Activate virtual environment 
(Windows)
```bash
venv\Scripts\activate.bat
```

(Mac)
```bash
source venv/bin/activate
```

5. Install requirements
```bash
pip install -r requirements.txt
```

6. Run App
```bash
uvicorn todo.main:app --reload
```
- Default url: http://127.0.0.1:8000
- API documentation:  http://127.0.0.1:8000/docs


## Running Tests

To run tests, run the following command in main directory of project

```bash
  pytest
```

