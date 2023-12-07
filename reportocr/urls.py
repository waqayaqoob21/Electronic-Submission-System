from django.urls import path
from .views import *

urlpatterns = [
    path('ocr/', ReprotOcrAPIView.as_view(), name='ocr'),
    path('addDocument/', AddDocumentAPIView.as_view(), name='addDocument'),
    path('getOcrDocsList/', GetOcrDocumentListAPIView.as_view(), name='getOcrDocsList'),
    path('deleteOcrDocument/', DeleteOcrDocumentAPIView.as_view(), name='deleteOcrDocument'),
    path('addAssmbly/', addAssmblyAPIView.as_view(), name='addAssmbly'),
    path('updateAssmbly/', updateAssmblyAPIView.as_view(), name='updateAssmbly'),
    path('getAssemblies/', getAssembliesAPIView.as_view(), name='getAssemblies'),
    path('DeleteAssembly/', deleteAssemblyAPIView.as_view(), name='DeleteAssembly'),

    ################# sub assembly master form apis

    path('addSubAssmbly/', addSubAssmblyAPIVIEW.as_view(), name='addSubAssmbly'),
    path('getSubAssemblies/', getSubAssembliesAPIView.as_view(), name='getSubAssemblies'),
    path('updateSubAssmbly/', updateSubAssmblyAPIView.as_view(), name='updateSubAssmbly'),
    path('DeleteSubAssembly/', deleteSubAssemblyAPIView.as_view(), name='DeleteSubAssembly'),
    path('getSetIdsBhdActivity/', getSetIdsBhdActivityAPIView.as_view(), name='getSetIdsBhdActivity'),

    ################# qualification test master form apis

    path('addQualificationTest/', addQualificationTestAPIVIEW.as_view(), name='addQualificationTest'),
    path('getQualificationTest/', getQualificationTestAPIView.as_view(), name='getQualificationTest'),
    path('updateQualificationTest/', updateQualificationTestAPIView.as_view(), name='updateQualificationTest'),
    path('DeleteTest/', DeleteTestAPIView.as_view(), name='DeleteTest'),

    ################# Qualification Test Report

    path('addQualificationReport/', addQualificationReport.as_view(), name='addQualificationReport'),
    path('getQualificationReport/', getQualificationReportAPIView.as_view(), name='getQualificationReport'),
    path('DeleteOCR/', DeleteOCRAPIView.as_view(), name='DeleteOCR'),
    path('updateOcr/', updateOcrAPIView.as_view(), name='updateOcr'),

    path('searchOcrReport', searchOcrReportAPIView.as_view(), name='searchOcrReport'),

]
