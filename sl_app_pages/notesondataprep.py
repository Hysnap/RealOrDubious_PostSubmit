import streamlit as st
from sl_utils.logger import log_function_call, streamlit_logger as logger


@log_function_call(logger)
def notesondataprep_body():
    
    Kaggle = "https://www.kaggle.com/"

    datalink = "https://www.kaggle.com/robertjacobson/uk-political-donations"

    tab1, tab2, tab3 = st.tabs("Source Data", "Data Cleansing and Assumptions", "Word and Phrase Analysis")
    # use markdown to create headers and sub headers
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.write("---")
            st.subheader("Notes on Data Source")
            st.write("---")
            st.markdown(''' 
            The data was sourced from [Kaggle](https://www.kaggle.com/),
            The following datasets were considered:
            #### Fake News Datasets from Kaggle
            [BBC Articles Dataset](https://www.kaggle.com/datasets/jacopoferretti/bbc-articles-dataset)
            **Files and Structure**
            - **bbc_news_text_complexity_summarization.csv** (2127 records)
            - `text`
            - `labels` (article type)
            - `no_sentences`
            - `flesch_reading_ease`
            - `dale_chall_readability`
            - `text_rank_summary`
            - `ISA_summary`
            - **bbc_text_cls.csv** (2127 records)
            - `text`
            - `label`
            - **bbc_news_data.csv** (2092 records)
            - `category`
            - `filename`
            - `title`
            - `content`

            [Fake News Classification Dataset](https://www.kaggle.com/datasets/aadyasingh55/fake-news-classification)
            **Files and Structure**
            - **evaluation.csv** (8117 records)
            - **test.csv** (8117 records)
            - **train.csv** (24352 records)
            - `index`
            - `title`
            - `text`
            - `label`

            [Fake or Real News Dataset](https://www.kaggle.com/datasets/nitishjolly/news-detection-fake-or-real-dataset)
            **Files and Structure**
            - **fake_and_real_news.csv** (9865 records)
            - `text`
            - `label` (real / fake)

            [AI vs Human Text Dataset](https://www.kaggle.com/datasets/shanegerami/ai-vs-human-text)
            **Files and Structure**
            - **Ai_Human.csv** (487,235 records)
            - `Text`
            - `Generated` (1 = AI, 0 = human)
            ''')
        with col2:
            st.write("---")
            st.subheader("Notes on Data Source (Continued)")
            st.write("---")
            st.markdown('''
            [Fake News Detection (2015-2017)](https://www.kaggle.com/datasets/bhavikjikadara/fake-news-detection)
            **Files and Structure**
            - **fake.csv** (17,903 records)
            - **true.csv** (21,192 records)
            - `title` (title of news)
            - `text` (description of news, including source)
            - `subject` (type of news)
            - `date`

            [Fake News Dataset](https://www.kaggle.com/datasets/algord/fake-news)
            **Files and Structure**
            - **FakeNewsNet.csv** (22,855 records)
            - `title` (title of the article)
            - `news_url` (URL of the article)
            - `source_domain` (web domain where the article was posted)
            - `tweet_num` (number of retweets for this article)
            - `real` (label column, where 1 is real and 0 is fake)

            [PolitiFact Fact-Check Dataset](https://www.kaggle.com/datasets/rmisra/politifact-fact-check-dataset)
            **Files and Structure**
            - **politifact_factcheck_data.json** (21,152 records)
            - `verdict` (one of {true, mostly-true, half-true, mostly-false, false, pants-fire})
            - `statement_originator` (person who made the statement being fact-checked)
            - `statement`
            - `statement_date`
            - `statement_source` (one of {speech, television, news, blog, social_media, etc.})
            - `factchecker` (name of fact-checker)
            - `factcheck_date`
            - `factcheck_analysis_link`

            [Misinformation & Fake News Text Dataset (79K)](https://www.kaggle.com/datasets/stevenpeutz/misinformation-fake-news-text-dataset-79k)
            **Files and Structure**
            - **MisinfoSuperSet_True.csv**
            - **MisinfoSuperSet_False.csv**
            - **EXTRA_RussianPropergandaSubset.csv**
            - `Index`
            - `Text`

            [Non-English Fake News Dataset](https://www.kaggle.com/datasets/cryptexcode/banfakenews)
            **Files and Structure**
            - **Authentic-48K.csv**
            - **Fake-1K.csv**
            - **LabeledAuthentic-7K.csv**
            - **LabeledFake-1K.csv**
            **Column Structure**
            - `articleID` (ID of the news)
            - `domain` (News publisher's site name)
            - `date` (Category of the news)
            - `category` (Category of the news)
            - `headline`
            - `content` (Article or body of the news)
            - `label` (1 for authentic, 0 for fake)
            - **For Labeled Datasets**
            - `source` (who can verify the claim)
            - `relation` (Related or Unrelated)
            - `F-type` (Type of fake news: Clickbait, Satire, Misleading)

            [Fake/Real News Dataset (2013-2020)](https://www.kaggle.com/datasets/techykajal/fakereal-news)
            **Files and Structure**
            - **New Task.csv** (9960 records)
            - `News_Headline`
            - `Link_Of_News`
            - `Source` (author of the post)
            - `Stated_On` (date posted on social media)
            - `Date` (date analyzed by fact-checkers)
            - `Label` (True, Mostly-True, Half-True, Barely-True, False, Pants on Fire)

            [Fake News Dataset Around the Syrian War (2014-2018)](https://www.kaggle.com/datasets/mohamadalhasan/a-fake-news-dataset-around-the-syrian-war)
            **Files and Structure**
            - **FA-Kes-Dataset.csv** (774 records)
            - `Index`
            - `Title_of_Article`
            - `article_content`
            - `source`
            - `date`
            - `location`
            - `Label`
            ''')
        st.write("### The final dataset used was")
        st.markdown('''
            Following a top line review of the available datasets - it has been decided to start with - 

            ## [Fake News Detection (2015-2017)](https://www.kaggle.com/datasets/bhavikjikadara/fake-news-detection)
            ### **Files and Structure**
            - **fake.csv** (17,903 records)
            - **true.csv** (21,192 records)
            - `title` (title of news)
            - `text` (description of news, including source)
            - `subject` (type of news)
            - `date`
                
            As it contains a date and a sizeable dataset.

            This was later enhanced with the following dataset - after several issues of Bias were identified in the original dataset.

            ## [Misinformation & Fake News Text Dataset (79K)](https://www.kaggle.com/datasets/stevenpeutz/misinformation-fake-news-text-dataset-79k)
            ### **Files and Structure**
            - **MisinfoSuperSet_True.csv**
            - **MisinfoSuperSet_False.csv**
            - **EXTRA_RussianPropergandaSubset.csv**
            - `Index`
            - `Text`

            The next step will be to get the data, combine the two files with labels added for fake and true.  Then review the cleanliness, implement data cleansing and start analysis.
            ''')
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("---")
            st.subheader("ETL Processing")
            st.write("---")
            # provide description of steps taken in ETL.py and TRANSORM.py and data_prep.py
            st.markdown(
            """**Description of Data Preparation Steps:**

            1. **Data Loading and Cleaning:**
                - Load data from CSV files.
                - Remove null values, duplicates, and irrelevant records.

            2. **Data Transformation:**
                - Extract relevant fields such as location and source.
                - Remove unnecessary text fields.
                - Perform sentiment analysis and categorize sentiments.
                - Calculate contradictions and variations in the data.

            3. **Location Processing:**
                - Append NLP-extracted locations to text.
                - Extract locations from articles and split them into a separate dataframe.
                - Summarize location data by `article_id` and `location`.
                - Create a dataframe of unique locations and filter out ignored locations. """
        with col2:
            st.write("---")
            st.markdown("""
            4. **Geographical Data Enrichment:**
                - Extract latitude, longitude, and address information.
                - Derive continent, country, and state details.
                - Search for location matches in multiple columns of the `worldcities_df`.

            5. **Common Themes Analysis:**
                - Generate a list of common themes from the data.
                - Create a dataframe of common themes and save it to a CSV file.

            6. **Final Data Preparation:**
                - Drop unnecessary columns and rows with empty `cleaned_text`.
                - Set missing `month`, `day`, and `year` values based on `date_clean`.
                - Export the cleaned and transformed data to a CSV file."""
            )
    with tab3:
        st.write("---")
        st.subheader("Word and Phrase Analysis")
        st.write("---")
        # provide description of steps taken in ETL.py and TRANSORM.py and data_prep.py
        st.markdown(
        """
        **Data Cleaning and Feature Extraction Overview:**

        - **Purpose:** Processing the text heavy articles and titles to enable analysis and creation of visualisations.
        - **Data Preparation steps:**
            - Remove stop words and punctuation from the texts.
            - Identify and analyse 1, 2 and 3 Ngrams, in Articles.
            - Compare the frequency of different Ngrams between the whole data set, Real and Dubious articles.
            - Try to identify unique Ngrams for Real and Dubious articles.
        - **Final Ngrams exported to csv:**
            - File will be imported to create wordclouds and other visualisations.
            - Enables further analysis with out the need to reprocess the text data.

        """)


# End of script
# PATH: sl_app_pages/notesondataprep.py