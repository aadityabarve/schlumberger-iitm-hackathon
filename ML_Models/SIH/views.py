from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from newspaper import Article
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
import io
import os
import dill
import nltk
# import pytesseract
# try:
#   from PIL import Image
# except ImportError:
#   import Image
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from msrest.authentication import CognitiveServicesCredentials
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class TextSummarizer(View):
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        text = pythondata.get('text', None)
        with open(os.path.join(settings.BASE_DIR, 'ml_models/tokenizer_text_summarizer'), 'rb') as f:
            tokenizer = dill.load(f)
        with open(os.path.join(settings.BASE_DIR, 'ml_models/model_text_summarizer'), 'rb') as f:
            model = dill.load(f)
        inputs = tokenizer([text], return_tensors='pt')
        words = len(text.split())
        summary_ids = model.generate(inputs['input_ids'], early_stopping=False)
        summary = [tokenizer.decode(g, skip_special_tokens=True) for g in summary_ids]
        return JsonResponse({'extracted_text': summary[0]})

@method_decorator(csrf_exempt, name='dispatch')
class ArticleSummarizer(View):
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        text = pythondata.get('text', None)
        article = Article(text)
        article.download()
        article.parse()
        nltk.download('punkt')
        article.nlp()
        return JsonResponse({'extracted_text': article.summary})

# @method_decorator(csrf_exempt, name='dispatch')
# class Summarizer(View):
#     def post(self, request, *args, **kwargs):


# @method_decorator(csrf_exempt, name='dispatch')
# class TextToImage(View):
#     def post(self, request, *args, **kwargs):
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         text = pythondata.get('text', None)
#         with open(os.path.join(settings.BASE_DIR, 'ml_models/netG210000.pth'), 'rb') as f:
#             model = dill.load(f)
#         image = model.generate(text)
#         return JsonResponse({'image': image})

# @method_decorator(csrf_exempt, name='dispatch')
# class ImageToText(View):
#     def post(self, request, *args, **kwargs):
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         text = pythondata.get('text', None)
#         # with open(os.path.join(settings.BASE_DIR, 'ml_models/netG210000.pth'), 'rb') as f:
#         #     model = dill.load(f)
#         # image = model.generate(text)
#         print(text)
#         key = "82a26595d5994464a2e3a02a3ede3cd5"
#         endpoint = "https://cvmitaoe.cognitiveservices.azure.com/"
#         creds = CognitiveServicesCredentials(key)
#         client = ComputerVisionClient(endpoint=endpoint, credentials=creds)
#         with open(text,'rb') as img:
#             result = client.describe_image_in_stream(img)
#         print(result.captions[0].text)
#         response = JsonResponse({'caption': result.captions[0].text})
#         response.status_code = 200
#         return response

# @method_decorator(csrf_exempt, name='dispatch')
# class OCR(View):
#     def post(self, request, *args, **kwargs):
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         image_path = pythondata.get('image_path', None)
#         extractedInformation = pytesseract.image_to_string(Image.open(image_path))
#         return JsonResponse({'extracted_text': extractedInformation})
#
# @method_decorator(csrf_exempt, name='dispatch')
# class DocumentSimilarity(View):
#     def compute_cosine_similarity(self, text1, text2):
#         list_text = [text1, text2]
#         vectorizer = TfidfVectorizer(stop_words='english')
#         vectorizer.fit_transform(list_text)
#         tfidf_text1, tfidf_text2 = vectorizer.transform([list_text[0]]), vectorizer.transform([list_text[1]])
#         cs_score = cosine_similarity(tfidf_text1, tfidf_text2)
#         return np.round(cs_score[0][0],2)
#
#     def post(self, request, *args, **kwarga):
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         document1 = pythondata.get('document1', None)
#         documents = pythondata.get('documents', None)
#         answer = 0
#         for document in documents:
#             cosine_similarity = self.compute_cosine_similarity(document1, document) * 100
#             if answer < cosine_similarity:
#                 answer = cosine_similarity
#         return JsonResponse({'percentage': answer})
