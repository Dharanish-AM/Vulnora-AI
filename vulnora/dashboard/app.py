import streamlit as st
import requests
import pandas as pd
import json
import os

st.set_page_config(page_title="Vulnora AI", page_icon="🛡️", layout="wide")

st.title("🛡️ Vulnora AI - Security Scanner")
st.markdown("### AI-Powered Multi-Language Code Security Scanner")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    project_path = st.text_input("Project Path", placeholder="/path/to/your/project")
    llm_model = st.selectbox("LLM Model", ["llama3.1:8b", "llama3", "mistral"], index=0)
    scan_button = st.button("Start Scan", type="primary")

if scan_button and project_path:
    if not os.path.exists(project_path):
        st.error(f"Path does not exist: {project_path}")
    else:
        with st.spinner("Scanning project... This may take a while depending on project size and LLM speed."):
            try:
                # Call the local API
                # Note: In a real deployment, the URL might be configurable
                response = requests.post(
                    "http://localhost:8000/scan",
                    json={"path": project_path, "model": llm_model}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Scan completed in {result['scan_duration']} seconds!")
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Issues", len(result['issues']))
                    col2.metric("Smell Score", result['smell_score'])
                    col3.metric("Files Scanned", "N/A") # API doesn't return this yet, but could
                    
                    # Issues Table
                    if result['issues']:
                        df = pd.DataFrame(result['issues'])
                        
                        # Severity distribution
                        st.subheader("Severity Distribution")
                        severity_counts = df['severity'].value_counts()
                        st.bar_chart(severity_counts)
                        
                        # Detailed Issues
                        st.subheader("Vulnerabilities Found")
                        
                        # Filters
                        severity_filter = st.multiselect("Filter by Severity", df['severity'].unique(), default=df['severity'].unique())
                        filtered_df = df[df['severity'].isin(severity_filter)]
                        
                        for index, row in filtered_df.iterrows():
                            with st.expander(f"[{row['severity']}] {row['vulnerability_type']} in {os.path.basename(row['file_path'])}:{row['line_number']}"):
                                st.markdown(f"**File:** `{row['file_path']}`")
                                st.markdown(f"**Description:** {row['description']}")
                                st.markdown(f"**Confidence:** {row['confidence']}")
                                if row['snippet']:
                                    st.code(row['snippet'], language='python') # Defaulting to python for highlighting
                                st.markdown(f"**Suggested Fix:**")
                                st.info(row['suggested_fix'])
                                
                    else:
                        st.balloons()
                        st.success("No vulnerabilities found! Great job!")
                        
                else:
                    st.error(f"Scan failed: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend API. Is it running? (Run `python main.py api`)")
            except Exception as e:
                st.error(f"An error occurred: {e}")

elif scan_button and not project_path:
    st.warning("Please enter a project path.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Vulnora AI Team")
