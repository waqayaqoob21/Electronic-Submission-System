from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FileUploadParser
from .models import Ocr
from .serializers import OcrSerializer
from .ocrController import ocrController

# Create your views here.

ctrl_obj = ocrController()


# -----------------------------------------


class ReprotOcrAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.reportOCr(request.data)
        return result


class AddDocumentAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.addDocument(request.data)
        return result


class GetOcrDocumentListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getOcrDocumentList(request.data)
        return result


class DeleteOcrDocumentAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.deleteOcrDocument(request)
        return result


# =====================================

class addAssmblyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.addAssmbly(request)
        return result


class addSubAssmblyAPIVIEW(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.addSubAssmbly(request)
        return result


class getAssembliesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getAssemblies(request)
        return result


class getSetIdsBhdActivityAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getSetIdsBhdActivity(request)
        return result


class getSubAssembliesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getSubAssemblies(request)
        return result


class getQualificationTestAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getQualificationTest(request)
        return result


class updateAssmblyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.updateAssmbly(request)
        return result


class deleteAssemblyAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.deleteAssembly(request)
        return result


class updateSubAssmblyAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.updateSubAssmbly(request)
        return result


class updateQualificationTestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.updateQualification(request)
        return result


class updateOcrAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.updateOcr(request)
        return result


class searchOcrReportAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.searchOcrReport(request)
        return result


class deleteSubAssemblyAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.deleteSubAssembly(request)
        return result


class DeleteTestAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.DeleteTestAPIView(request)
        return result


class DeleteOCRAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.DeleteOCR(request)
        return result


class addQualificationTestAPIVIEW(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.addQualificationTest(request)
        return result


class addQualificationReport(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.addQualificationReport(request)
        return result


class getQualificationReportAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getQualificationReport(request)
        return result


class addExcelDataAPIVIEW(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.bulkInsert(request)
        return result


class getTreeDataAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getTreeData(request)
        return result


class checkReportAPIVIEW(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.reportCheck(request.data)
        return result


class getScannedQualificationReportListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getScannedQualificationReportList(request)
        return result


class checkBatchNoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.checkBatchNo(request)
        return result


class DownloadFileAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.downloadFile(request)
        return result


class getBatchListListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getBatchList(request)
        return result


class getDataForExcelViewAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = ctrl_obj.getDataForExcelView(request)
        return result


class RenameReportsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.RenameReports(request)
        return result


class ScanAllReportsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = ctrl_obj.ScanAllReports(request)
        return result
