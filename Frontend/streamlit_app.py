import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

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
    if st.button("Rank Jobs", key="rank_button") and uploaded_files:
        # Placeholder until hooked up with FastAPI
        st.info("✅ CVs uploaded. Ranking will be handled by backend API.")
        # Later you can call FastAPI here and display results
        # Example placeholder visualization:
        example_scores = [75, 60, 40]
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(
            x=list(range(1, len(example_scores) + 1)), 
            y=example_scores, 
            palette=['red', 'blue', 'purple']
        )
        plt.title("Job Similarity Scores", color='white')
        plt.xlabel("Job", color='white')
        plt.ylabel("Similarity Score (%)", color='white')
        plt.ylim(0, 100)
        plt.xticks(ticks=list(range(0, len(example_scores) + 1)), color='white')
        plt.yticks(color='white')
        for idx, score in enumerate(example_scores):
            ax.text(idx, score + 1, f"{score:.2f}%", ha="center", color='white')
        st.pyplot(plt)
        st.write("")

if __name__ == "__main__":
    main()
