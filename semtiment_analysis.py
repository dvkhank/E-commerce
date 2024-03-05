import pandas as pd
import string
from stop_words import get_stop_words
from underthesea import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Đọc dữ liệu
positive_df = pd.read_excel('D:/Github/e_commerce/data_positive_full.xlsx')
negative_df = pd.read_excel('D:/Github/e_commerce/data_negetive_full.xlsx')

# Ghép nối hai bảng dữ liệu
merged_df = pd.concat([positive_df, negative_df], ignore_index=True)

# Tải stopwords tiếng Việt
stop_words = get_stop_words('vi')

# Tiền xử lý dữ liệu
def preprocess_text(text):
    text = text.lower()
    text = remove_punctuation(text)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text_tokens = word_tokenize(text)
    text_str = ' '.join(text_tokens)
    return text_str

# Loại bỏ dấu câu
def remove_punctuation(text):
    if isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    return str(text)

# Tokenize và tiền xử lý dữ liệu trong dataframe
merged_df['Reviews'] = merged_df['Reviews'].str.lower()
merged_df['Reviews'] = merged_df['Reviews'].apply(remove_punctuation)
merged_df['Reviews'] = merged_df['Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
merged_df['Reviews'] = merged_df['Reviews'].apply(word_tokenize)

# Chia dữ liệu tập huấn
X_train, X_test, y_train, y_test = train_test_split(merged_df['Reviews'], merged_df['Sentiment'], test_size=0.2, random_state=42)

# Chuyển đổi văn bản thành ma trận đặc trưng
vectorizer = CountVectorizer()
X_train_str = [' '.join(tokens) for tokens in X_train]
X_test_str = [' '.join(tokens) for tokens in X_test]
X_train_vectorized = vectorizer.fit_transform(X_train_str)
X_test_vectorized = vectorizer.transform(X_test_str)

# Huấn luyện mô hình Logistic Regression
model = LogisticRegression(random_state=42)
model.fit(X_train_vectorized, y_train)

# Dự đoán cảm xúc của một đoạn văn bản
def predict_sentiment(text):
    # Tiền xử lý dữ liệu
    text_processed = preprocess_text(text)
    text_vectorized = vectorizer.transform([text_processed])

    # Dự đoán
    prediction = model.predict(text_vectorized)
    return prediction[0] == 'Positive'

text_to_test = "Sản phẩm này rất tốt, tôi rất hài lòng với chất lượng và dịch vụ của cửa hàng."

# Dự đoán cảm xúc của đoạn văn bản
predicted_sentiment = predict_sentiment(text_to_test)

if predicted_sentiment: #KQ là TRUE
    print("Đoạn văn bản tích cực")
else: #KQ là FALSE
    print("Đoạn văn bản tiêu cực")
