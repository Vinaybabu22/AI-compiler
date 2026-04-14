import os
import subprocess
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import CodeHistory
from . import db

compiler = Blueprint('compiler', __name__)

# --- PORTABLE COMPILER PATHS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GCC_PATH = os.path.join(BASE_DIR, 'compilers', 'mingw64', 'bin', 'gcc.exe')
JAVAC_PATH = os.path.join(BASE_DIR, 'compilers', 'jdk-21', 'bin', 'javac.exe')
JAVA_PATH = os.path.join(BASE_DIR, 'compilers', 'jdk-21', 'bin', 'java.exe')

def get_ai_client():
    """Initializes and returns the Mistral API Client."""
    from mistralai.client import Mistral
    # Ensure MISTRAL_API_KEY is defined in your .env file
    api_key = os.getenv("MISTRAL_API_KEY")
    return Mistral(api_key=api_key)

@compiler.route('/')
def index():
    load_id = request.args.get('load')
    saved_code = "" 
    if load_id:
        code_entry = CodeHistory.query.get(load_id)
        if code_entry:
            saved_code = code_entry.content
    return render_template('compiler.html', saved_code=saved_code)

@compiler.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code, lang = data.get('code'), data.get('language')
    output = ""
    
    # 1. RUN CODE LOGIC
    try:
        if lang == 'python':
            result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=5)
            output = result.stdout if result.returncode == 0 else result.stderr
        elif lang == 'c':
            with open('test.c', 'w') as f: f.write(code)
            comp = subprocess.run([GCC_PATH, 'test.c', '-o', 'out.exe'], capture_output=True, text=True)
            if comp.returncode != 0: 
                output = comp.stderr
            else:
                res = subprocess.run(['out.exe'], capture_output=True, text=True, timeout=5)
                output = res.stdout if res.returncode == 0 else res.stderr
        elif lang == 'java':
            with open('Main.java', 'w') as f: f.write(code)
            comp = subprocess.run([JAVAC_PATH, 'Main.java'], capture_output=True, text=True)
            if comp.returncode != 0: 
                output = comp.stderr
            else:
                res = subprocess.run([JAVA_PATH, 'Main'], capture_output=True, text=True, timeout=5)
                output = res.stdout if res.returncode == 0 else res.stderr
    except Exception as e:
        output = str(e)

    # 2. AI ASSISTANT LOGIC
    ai_help = ""
    try:
        client = get_ai_client() 
    
        prompt = (
            f"Analyze this {lang} code. Provide the following in your response:\n"
            f"1. A 2-sentence logic explanation.\n"
            f"2. Time and Space Complexity (Big O notation).\n"
            f"3. If the code is inefficient, provide an optimized snippet.\n"
            f"4. If there is a compiler error, explain the fix. If there are no errors, simply state 'No errors found.' Do NOT provide formatting, structural, or stylistic advice (like suggesting __main__ blocks).\n"
            f"CODE:\n{code}\nOUTPUT:\n{output}"
        )

        # Using Mistral API
        ai_response = client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": "You are an expert programming assistant that helps developers analyze and debug their code."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_help = ai_response.choices[0].message.content

    except Exception as e:
        print(f"Mistral Error: {e}")
        ai_help = "The AI Assistant is currently unavailable. Please try again in a moment."

    return jsonify({"output": output, "ai_help": ai_help})


@compiler.route('/save', methods=['POST'])
@login_required
def save_code():
    data = request.json
    new_code = CodeHistory(
        filename=data.get('filename'),
        content=data.get('code'),
        language=data.get('language'),
        user_id=current_user.id
    )
    db.session.add(new_code)
    db.session.commit()
    return jsonify({"message": "Code saved successfully!"})

@compiler.route('/history')
@login_required
def history():
    # Fetch all saved codes for the logged-in user
    user_codes = CodeHistory.query.filter_by(user_id=current_user.id).order_by(CodeHistory.timestamp.desc()).all()
    return render_template('history.html', codes=user_codes)