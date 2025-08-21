import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import requests

API_URL = "http://127.0.0.1:8000"  # replace with your DigitalOcean URL later

def main():
    plt.style.use('dark_background')
    
    # App title & header
    st.title("🧭 CareerCompass")
    st.write("## ✍️ CV Ranking System")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.title("🧭 CareerCompass")
        st.write("Welcome to CareerCompass, your personal career guide!")
        st.write("We help you find the most suitable job opportunities based on the similarity between your CV and job descriptions.")
        st.markdown("---")
        st.markdown("# 💀 Cheat Code")
        if st.button("💡 Show Team Members"):
            st.markdown("👤 Ryan Chitate")
            st.markdown("👤 Mitheel Ramdaw")
            st.markdown("👤 Mikhaar Ramdaw")
        st.markdown("---")

    # Fetch jobs from backend
    try:
        jobs = requests.get(f"{API_URL}/jobs").json()["jobs"]
        job_options = {job["title"]: job["id"] for job in jobs}
        job_title = st.selectbox("Select Job", list(job_options.keys())) if job_options else None
    except Exception:
        st.error("⚠️ Could not connect to backend. Make sure FastAPI is running.")
        return

    # Upload CV section
    st.title("📄 **Upload CVs**")
    uploaded_files = st.file_uploader(
        "Upload PDFs", 
        type=["pdf"], 
        accept_multiple_files=True, 
        key="cv_upload"
    )
    st.write("")

    # Action button
    if st.button("Rank Jobs", key="rank_button") and uploaded_files and job_title:
        job_id = job_options[job_title]
        scores = []

        for uploaded_file in uploaded_files:
            files = {"file": uploaded_file}
            data = {"job_id": job_id}
            res = requests.post(f"{API_URL}/upload_cv", files=files, data=data)

            if res.status_code == 200:
                result = res.json()
                scores.append({"cv": uploaded_file.name, "score": result["score"]})
                st.success(f"{uploaded_file.name} scored {result['score']:.2f}%")
            else:
                st.error(f"❌ Failed to process {uploaded_file.name}")

        # Plot results
        if scores:
            plt.figure(figsize=(10, 6))
            labels = [s["cv"] for s in scores]
            values = [s["score"] for s in scores]
            ax = sns.barplot(x=labels, y=values, palette="viridis")
            plt.title("CV Match Scores", color="white")
            plt.ylabel("Similarity (%)", color="white")
            for idx, score in enumerate(values):
                ax.text(idx, score + 1, f"{score:.2f}%", ha="center", color="white")
            st.pyplot(plt)

if __name__ == "__main__":
    main()
