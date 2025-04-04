import streamlit as st
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data():
    uploaded_file = st.file_uploader("Upload CSV File",type=["csv"])
    if uploaded_file is not None:

        return pd.read_csv(uploaded_file)
    else:
        st.warning("No file uploaded! Using default sample dataset.")


        np.random.seed(42)
        size = 1000

        df = pd.DataFrame({
            "group": np.random.choice(["control", "treatment"], size=10000, p=[0.5, 0.5]),
            "converted": np.random.choice([0, 1], size=10000, p=[0.95, 0.05])  # %5 dönüşüm oranı
        })

        return df

def ab_test(df):
    if "group" not in df.columns or "converted" not in df.columns:
        st.error("there is not group and converted columns")
        return None
    control = df[df['group'] == 'control']['converted']
    treatment = df[df['group'] == 'treatment']['converted']

    stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)
    return stat, p_value


def main():
    st.title('A/B Tester')

    df = load_data()

    if df is not None:
        st.write("## 📊 loaded data")
        st.dataframe(df.head())

        st.write("## 🔍 data distribution")
        fig, ax = plt.subplots()

        sns.barplot(x=df['group'],y=df['converted'],ci=None,ax=ax)
        st.pyplot(fig)

        stats,p_value = ab_test(df)

        if stats is not None:
            st.write("## 📈 test result")
            st.write(f"t_statistics: {stats:.4f}")
            st.write(f"p_value: {p_value:.4f}")

            if p_value < 0.05:
                st.success("result: A/B test logical! (p < 0.05)")
            else:
                st.warning("result: A/B test not logical! (p > 0.05 )")

if __name__ =="__main__":
    main()