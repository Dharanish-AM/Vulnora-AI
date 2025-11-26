import streamlit as st
import os
import time
import pandas as pd
from vulnora.core.scanner import ProjectScanner

st.set_page_config(
    page_title="Vulnora AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main {
        background: #0e1117;
    }
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
    }
    .stButton>button {
        background-color: #6366f1;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #4f46e5;
    }
    .metric-card {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🛡️ Vulnora AI")
    st.markdown("### AI-Powered Code Security Scanner")

    with st.sidebar:
        st.header("Configuration")
        project_path = st.text_input("Project Path", placeholder="/path/to/your/project")
        
        model = st.selectbox(
            "LLM Model",
            ["llama3.1:8b", "llama3", "mistral", "gemma"],
            index=0
        )
        
        scan_button = st.button("Start Scan", type="primary")
        
        st.markdown("---")
        st.markdown("### About")
        st.info("Vulnora AI uses local LLMs and static analysis to find vulnerabilities in your code.")

    if scan_button and project_path:
        if not os.path.exists(project_path):
            st.error(f"Path does not exist: {project_path}")
            return

        with st.spinner(f"Scanning {project_path}..."):
            start_time = time.time()
            
            try:
                # Initialize Scanner
                scanner = ProjectScanner(project_path=project_path, llm_model=model)
                
                # Run Scan
                issues = scanner.scan()
                
                duration = time.time() - start_time
                
                # Calculate Metrics
                total_issues = len(issues)
                critical = len([i for i in issues if i.severity == "Critical"])
                high = len([i for i in issues if i.severity == "High"])
                medium = len([i for i in issues if i.severity == "Medium"])
                low = len([i for i in issues if i.severity == "Low"])
                
                # Calculate Risk Score
                weights = {"Critical": 10, "High": 5, "Medium": 2, "Low": 1}
                risk_score = sum(weights.get(i.severity, 1) for i in issues)
                
                # Display Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Issues", total_issues)
                with col2:
                    st.metric("Risk Score", risk_score)
                with col3:
                    st.metric("Files Scanned", len(scanner.files_to_scan))
                with col4:
                    st.metric("Duration", f"{duration:.2f}s")
                
                st.markdown("---")
                
                # Charts
                if total_issues > 0:
                    chart_col1, chart_col2 = st.columns(2)
                    
                    with chart_col1:
                        st.subheader("Severity Distribution")
                        severity_data = pd.DataFrame({
                            "Severity": ["Critical", "High", "Medium", "Low"],
                            "Count": [critical, high, medium, low]
                        })
                        st.bar_chart(severity_data.set_index("Severity"))
                        
                    with chart_col2:
                        st.subheader("Vulnerability Types")
                        type_counts = {}
                        for issue in issues:
                            type_counts[issue.vulnerability_type] = type_counts.get(issue.vulnerability_type, 0) + 1
                        st.bar_chart(pd.Series(type_counts))

                # Issues List
                st.subheader("Detected Vulnerabilities")
                
                if total_issues == 0:
                    st.success("No vulnerabilities found! 🎉")
                else:
                    for issue in issues:
                        with st.expander(f"{issue.severity} - {issue.vulnerability_type} in {os.path.basename(issue.file_path)}"):
                            st.markdown(f"**File:** `{issue.file_path}:{issue.line_number}`")
                            st.markdown(f"**Description:** {issue.description}")
                            
                            st.markdown("#### Code Snippet")
                            st.code(issue.snippet, language=os.path.splitext(issue.file_path)[1][1:])
                            
                            if issue.suggested_fix:
                                st.markdown("#### Suggested Fix")
                                st.code(issue.suggested_fix, language=os.path.splitext(issue.file_path)[1][1:])
                                
                            if issue.fix_theory:
                                st.markdown(f"**Theory:** {issue.fix_theory}")

            except Exception as e:
                st.error(f"An error occurred during scanning: {e}")
                st.exception(e)

if __name__ == "__main__":
    main()
