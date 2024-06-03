import re
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from word2number import w2n
import string
from datetime import datetime
from dateutil import parser


def _expand_abbreviations(text, abbreviations):
    for abbr, expanded in abbreviations.items():
        text = re.sub(r'\b' + re.escape(abbr) + r'\b', expanded, text)
    return text

# تابع لتطبيع التواريخ
def _normalize_dates(text: str) -> str:
    # نمط العادي للتواريخ
    date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|' \
                   r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})|' \
                   r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2,4})|' \
                   r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{2,4})|' \
                   r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4})|' \
                   r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{2,4})|' \
                   r'(\d{1,2})(st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:\s+\d{2,4})?|' \
                   r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})(st|nd|rd|th)?(?:,\s+\d{2,4})?|' \
                   r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})(st|nd|rd|th)?(?:\s+\d{2,4})?'

    def replace_date(match):
        date_str = match.group(0)
        try:
            # محاولة تحليل التاريخ باستخدام parser
            date_obj = parser.parse(date_str, default=datetime(2024, 1, 1))
            # معالجة التواريخ المختصرة
            if date_obj.year < 100:
                if date_obj.year >= 70:  # اعتبار تواريخ من 70-99 ضمن القرن 1900
                    date_obj = date_obj.replace(year=date_obj.year + 1900)
                else:  # اعتبار تواريخ من 00-69 ضمن القرن 2000
                    date_obj = date_obj.replace(year=date_obj.year + 2000)
            normalized_date = date_obj.strftime('%Y-%m-%d')
            return normalized_date
        except ValueError:
            return date_str

    # تحليل النص وتطبيق المنطق
    processed_text = re.sub(date_pattern, replace_date, text)
    return processed_text

# تابع لتجذير الكلمات
def _stem_tokens(tokens):
    ps = PorterStemmer()
    stemmed_words = [ps.stem(word) for word in tokens]
    return stemmed_words

# تابع لتصريف الكلمات
def _lemmatize_tokens(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
    return lemmatized_words

# تابع لتصفية الكلمات
def _filter_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in tokens if word.lower() not in stop_words]
    return filtered_words

# تابع لتحويل الأرقام إلى كلمات
def _number_to_words(tokens):
    number_words = [w2n.word_to_num(word) if word.isdigit() else word for word in tokens]
    return list(map(str, number_words))

# تابع لإزالة علامات الترقيم
def _remove_punctuations(tokens):
    return [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens if word.translate(str.maketrans('', '', string.punctuation))]

abbreviations = {
    "e.g.": "for example",
    "i.e.": "that is",
    'Dr.': 'Doctor',
    'Mr.': 'Mister',
    'Mrs.': 'Misess',
    'Ms.': 'Misess',
    'Jr.': 'Junior',
    'Sr.': 'Senior',
    'U.S': 'UNITED STATES',
    'U-S': 'UNITED STATES',
    'U_K': 'UNITED KINGDOM',
    'U_S': 'UNITED STATES',
    'U.K': 'UNITED KINGDOM',
    'U.S': 'UNITED STATES',
    'VIETNAM': 'VIET NAM',
    'VIET NAM': 'VIET NAM',
    'U-N': 'NITED NATIONS',
    'U_N': 'NITED NATIONS',
    'U.N': 'NITED NATIONS',
    'UK': 'UNITED KINGDOM',
    'US': 'UNITED STATES',
    'U-K': 'UNITED KINGDOM',
    'mar': 'March',
    'march': 'March',
    'jan': 'January',
    'anuary': 'January',
    'feb': 'February',
    'february': 'February',
    'apr': 'April',
    'april': 'April',
    'jun': 'June',
    'june': 'June',
    'jul': 'July',
    'july': 'July',
    'dec': 'December',
    'december': 'December',
    'nov': 'November',
    'november': 'November',
    'oct': 'October',
    'october': 'October',
    'sep': 'September',
    'september': 'September',
    'aug': 'August',
    'august': 'August',
}

# تابع المعالجة الرئيسية
def get_preprocessed_text_terms(text: str,dataset_name:str) -> str:
    text = _expand_abbreviations(text, abbreviations)
    text = _normalize_dates(text)
    tokens = nltk.word_tokenize(text)
    tokens = _filter_tokens(tokens)
    tokens = _stem_tokens(tokens)
    tokens = _lemmatize_tokens(tokens)
    # tokens = _number_to_words(tokens)
    tokens = _remove_punctuations(tokens)

    return tokens
