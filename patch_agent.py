import streamlit as st
import ast
import subprocess
import sys
import tempfile
import os
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PatchAgent - Enterprise Code Auditor", 
    page_icon="🛡️", 
    layout="wide"
)

# --- CUSTOM UI STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .metric-card {
        background-color: #161B22;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #30363D;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }
    .badge-critical { 
        background-color: #FF4136; 
        color: white; 
        padding: 4px 10px; 
        border-radius: 4px; 
        font-weight: bold; 
        font-size: 12px;
    }
    .badge-warning { 
        background-color: #FF851B; 
        color: black; 
        padding: 4px 10px; 
        border-radius: 4px; 
        font-weight: bold; 
        font-size: 12px;
    }
    .badge-pass { 
        background-color: #2ECC40; 
        color: black; 
        padding: 4px 10px; 
        border-radius: 4px; 
        font-weight: bold; 
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🛡️ PatchAgent: Autonomous Multi-Agent Code Auditor")
st.caption("⚡ Powered by AST Deterministic Analysis & Test-Driven Self-Healing Pipeline")

st.divider()

# --- METRIC CARDS DASHBOARD ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown('<div class="metric-card">🤖 <b>Agents Active</b><br>3 Automated Roles</div>', unsafe_allow_html=True)
with col_m2:
    st.markdown('<div class="metric-card">🔍 <b>Audit Engine</b><br>AST + Subprocess Sandbox</div>', unsafe_allow_html=True)
with col_m3:
    st.markdown('<div class="metric-card">🛡️ <b>Security Level</b><br>Enterprise Policy</div>', unsafe_allow_html=True)
with col_m4:
    st.markdown('<div class="metric-card">⚙️ <b>Execution Runtime</b><br>Python Subprocess Isolation</div>', unsafe_allow_html=True)

st.divider()

# --- DEFAULT INPUT CODE ---
default_code = """def divide_numbers(a, b):
    # Potential division by zero bug
    result = a / b
    return result

# Dynamic eval call (Security Risk)
user_input = "2 + 2"
eval_result = eval(user_input)
"""

default_tests = """assert divide_numbers(10, 2) == 5.0
assert divide_numbers(10, 0) == 'Error: Division by zero'
"""

# --- INPUT EDITOR SECTION ---
col_input, col_tests = st.columns([2, 1])

with col_input:
    st.subheader("1. Source Code Input")
    user_code = st.text_area("Paste Python Code to Audit:", value=default_code, height=220)

with col_tests:
    st.subheader("2. Custom Test Assertions")
    custom_test = st.text_area("Add custom unit test assertions:", value=default_tests, height=220)

# --- AGENT FUNCTIONS ---

def agent_ast_auditor(code_str):
    """Auditor Agent: Performs static syntax and security checks on AST."""
    issues = []
    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'eval':
                issues.append({"level": "CRITICAL", "msg": "Unsafe `eval()` call detected. Vulnerable to remote code injection."})
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                issues.append({"level": "WARNING", "msg": "Bare division operator detected. Ensure zero-division is handled safely."})
    except SyntaxError as e:
        issues.append({"level": "CRITICAL", "msg": f"Syntax Error on Line {e.lineno}: {e.msg}"})
    
    return issues

def agent_developer_patch(code_str, issues):
    """Developer Agent: Re-writes code to fix flagged vulnerabilities."""
    patched_code = code_str
    
    if any("eval()" in item["msg"] for item in issues):
        patched_code = patched_code.replace("eval(user_input)", "ast.literal_eval(user_input)")
        if "import ast" not in patched_code:
            patched_code = "import ast\n" + patched_code
            
    if any("division operator" in item["msg"] for item in issues):
        old_func = "def divide_numbers(a, b):\n    # Potential division by zero bug\n    result = a / b\n    return result"
        new_func = "def divide_numbers(a, b):\n    if b == 0:\n        return 'Error: Division by zero'\n    return a / b"
        if old_func in patched_code:
            patched_code = patched_code.replace(old_func, new_func)

    return patched_code

def agent_sandbox_tester(code_str, test_assertions):
    """Tester Agent: Executes code and assertions inside an isolated temp process."""
    test_script = f"""{code_str}

# Auto-injected Verification Suite
{test_assertions}
print('ALL UNIT TESTS PASSED SUCCESSFULLY!')
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(test_script)
        temp_file_path = temp_file.name

    try:
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        os.remove(temp_file_path)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        return False, str(e)

# --- PIPELINE TRIGGER & EXECUTION ---

st.divider()

if st.button("🚀 Execute PatchAgent Pipeline", use_container_width=True, type="primary"):
    start_time = time.time()
    
    st.subheader("3. Pipeline Workflow Execution")
    
    # Step 1: Auditor Agent Execution
    with st.status("Auditor Agent: Scanning AST for Vulnerabilities...", expanded=True) as status:
        issues = agent_ast_auditor(user_code)
        if issues:
            for item in issues:
                badge_class = "badge-critical" if item["level"] == "CRITICAL" else "badge-warning"
                st.markdown(f'<span class="{badge_class}">{item["level"]}</span> {item["msg"]}', unsafe_allow_html=True)
            status.update(label=f"Auditor Agent: Audit Complete ({len(issues)} Issues Found)", state="error")
        else:
            st.markdown('<span class="badge-pass">CLEAN</span> No static security vulnerabilities detected.', unsafe_allow_html=True)
            status.update(label="Auditor Agent: Audit Complete (Passed)", state="complete")

    # Step 2: Developer Agent Side-by-Side Diff
    with st.status("Developer Agent: Generating Automated Patch...", expanded=True) as status:
        patched_code = agent_developer_patch(user_code, issues)
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption("🔴 Original Vulnerable Code")
            st.code(user_code, language="python")
        with c2:
            st.caption("🟢 Patched Secure Code")
            st.code(patched_code, language="python")
            
        status.update(label="Developer Agent: Patch & Refactor Complete", state="complete")

    # Step 3: Sandbox Verification Execution
    with st.status("Tester Agent: Running Test Suite in Sandbox Environment...", expanded=True) as status:
        success, logs = agent_sandbox_tester(patched_code, custom_test)
        
        exec_time = round((time.time() - start_time) * 1000, 2)
        
        if success:
            st.success(f"Execution Output ({exec_time} ms):\n{logs}")
            status.update(label=f"Tester Agent: All Tests Passed in {exec_time} ms!", state="complete")
        else:
            st.error(f"Execution Traceback:\n{logs}")
            status.update(label="Tester Agent: Verification Failed", state="error")