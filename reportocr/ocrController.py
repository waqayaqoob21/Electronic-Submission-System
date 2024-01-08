import json

from django.http import JsonResponse
from django.http import HttpResponse
import uuid

from usermanagement.serializer import *
from .models import *
from django.db.models import F, Q
from datetime import date, datetime
import random
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
import string
import os, shutil
import fitz
import io
import pandas as pd
import itertools
import math
from .serializers import *
import PyPDF2


class ocrController:
    @staticmethod
    def addDocument(request):
        ocrModel = Ocr()
        try:
            OcrData = Ocr.objects.filter(BHD_No=request.get('BHD_No')).first()
            if OcrData is None:
                ocrModel.document_type = request['document_type']
                ocrModel.bhd_no = request['BHD_No']
                ocrModel.job_card_no = request['Job_Card_No']
                if request['Dated'] != '':
                    ocrModel.date = request['Dated']
                ocrModel.system_type = request['sys_type']
                ocrModel.system_name = request['sys_name']
                ocrModel.batch_set_id = request['Batch_Set_NO']
                ocrModel.ref_criteria = request['Ref_Criteria']
                ocrModel.activity_type = request['Type_of_activity']
                ocrModel.status = request['status']
                ocrModel.save()
                return JsonResponse({'message': 'User added successfully', 'success': True, 'status': 201},
                                    status=201)
            else:
                print("we are in the editing part")
                ocrModel.document_type = request['document_type']
                ocrModel.bhd_no = request['BHD_No']
                ocrModel.job_card_no = request['Job_Card_No']
                if request['Dated'] != '':
                    ocrModel.date = request['Dated']
                ocrModel.system_type = request['sys_type']
                ocrModel.system_name = request['sys_name']
                ocrModel.batch_set_id = request['Batch_Set_NO']
                ocrModel.ref_criteria = request['Ref_Criteria']
                ocrModel.activity_type = request['Type_of_activity']
                ocrModel.status = request['status']
                ocrModel.save()
                return JsonResponse({'message': 'User Successfully Edited', 'success': True, 'status': 201},
                                    status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def addAssmbly(request):
        try:
            print(request)
            assebmlies = json.loads(request.data['assemblies'])
            for item in assebmlies:
                print(item)
                if item['value'] != '':
                    check_record = batch_bhd_activity.objects.filter(system_name=request.data['sys_name'],
                                                                     batch_set_id=request.data['batch_set_no'],
                                                                     bhd_no=request.data['bhd_no'],
                                                                     activity_type=request.data['activityType']).first()
                    if check_record is None:
                        row = batch_bhd_activity()
                        row.system_name = request.data['sys_name']
                        row.batch_set_id = request.data['batch_set_no']
                        row.bhd_no = request.data['bhd_no']
                        row.activity_type = request.data['activityType']
                        row.title = request.data['title_name']
                        row.date = request.data['ass_date']
                        row.ref_criteria = request.data['reference_criteria']
                        row.save()

                    print("going to add assembly")
                    # if check_record is None:
                    modal = assemblies()
                    modal.assembly_name = item['value']
                    modal.system_name = request.data['sys_name']
                    modal.system_type = request.data['sys_type']
                    modal.batch_set_id = request.data['batch_set_no']
                    modal.bhd_no = request.data['bhd_no']
                    modal.activity_type = request.data['activityType']
                    modal.title = request.data['title_name']
                    modal.date = request.data['ass_date']
                    modal.ref_criteria = request.data['reference_criteria']
                    modal.save()
                    print("assembly saved")

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def addSubAssmbly(request):
        try:
            sub_assebmlies = json.loads(request.data['sub_assemblies'])
            for item in sub_assebmlies:
                print(item)
                if item['value'] != '':
                    print("going to add assembly")
                    modal = sub_assemblies()
                    modal.assembly_name = request.data['assembly_name']
                    modal.sub_assembly_name = item['value']
                    modal.system_name = request.data['sys_name']
                    modal.system_type = request.data['sys_type']
                    modal.batch_set_id = request.data['batch_set_no']
                    modal.bhd_no = request.data['bhd_no']
                    modal.activity_type = request.data['activityType']
                    modal.title = request.data['title_name']
                    modal.date = request.data['ass_date']
                    modal.ref_criteria = request.data['reference_criteria']
                    modal.save()
                    print("assembly saved")

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def updateAssmbly(request):
        try:
            print(request)
            id = json.loads(request.data['id'])
            if id != '' and id != 0:
                record = assemblies.objects.filter(id=id).first()
                if record is not None:
                    print("going to update record")
                    record.system_name = request.data['sys_name']
                    record.system_type = request.data['sys_type']
                    record.assembly_name = request.data['assemblies']
                    record.batch_set_id = request.data['batch_set_no']
                    record.bhd_no = request.data['bhd_no']
                    record.activity_type = request.data['activityType']
                    record.title = request.data['title_name']
                    record.date = request.data['ass_date']
                    record.ref_criteria = request.data['reference_criteria']
                    record.save()

            return JsonResponse({'message': "Record updated", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def updateSubAssmbly(request):
        try:
            print(request)
            id = json.loads(request.data['id'])
            if id != '' and id != 0:
                record = sub_assemblies.objects.filter(id=id).first()
                if record is not None:
                    print("going to update record")
                    record.system_name = request.data['sys_name']
                    record.system_type = request.data['sys_type']
                    record.assembly_name = request.data['assembly_name']
                    record.sub_assembly_name = request.data['sub_assembly_name']
                    record.batch_set_id = request.data['batch_set_no']
                    record.bhd_no = request.data['bhd_no']
                    record.activity_type = request.data['activityType']
                    record.title = request.data['title_name']
                    record.date = request.data['ass_date']
                    record.ref_criteria = request.data['reference_criteria']
                    record.save()

            return JsonResponse({'message': "Record updated", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def updateQualification(request):
        try:
            print(request)
            id = json.loads(request.data['id'])
            if id != '' and id != 0:
                record = qualification_test.objects.filter(id=id).first()
                if record is not None:
                    print("going to update record")
                    record.system_name = request.data['sys_name']
                    record.system_type = request.data['sys_type']
                    record.assembly_name = request.data['assembly_name']
                    record.sub_assembly_name = request.data['sub_assembly_name']
                    record.qualification_test = request.data['qualificatio_name']
                    record.batch_set_id = request.data['batch_set_no']
                    record.bhd_no = request.data['bhd_no']
                    record.activity_type = request.data['activityType']
                    record.title = request.data['title_name']
                    record.date = request.data['ass_date']
                    record.ref_criteria = request.data['reference_criteria']
                    record.save()

            return JsonResponse({'message': "Record updated", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def updateOcr(request):
        try:
            print(request)
            id = json.loads(request.data['id'])
            if id != '' and id != 0:
                record = qualification_ocr_report.objects.filter(id=id).first()
                if record is not None:
                    print("going to update record")
                    record.system_name = request.data['sys_name']
                    record.system_type = request.data['sys_type']
                    record.assembly_name = request.data['assembly_name']
                    record.sub_assembly_name = request.data['sub_assembly_name']
                    record.qualification_test = request.data['Q_test']
                    record.batch_set_id = request.data['batch_set_no']
                    record.bhd_no = request.data['bhd_no']
                    record.activity_type = request.data['activityType']
                    record.title = request.data['title_name']
                    record.date = request.data['ass_date']
                    record.ref_criteria = request.data['reference_criteria']
                    record.ocr_report = request.data['ocr_reports']
                    record.save()

            return JsonResponse({'message': "Record updated", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def searchOcrReport(request):
        try:
            system_type = request.query_params['system_type']
            system_name = request.query_params['system_name']
            assembly_name = request.query_params['assembly_name']
            sub_assembly_name = request.query_params['sub_assembly_name']
            qualification_test = request.query_params['qualification_name']
            batch_no = request.query_params['batch_no']
            bhd_no = request.query_params['bhd_no']
            activity_type = request.query_params['activity_type']
            title = request.query_params['title']
            date = request.query_params['date']
            ref_creiteria = request.query_params['ref_creiteria']

            def get_filter(field_name, filter_condition, filter_value):
                # thanks to the below post
                # https://stackoverflow.com/questions/310732/in-django-how-does-one-filter-a-queryset-with-dynamic-field-lookups
                # the idea to this below logic is very similar to that in the above mentioned post
                if filter_condition.strip() == "contains":
                    kwargs = {
                        '{0}__icontains'.format(field_name): filter_value
                    }
                    return Q(**kwargs)

                if filter_condition.strip() == "not_equal":
                    kwargs = {
                        '{0}__iexact'.format(field_name): filter_value
                    }
                    return ~Q(**kwargs)

                if filter_condition.strip() == "starts_with":
                    kwargs = {
                        '{0}__istartswith'.format(field_name): filter_value
                    }
                    return Q(**kwargs)
                if filter_condition.strip() == "equal":
                    kwargs = {
                        '{0}__iexact'.format(field_name): filter_value
                    }
                    return Q(**kwargs)

                if filter_condition.strip() == "not_equal":
                    kwargs = {
                        '{0}__iexact'.format(field_name): filter_value
                    }

                    return ~Q(**kwargs)

            total_filter_objects = Q()
            if system_type != '':
                total_filter_objects &= get_filter(
                    'system_type', 'equal',
                    system_type)

            if system_name != '':
                total_filter_objects &= get_filter(
                    'system_name', 'equal',
                    system_name)
            if assembly_name != '':
                total_filter_objects &= get_filter(
                    'assembly_name', 'equal',
                    assembly_name)
            if sub_assembly_name != '':
                total_filter_objects &= get_filter(
                    'sub_assembly_name', 'equal',
                    sub_assembly_name)

            if qualification_test != '':
                total_filter_objects &= get_filter(
                    'qualification_test', 'equal',
                    qualification_test)

            if batch_no != '':
                total_filter_objects &= get_filter(
                    'batch_set_id', 'equal',
                    batch_no)

            if bhd_no != '':
                total_filter_objects &= get_filter(
                    'bhd_no', 'equal',
                    bhd_no)

            if activity_type != '':
                total_filter_objects &= get_filter(
                    'activity_type', 'equal',
                    activity_type)

            if title != '':
                total_filter_objects &= get_filter(
                    'title', 'equal',
                    title)

            if ref_creiteria != '':
                total_filter_objects &= get_filter(
                    'ref_criteria', 'equal',
                    ref_creiteria)

            result = qualification_ocr_report.objects.filter(total_filter_objects)
            serializer = ocr_reportSerializer(result, many=True)
            return JsonResponse({'message': "Record updated", 'success': True, 'data': serializer.data, 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def deleteAssembly(request):
        try:
            id = request.query_params['id']
            if id != '' and id != 0:
                result = assemblies.objects.filter(id=id).first()
                result.delete()
                print("record deleted")
            serializer = assembliesSerializer(result, many=True)

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def deleteSubAssembly(request):
        try:
            id = request.query_params['id']
            if id != '' and id != 0:
                result = sub_assemblies.objects.filter(id=id).first()
                result.delete()
                print("record deleted")
            serializer = assembliesSerializer(result, many=True)

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def DeleteTestAPIView(request):
        try:
            id = request.query_params['id']
            if id != '' and id != 0:
                result = qualification_test.objects.filter(id=id).first()
                result.delete()
                print("record deleted")
            serializer = assembliesSerializer(result, many=True)

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def DeleteOCR(request):
        try:
            id = request.query_params['id']
            if id != '' and id != 0:
                result = qualification_ocr_report.objects.filter(id=id).first()
                result.delete()
                print("record deleted")
            serializer = assembliesSerializer(result, many=True)

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def getAssemblies(request):
        try:
            result = assemblies.objects.all()
            serializer = assembliesSerializer(result, many=True)
            result1 = batch_bhd_activity.objects.all()
            serializer1 = getSetIdsBhdActivitySerializer(result1, many=True)

            return JsonResponse(
                {'message': "Record added", 'success': True, 'data': serializer.data, 'batch_detail': serializer1.data,
                 'status': 200},
                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def getSetIdsBhdActivity(request):
        try:
            # print(request)
            result = assemblies.objects.all()
            serializer = assembliesSerializer(result, many=True)

            result1 = batch_bhd_activity.objects.all()
            serializer1 = getSetIdsBhdActivitySerializer(result1, many=True)

            return JsonResponse(
                {'message': "Record added", 'success': True, 'data': serializer.data, 'batch_detail': serializer1.data,
                 'status': 200},
                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def getSubAssemblies(request):
        try:
            result = sub_assemblies.objects.all()
            serializer = sub_assembliesSerializer(result, many=True)

            return JsonResponse({'message': "Record added", 'success': True, 'data': serializer.data, 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def reportOCr(request):
        try:
            def save_file(file: InMemoryUploadedFile, full_path):
                with open(full_path, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

            report_number = ''
            id_number = ''
            result_status = ''
            # filename = "2014_Form_1120.pdf"
            # attachment = request['uploaded_file']
            # open file
            file: InMemoryUploadedFile = request['file']
            # define file_save_path variable
            # full_path = str(datetime.today()).replace('-', '').replace(' ', '') + '_' + file.name
            full_path = file.name
            save_file(file, full_path)
            pdf_images = convert_from_path(full_path)
            for i in range(len(pdf_images)):
                # Save pages as images in the pdf
                pdf_images[i].save('page' + str(i) + '.jpg', 'JPEG')

            # load all images and extract text from each page
            mydist = {}
            for i in range(len(pdf_images)):
                if i == 0:
                    # path_to_tesseract = "/usr/bin/tesseract"  # r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                    image_path = r"page" + str(i) + ".jpg"  # r"page0.jpg"
                    img = Image.open(image_path)
                    pytesseract.tesseract_cmd = path_to_tesseract
                    text = pytesseract.image_to_string(img)

                    print("############################################page ", i)
                    print(text)
                    data = text.split("\n")
                    final_list = data  # [y for x in data for y in x.split(':')]
                    print(final_list)

                    for item in final_list:

                        if item.__contains__("Test Report No:") or item.__contains__(
                                "test report no:") or item.__contains__("Test Report No.") or item.__contains__(
                                "Test Report No") or item.__contains__("Report Number") or item.__contains__(
                                "Report #") or item.__contains__("Report ID") or item.__contains__(
                                "Report ID.") or item.__contains__("Report Id") or item.__contains__(
                                "Report Id.") or item.__contains__("Report No") or item.__contains__("Report No."):
                            print(item)
                            report_number = item.split(":")[1]
                        if item.__contains__("ID No.") or item.__contains__("id no.") or item.__contains__(
                                "ID No.") or item.__contains__("ID NO") or item.__contains__(
                                "ID NO.") or item.__contains__("Part ID") or item.__contains__(
                                "Cable Analyzer ID") or item.__contains__("ID#") or item.__contains__(
                                "Sample ID") or item.__contains__("Identity No") or item.__contains__(
                                "Identity No.") or item.__contains__("Module Name & ID No.") or item.__contains__(
                                "Module Name & ID No"):
                            print(item)
                            id_number = item.split("ID No.:")[1]
                        if item.__contains__("Results") or item.__contains__("results") or item.__contains__(
                                "Test Results") or item.__contains__("Test Result") or item.__contains__(
                                "Expert") or item.__contains__("Review") or item.__contains__(
                                "Results") or item.__contains__("Result") or item.__contains__(
                                "Status") or item.__contains__("Measurement Status") or item.__contains__(
                                "Result(s)") or item.__contains__("Result (s)") or item.__contains__(
                                "Result(S)") or item.__contains__("Result (S)"):
                            print(item)
                            result_status = item.split("Results:")[1]

                        if item.__contains__("Status") or item.__contains__("status"):
                            print(item)
                            result_status = item.split("Status:")[1]
            for i in range(len(pdf_images)):
                image_path = r"page" + str(i) + ".jpg"
                os.remove(image_path)

            # remove pdf file
            os.remove(full_path)
            dist = {
                'report_number': report_number,
                'id_number': id_number,
                'result_status': result_status
            }
            return JsonResponse(
                {'message': 'ocr Successfully ', 'success': True, 'data': dist, 'status': 200},
                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'OCr could not perform'}, status=500)

    @staticmethod
    def getOcrDocumentList(request):
        try:
            data = Ocr.objects.all()
            serializer = OcrSerializer(data, many=True)
            return JsonResponse(
                {'message': 'User Successfully Edited', 'success': True, 'data': serializer.data, 'status': 201},
                status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'OCr could not perfome'}, status=500)

    @staticmethod
    def getQualificationTest(request):
        try:
            data = qualification_test.objects.all()
            serializer = qual_testSerializer(data, many=True)
            return JsonResponse(
                {'message': 'record found', 'success': True, 'data': serializer.data, 'status': 201},
                status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)

    @staticmethod
    def deleteOcrDocument(request):
        try:
            docId = request.query_params['id']
            doc = Ocr.objects.get(id=docId)
            doc.delete()
            return JsonResponse({'message': 'Motor has been deleted'}, status=200)
        except:
            return JsonResponse({'message': 'Sorry! No Motor found.'}, status=500)

    @staticmethod
    def addQualificationTest(request):
        try:
            print(request)
            assebmlies = json.loads(request.data['Q_test'])
            for item in assebmlies:
                print(item)
                if item['value'] != '':
                    print("going to add Qualification Test")
                    modal = qualification_test()
                    modal.qualification_test = item['value']
                    modal.sub_assembly_name = request.data['sub_assembly_name']
                    modal.assembly_name = request.data['assembly_name']
                    modal.system_name = request.data['sys_name']
                    modal.system_type = request.data['sys_type']
                    modal.batch_set_id = request.data['batch_set_no']
                    modal.bhd_no = request.data['bhd_no']
                    modal.activity_type = request.data['activityType']
                    modal.title = request.data['title_name']
                    modal.date = request.data['ass_date']
                    modal.ref_criteria = request.data['reference_criteria']
                    modal.save()
                    print("Qualification Test saved")

            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def addQualificationReport(request):
        try:
            print(request)
            print("going to add Qualification Report")
            modal = qualification_ocr_report()
            sys_name = request.data['sys_name']
            sys_type = request.data['sys_type']
            qualification_test = request.data['Q_test']
            acceptance_test = request.data['acceptance_test']
            qualification_report = request.data['qualification_report']
            sub_assembly = request.data['sub_assembly_name']
            assembly = request.data['assembly_name']
            batch_no = request.data['batch_set_no']
            scanned_report_list = []
            if acceptance_test != "":
                scanned_report_list = qualification_ocr_report.objects.filter(system_type=sys_type, system_name=sys_name,
                                                                              assembly_name=assembly,
                                                                              sub_assembly_name=sub_assembly,
                                                                              acceptance_test=acceptance_test,
                                                                              batch_set_id=batch_no).first()
            elif qualification_test != "":
                scanned_report_list = qualification_ocr_report.objects.filter(system_type=sys_type, system_name=sys_name,
                                                                              assembly_name=assembly,
                                                                              sub_assembly_name=sub_assembly,
                                                                              qualification_test=qualification_test,
                                                                              batch_set_id=batch_no).first()
            else:
                scanned_report_list = qualification_ocr_report.objects.filter(system_type=sys_type, system_name=sys_name,
                                                                              assembly_name=assembly,
                                                                              sub_assembly_name=sub_assembly,
                                                                              qualification_report=qualification_report,
                                                                              batch_set_id=batch_no).first()

            if scanned_report_list is None:
                modal.ocr_report = request.data['ocr_reports']
                modal.qualification_test = request.data['Q_test']
                modal.acceptance_test = request.data['acceptance_test']
                modal.qualification_report = request.data['qualification_report']
                modal.sub_assembly_name = request.data['sub_assembly_name']
                modal.assembly_name = request.data['assembly_name']
                modal.system_name = request.data['sys_name']
                modal.system_type = request.data['sys_type']
                modal.batch_set_id = request.data['batch_set_no']
                modal.bhd_no = request.data['bhd_no']
                modal.activity_type = request.data['activityType']
                modal.title = request.data['title_name']
                modal.date = request.data['ass_date']
                modal.ref_criteria = request.data['reference_criteria']
                modal.save()
                print("Qualification Report saved")
                return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                    status=200)
            else:
                scanned_report_list.ocr_report = request.data['ocr_reports']
                scanned_report_list.qualification_test = request.data['Q_test']
                scanned_report_list.acceptance_test = request.data['acceptance_test']
                scanned_report_list.qualification_report = request.data['qualification_report']
                scanned_report_list.sub_assembly_name = request.data['sub_assembly_name']
                scanned_report_list.assembly_name = request.data['assembly_name']
                scanned_report_list.system_name = request.data['sys_name']
                scanned_report_list.system_type = request.data['sys_type']
                scanned_report_list.batch_set_id = request.data['batch_set_no']
                scanned_report_list.bhd_no = request.data['bhd_no']
                scanned_report_list.activity_type = request.data['activityType']
                scanned_report_list.title = request.data['title_name']
                scanned_report_list.date = request.data['ass_date']
                scanned_report_list.ref_criteria = request.data['reference_criteria']
                scanned_report_list.save()
                print("Qualification Report saved")
                return JsonResponse(
                    {'message': "Record updated successfully!", 'success': True, 'data': [], 'status': 200},
                    status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def getQualificationReport(request):
        try:
            data = qualification_ocr_report.objects.all()
            serializer = ocr_reportSerializer(data, many=True)
            return JsonResponse(
                {'message': 'record found', 'success': True, 'data': serializer.data, 'status': 201},
                status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)

    @staticmethod
    def bulkInsert(request):
        try:
            if request.data['file'] != '':
                excel_file = request.data['file']
                df = pd.read_excel(excel_file)
                assemblies_list = []
                sub_assemblies_list = []
                acceptance_test_list = []
                qualification_test_list = []
                qualification_reports_list = []
                curr_assembly = ''
                curr_sub_assembly = ''
                temp_data_sa = ''
                qt_list = []


                at_superList = []
                atList = []
                qt_superList = []
                qtList = []
                curr_type = ""
                qr_superList = []
                for (a, b, c) in zip(df.SrNo, df.Assembly_SubAssembly, df.QualificationTest):
                    if math.isnan(a):
                        curr_assembly = b
                        assemblies_list.append(b)
                    if b not in sub_assemblies_list:
                        curr_sub_assembly = b
                        if math.isnan(a) and math.isnan(c):
                            continue
                        else:
                            temp_data_sa = curr_assembly + '=' + b
                        if temp_data_sa not in sub_assemblies_list:
                            sub_assemblies_list.append(temp_data_sa)
                    if c != '':
                        # qt_list.append(c)
                        # temp_data_qt = curr_assembly + '=' + curr_sub_assembly + ':' + str(c)
                        # qualification_test_list.append(temp_data_qt)
                        # for item in qt_list:
                        if c == 'Acceptance Tests':
                            curr_type = c
                            continue
                        elif c == 'Qualification Tests':
                            curr_type = c
                            continue
                        elif c == 'Sample Qualification Reports':
                            curr_type = c
                            continue
                        else:
                            if curr_type == 'Acceptance Tests':
                                temp_data_qt = curr_assembly + '=' + curr_sub_assembly + ':' + str(c)
                                acceptance_test_list.append(temp_data_qt)
                                # at_superList.append(c)
                            elif curr_type == 'Qualification Tests':
                                temp_data_qt = curr_assembly + '=' + curr_sub_assembly + ':' + str(c)
                                qualification_test_list.append(temp_data_qt)
                                # qt_superList.append(c)
                            else:
                                temp_data_qt = curr_assembly + '=' + curr_sub_assembly + ':' + str(c)
                                qualification_reports_list.append(temp_data_qt)
                                # qr_superList.append(c)
                        #     if c == 'Acceptance Tests':
                        #         if atList:
                        #             at_superList.append(atList)
                        #         atList = []
                        #         curr_type = c
                        #     else:
                        #         if c == 'Qualification Tests':
                        #             if qtList:
                        #                 qt_superList.append(qtList)
                        #             qtList = []
                        #             curr_type = c
                        #         else:
                        #             if curr_type == 'Acceptance Tests':
                        #                 atList.append(c)
                        #             else:
                        #                 qtList.append(c)
                print(acceptance_test_list)
                print(qualification_test_list)
                print(qualification_reports_list)
                for item in assemblies_list:
                    # print(item)
                    if item != '':
                        check_record = batch_bhd_activity.objects.filter(system_name=request.data['sys_name'],
                                                                         batch_set_id=request.data['batch_set_no'],
                                                                         bhd_no=request.data['bhd_no'],
                                                                         activity_type=request.data[
                                                                             'activityType']).first()
                        if check_record is None:
                            row = batch_bhd_activity()
                            row.system_name = request.data['sys_name']
                            row.batch_set_id = request.data['batch_set_no']
                            row.bhd_no = request.data['bhd_no']
                            row.activity_type = request.data['activityType']
                            row.title = request.data['title_name']
                            row.date = request.data['ass_date']
                            row.ref_criteria = request.data['reference_criteria']
                            row.save()
                        print("going to add assembly")
                        # if check_record is None:
                        modal = assemblies()
                        modal.assembly_name = item
                        modal.system_name = request.data['sys_name']
                        modal.system_type = request.data['sys_type']
                        modal.batch_set_id = request.data['batch_set_no']
                        modal.bhd_no = request.data['bhd_no']
                        modal.activity_type = request.data['activityType']
                        modal.title = request.data['title_name']
                        modal.date = request.data['ass_date']
                        modal.ref_criteria = request.data['reference_criteria']
                        modal.save()
                        print("assembly saved")
                for item in sub_assemblies_list:
                    # print(item)
                    if item != '':
                        print("going to add sub assembly")
                        modal = sub_assemblies()
                        curr_ass = ''
                        curr_sub_ass = ''
                        if item.__contains__("="):
                            print(item)
                            curr_ass = item.split("=")[0]
                            curr_sub_ass = item.split("=")[1]
                        modal.assembly_name = curr_ass
                        modal.sub_assembly_name = curr_sub_ass
                        modal.system_name = request.data['sys_name']
                        modal.system_type = request.data['sys_type']
                        modal.batch_set_id = request.data['batch_set_no']
                        modal.bhd_no = request.data['bhd_no']
                        modal.activity_type = request.data['activityType']
                        modal.title = request.data['title_name']
                        modal.date = request.data['ass_date']
                        modal.ref_criteria = request.data['reference_criteria']
                        modal.save()
                        print("sub assembly saved")

                for item in acceptance_test_list:
                    # print(item)
                    if item != '':
                        print("going to add Acceptance Test")
                        modal = acceptance_test()
                        curr_ass = ''
                        curr_sub_ass = ''
                        curr_at = ''
                        temp = ''
                        if item.__contains__("="):
                            # print(item)
                            curr_ass = item.split("=")[0]
                            temp = item.split("=")[1]
                        if temp.__contains__(":"):
                            curr_sub_ass = temp.split(":")[0]
                            curr_at = temp.split(":")[1]
                        modal.sub_assembly_name = curr_sub_ass
                        modal.assembly_name = curr_ass
                        modal.system_name = request.data['sys_name']
                        modal.system_type = request.data['sys_type']
                        modal.acceptance_test = curr_at
                        modal.batch_set_id = request.data['batch_set_no']
                        modal.bhd_no = request.data['bhd_no']
                        modal.activity_type = request.data['activityType']
                        modal.title = request.data['title_name']
                        modal.date = request.data['ass_date']
                        modal.ref_criteria = request.data['reference_criteria']
                        modal.save()
                        print("Acceptance Test saved")
                for item in qualification_test_list:
                    # print(item)
                    if item != '':
                        print("going to add Qualification Test")
                        modal = qualification_test()
                        curr_ass = ''
                        curr_sub_ass = ''
                        curr_qt = ''
                        temp = ''
                        if item.__contains__("="):
                            # print(item)
                            curr_ass = item.split("=")[0]
                            temp = item.split("=")[1]
                        if temp.__contains__(":"):
                            curr_sub_ass = temp.split(":")[0]
                            curr_qt = temp.split(":")[1]
                        modal.sub_assembly_name = curr_sub_ass
                        modal.assembly_name = curr_ass
                        modal.system_name = request.data['sys_name']
                        modal.system_type = request.data['sys_type']
                        modal.qualification_test = curr_qt
                        modal.batch_set_id = request.data['batch_set_no']
                        modal.bhd_no = request.data['bhd_no']
                        modal.activity_type = request.data['activityType']
                        modal.title = request.data['title_name']
                        modal.date = request.data['ass_date']
                        modal.ref_criteria = request.data['reference_criteria']
                        modal.save()
                        print("Qualification Test saved")
                for item in qualification_reports_list:
                    # print(item)
                    if item != '':
                        print("going to add Qualification Reports")
                        modal = sample_qualification_reports()
                        curr_ass = ''
                        curr_sub_ass = ''
                        curr_qr = ''
                        temp = ''
                        if item.__contains__("="):
                            # print(item)
                            curr_ass = item.split("=")[0]
                            temp = item.split("=")[1]
                        if temp.__contains__(":"):
                            curr_sub_ass = temp.split(":")[0]
                            curr_qr = temp.split(":")[1]
                        modal.sub_assembly_name = curr_sub_ass
                        modal.assembly_name = curr_ass
                        modal.system_name = request.data['sys_name']
                        modal.system_type = request.data['sys_type']
                        modal.sample_qualification_reports = curr_qr
                        modal.batch_set_id = request.data['batch_set_no']
                        modal.bhd_no = request.data['bhd_no']
                        modal.activity_type = request.data['activityType']
                        modal.title = request.data['title_name']
                        modal.date = request.data['ass_date']
                        modal.ref_criteria = request.data['reference_criteria']
                        modal.save()
                        print("Qualification Reports saved")
            else:
                check_record = batch_bhd_activity.objects.filter(system_name=request.data['sys_name'],
                                                                 batch_set_id=request.data['batch_set_no']).first()
                if check_record is None:
                    row = batch_bhd_activity()
                    row.system_name = request.data['sys_name']
                    row.batch_set_id = request.data['batch_set_no']
                    row.bhd_no = request.data['bhd_no']
                    row.activity_type = request.data['activityType']
                    row.title = request.data['title_name']
                    row.date = request.data['ass_date']
                    row.ref_criteria = request.data['reference_criteria']
                    row.save()
            return JsonResponse({'message': "Record added", 'success': True, 'data': [], 'status': 200},
                                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': "User do not created !", 'success': False, 'data': [], 'status': 500},
                                status=500)

    @staticmethod
    def reportCheck(request):
        try:
            def save_file(file: InMemoryUploadedFile, full_path):
                with open(full_path, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

            report_number = ''
            id_number = ''
            results = ''
            status = ''
            qaualification_criteria = ''
            fs = FileSystemStorage()
            if not os.path.isdir('myScannedReports'):
                os.mkdir('myScannedReports')
            # open file
            file: InMemoryUploadedFile = request['file']
            batch_no = request['batch_no']
            report_observation = request['report_observation']
            report_remarks = request['report_remarks']
            idNumber = request['id_number']
            # define file_save_path variable
            # full_path = str(datetime.today()).replace('-', '').replace(' ', '') + '_' + file.name
            full_path = file.name
            save_file(file, full_path)
            target_path = 'myScannedReports/'
            shutil.copy(full_path, target_path)
            prefix = ''.join(random.choice(string.ascii_letters) for i in range(10))
            oldFilePath = target_path + full_path
            newFileName = batch_no + '_' + prefix + '_' + full_path
            newFIlePath = target_path + newFileName
            os.rename(oldFilePath, newFIlePath)

            pdf_images = convert_from_path(full_path)
            for i in range(len(pdf_images)):
                # Save pages as images in the pdf
                pdf_images[i].save('page' + str(i) + '.jpg', 'JPEG')

            # load all images and extract text from each page
            mydist = {}
            for i in range(len(pdf_images)):
                if i == 0:
                    # path_to_tesseract = "/usr/bin/tesseract"  # r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                    path_to_tesseract = r"\usr\bin\tesseract"
                    image_path = r"page" + str(i) + ".jpg"  # r"page0.jpg"
                    img = Image.open(image_path)
                    pytesseract.tesseract_cmd = path_to_tesseract
                    text = pytesseract.image_to_string(img)
                    data = text.split("\n")
                    final_list = data  # [y for x in data for y in x.split(':')]
                    print(final_list)

                    for item in final_list:
                        if item.__contains__("Product Delivery Form (PDF)") or item.__contains__(
                                "Product Delivery Form"):
                            return JsonResponse(
                                {'message': 'Report not found', 'success': False, 'data': dict, 'status': 403},
                                status=403)
                        else:
                            # print("report is not Product Delivery Form ")
                            if item.__contains__("ID No:") or item.__contains__("id no:") or item.__contains__(
                                    "ID No.") or item.__contains__("id no.") or item.__contains__(
                                    "ID No.") or item.__contains__("ID NO") or item.__contains__(
                                    "ID NO.") or item.__contains__("Part ID") or item.__contains__(
                                    "Cable Analyzer ID") or item.__contains__("ID#") or item.__contains__(
                                    "Sample ID") or item.__contains__("Identity No") or item.__contains__(
                                    "Identity No.") or item.__contains__("Module Name & ID No.") or item.__contains__(
                                    "Module Name & ID No"):
                                print(item)
                                id_number = item.split(":")[item.split(":").__len__() - 1]
                            if item.__contains__("Test Report No:") or item.__contains__(
                                    "test report no.") or item.__contains__("Test Report No:") or item.__contains__(
                                    "test report no:") or item.__contains__("Test Report No.") or item.__contains__(
                                    "Test Report No") or item.__contains__("Report Number") or item.__contains__(
                                    "Report #") or item.__contains__("Report ID") or item.__contains__(
                                    "Report ID.") or item.__contains__("Report Id") or item.__contains__(
                                    "Report Id.") or item.__contains__("Report No") or item.__contains__("Report No."):
                                print(item)
                                report_number = item.split(":")[item.split(":").__len__() - 1]
                            # if item.__contains__("Status:") or item.__contains__("test report no."):
                            #     print(item)
                            #     id_number = item.split("Test Report No:")[1]
                            if item.__contains__("Status") or item.__contains__("status"):
                                print(item)
                                status = item.split(":")[item.split(":").__len__() - 1]

                            if item.__contains__("Qualification Criteria") or item.__contains__(
                                    "Qualiﬁcation Standard") or item.__contains__(
                                    "Compliance Statement") or item.__contains__(
                                    "Qualification Standard") or item.__contains__(
                                    "Qualification Standard | ") or item.__contains__(
                                    "Qualification Procedure") or item.__contains__(
                                    "Qualification/Acceptance Criteria") or item.__contains__(
                                    "Qualification/Accep. Criteria") or item.__contains__(
                                    "Qualification / Acceptance Criteria") or item.__contains__(
                                    "Qualification / Accep. Criteria") or item.__contains__(
                                    "Test Criteria/Standard") or item.__contains__(
                                    "Test Criteria / Standard") or item.__contains__("Reference") or item.__contains__(
                                    "Ref. Document No.") or item.__contains__("Ref Document No") or item.__contains__(
                                    "Acceptance Criteria No./Dwg.No.") or item.__contains__(
                                    "Acceptance Criteria No. / Dwg.No."):
                                print(item)
                                if item.__contains__("Qualification Standard | "):
                                    qaualification_criteria = item.split(" | ")[item.split(" | ").__len__() - 1]
                                elif item.__contains__("Qualiﬁcation Standard"):
                                    qaualification_criteria = item.split("Qualiﬁcation Standard")[
                                        item.split("Qualiﬁcation Standard").__len__() - 1]
                                else:
                                    qaualification_criteria = item.split(":")[item.split(":").__len__() - 1]

                            if item.__contains__("Results") or item.__contains__("results") or item.__contains__(
                                    "Results") or item.__contains__("results") or item.__contains__(
                                    "Test Results") or item.__contains__("Test Result") or item.__contains__(
                                    "Expert") or item.__contains__("Review") or item.__contains__(
                                    "Results") or item.__contains__("Result") or item.__contains__(
                                    "Status") or item.__contains__("Measurement Status") or item.__contains__(
                                    "Result(s)") or item.__contains__("Result (s)") or item.__contains__(
                                    "Result(S)") or item.__contains__("Result (S)"):
                                print(item)
                                # results = item.split("Results ® ")[1]
                                if item.split("Results 0 ").__len__() == 1:
                                    if item.split("Results ® ").__len__()>1:
                                        results = item.split("Results ® ")[1]
                                else:
                                    if item.split("Results 0 ")[1].__len__():
                                        results = item.split("Results 0 ")[1]

                                break

            print("report scan going to remove images")
            for i in range(len(pdf_images)):
                image_path = r"page" + str(i) + ".jpg"
                os.remove(image_path)

            # remove pdf file
            os.remove(full_path)
            dict = ""
            print("going to match id num")
            print("id number is ", idNumber)
            if idNumber == id_number.lstrip():
                dict = {
                    'results': results,
                    'report_number': report_number,
                    'id_number': id_number,
                    'report_url': newFileName,
                    'file_absolute_url': os.path.abspath(newFIlePath),
                    'observation': report_observation,
                    'remarks': report_remarks,
                    'qaualification_criteria': qaualification_criteria
                }
                return JsonResponse(
                    {'message': 'Report found ', 'success': True, 'data': dict, 'status': 200},
                    status=200)
            else:
                return JsonResponse(
                    {'message': 'Report not found ', 'success': False, 'data': [], 'status': 403},
                    status=403)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'OCr could not perform'}, status=500)

    @staticmethod
    def reportCheck_v2(request):
        try:
            def save_file(file: InMemoryUploadedFile, full_path):
                with open(full_path, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

            report_number = ''
            id_number = ''
            results = ''
            status = ''
            qaualification_criteria = ''
            fs = FileSystemStorage()
            if not os.path.isdir('myScannedReports'):
                os.mkdir('myScannedReports')
            # open file
            #file: InMemoryUploadedFile = request['file']
            batch_no = request['batch_no']
            report_observation = request['report_observation']
            report_remarks = request['report_remarks']
            idNumber = request['id_number']
            if idNumber == "RD-19C (a)":

                # directory name 1. S1A-Prod-06 BHD
                # scan PDF directory
                # get all files in a directory python
                arr = os.listdir('reports/Reports/PDF')
                print(arr)
                count = 0
                for single_pdf in arr:
                    report_number = ''
                    results = ''
                    status = ''
                    count = count +1
                    print("report scenned", count)
                    pdf_images = convert_from_path("reports/Reports/PDF/" +single_pdf)
                    for i in range(len(pdf_images)):
                        # Save pages as images in the pdf
                        pdf_images[i].save('page' + str(i) + '.jpg', 'JPEG')

                    # load all images and extract text from each page
                    mydist = {}
                    for i in range(len(pdf_images)):
                        if i == 0:
                            # path_to_tesseract = "/usr/bin/tesseract"  # r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                            path_to_tesseract = r"\usr\bin\tesseract"
                            image_path = r"page" + str(i) + ".jpg"  # r"page0.jpg"
                            img = Image.open(image_path)
                            pytesseract.tesseract_cmd = path_to_tesseract
                            text = pytesseract.image_to_string(img)
                            data = text.split("\n")
                            final_list = data  # [y for x in data for y in x.split(':')]
                            print(final_list)

                            for item in final_list:
                                if item.__contains__("Product Delivery Form (PDF)") or item.__contains__(
                                        "Product Delivery Form"):
                                    print("")
                                    # return JsonResponse(
                                    #     {'message': 'Report not found', 'success': False, 'data': dict, 'status': 403},
                                    #     status=403)
                                else:
                                    # print("report is not Product Delivery Form ")
                                    if item.__contains__("ID No:") or item.__contains__("id no:") or item.__contains__(
                                            "ID No.") or item.__contains__("id no.") or item.__contains__(
                                        "ID No.") or item.__contains__("ID NO") or item.__contains__(
                                        "ID NO.") or item.__contains__("Part ID") or item.__contains__(
                                        "Cable Analyzer ID") or item.__contains__("ID#") or item.__contains__(
                                        "Sample ID") or item.__contains__("Identity No") or item.__contains__(
                                        "Identity No.") or item.__contains__(
                                        "Module Name & ID No.") or item.__contains__(
                                        "Module Name & ID No"):
                                        print(item)
                                        id_number = item.split(":")[item.split(":").__len__() - 1]
                                    if item.__contains__("Test Report No:") or item.__contains__(
                                            "test report no.") or item.__contains__(
                                        "Test Report No:") or item.__contains__(
                                        "test report no:") or item.__contains__("Test Report No.") or item.__contains__(
                                        "Test Report No") or item.__contains__("Report Number") or item.__contains__(
                                        "Report #") or item.__contains__("Report ID") or item.__contains__(
                                        "Report ID.") or item.__contains__("Report Id") or item.__contains__(
                                        "Report Id.") or item.__contains__("Report No") or item.__contains__(
                                        "Report No."):
                                        print(item)
                                        report_number = item.split(":")[item.split(":").__len__() - 1]
                                    # if item.__contains__("Status:") or item.__contains__("test report no."):
                                    #     print(item)
                                    #     id_number = item.split("Test Report No:")[1]
                                    if item.__contains__("Status") or item.__contains__("status"):
                                        print(item)
                                        status = item.split(":")[item.split(":").__len__() - 1]

                                    if item.__contains__("Qualification Criteria") or item.__contains__(
                                            "Qualiﬁcation Standard") or item.__contains__(
                                        "Compliance Statement") or item.__contains__(
                                        "Qualification Standard") or item.__contains__(
                                        "Qualification Standard | ") or item.__contains__(
                                        "Qualification Procedure") or item.__contains__(
                                        "Qualification/Acceptance Criteria") or item.__contains__(
                                        "Qualification/Accep. Criteria") or item.__contains__(
                                        "Qualification / Acceptance Criteria") or item.__contains__(
                                        "Qualification / Accep. Criteria") or item.__contains__(
                                        "Test Criteria/Standard") or item.__contains__(
                                        "Test Criteria / Standard") or item.__contains__(
                                        "Reference") or item.__contains__(
                                        "Ref. Document No.") or item.__contains__(
                                        "Ref Document No") or item.__contains__(
                                        "Acceptance Criteria No./Dwg.No.") or item.__contains__(
                                        "Acceptance Criteria No. / Dwg.No."):
                                        print(item)
                                        if item.__contains__("Qualification Standard | "):
                                            qaualification_criteria = item.split(" | ")[item.split(" | ").__len__() - 1]
                                        elif item.__contains__("Qualiﬁcation Standard"):
                                            qaualification_criteria = item.split("Qualiﬁcation Standard")[
                                                item.split("Qualiﬁcation Standard").__len__() - 1]
                                        else:
                                            qaualification_criteria = item.split(":")[item.split(":").__len__() - 1]

                                    if item.__contains__("Results") or item.__contains__(
                                            "results") or item.__contains__(
                                            "Results") or item.__contains__("results") or item.__contains__(
                                        "Test Results") or item.__contains__("Test Result") or item.__contains__(
                                        "Expert") or item.__contains__("Review") or item.__contains__(
                                        "Results") or item.__contains__("Result") or item.__contains__(
                                        "Status") or item.__contains__("Measurement Status") or item.__contains__(
                                        "Result(s)") or item.__contains__("Result (s)") or item.__contains__(
                                        "Result(S)") or item.__contains__("Result (S)"):
                                        print(item)
                                        # results = item.split("Results ® ")[1]
                                        if item.split("Results 0 ").__len__() == 1:
                                            if item.split("Results ® ").__len__() > 1:
                                                results = item.split("Results ® ")[1]
                                        else:
                                            if item.split("Results 0 ")[1].__len__():
                                                results = item.split("Results 0 ")[1]

                                        break

                    print("report scan going to remove images")
                    for i in range(len(pdf_images)):
                        image_path = r"page" + str(i) + ".jpg"
                        os.remove(image_path)

                    # remove pdf file
                    #os.remove(full_path)
                    dict = ""
                    print("going to match id num")
                    print("id number is ", idNumber)
                    print("id from pdf is ", id_number)
                    print("report name ", single_pdf)
                    if idNumber == id_number.lstrip():
                        dict = {
                            'results': results,
                            'report_number': report_number,
                            'id_number': id_number,
                            'report_url': '',
                            'file_absolute_url': '',
                            'observation': report_observation,
                            'remarks': report_remarks,
                            'qaualification_criteria': qaualification_criteria
                        }
                        return JsonResponse(
                            {'message': 'Report found ', 'success': True, 'data': dict, 'status': 200},
                            status=200)
                    # else:
                    #     return JsonResponse(
                    #         {'message': 'Report not found ', 'success': False, 'data': [], 'status': 403},
                    #         status=403)

            # define file_save_path variable
            # full_path = str(datetime.today()).replace('-', '').replace(' ', '') + '_' + file.name
            #full_path = file.name
            # #save_file(file, full_path)
            # target_path = 'myScannedReports/'
            # shutil.copy(full_path, target_path)
            # prefix = ''.join(random.choice(string.ascii_letters) for i in range(10))
            # oldFilePath = target_path + full_path
            # newFileName = batch_no + '_' + prefix + '_' + full_path
            # newFIlePath = target_path + newFileName
            # os.rename(oldFilePath, newFIlePath)

            return JsonResponse(
                {'message': 'Report found ', 'success': True, 'data': {}, 'status': 200},
                status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'OCr could not perform'}, status=500)

    @staticmethod
    def getTreeData(request):
        try:
            system_type = request.query_params['system_type']
            system_name = request.query_params['system_name']

            ass_data = assemblies.objects.filter(system_type=system_type, system_name=system_name)
            ass_serializer = assembliesSerializer(ass_data, many=True)
            ass_tree_data = ass_serializer.data

            sa_data = sub_assemblies.objects.filter(system_type=system_type, system_name=system_name)
            sa_serializer = sub_assembliesSerializer(sa_data, many=True)
            sa_tree_data = sa_serializer.data

            at_data = acceptance_test.objects.filter(system_type=system_type, system_name=system_name)
            at_serializer = acceptance_testSerializer(at_data, many=True)
            at_tree_data = at_serializer.data

            qt_data = qualification_test.objects.filter(system_type=system_type, system_name=system_name)
            qt_serializer = qual_testSerializer(qt_data, many=True)
            qt_tree_data = qt_serializer.data

            qr_data = sample_qualification_reports.objects.filter(system_type=system_type, system_name=system_name)
            qr_serializer = sample_qualification_reportSerializer(qr_data, many=True)
            qr_tree_data = qr_serializer.data
            tree_data = {
                'assemblies': ass_tree_data,
                'sub_assemblies': sa_tree_data,
                'acceptance_tests': at_tree_data,
                'qualification_test': qt_tree_data,
                'qualification_reports': qr_tree_data
            }
            return JsonResponse(
                {'message': 'record found', 'success': True, 'data': tree_data, 'status': 201},
                status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)

    @staticmethod
    def getScannedQualificationReportList(request):
        try:
            system_type = request.query_params['system_type']
            system_name = request.query_params['system_name']
            assembly = request.query_params['assembly']
            sub_assembly = request.query_params['sub_assembly']
            qualification_test = request.query_params['qualification_test']
            acceptance_test = request.query_params['acceptance_test']
            qualification_report = request.query_params['qualification_report']
            batch_no = request.query_params['batch_no']
            data = ""
            if acceptance_test != "":
                data = qualification_ocr_report.objects.filter(system_type=system_type, system_name=system_name,
                                                               assembly_name=assembly, sub_assembly_name=sub_assembly,
                                                               acceptance_test=acceptance_test,
                                                               batch_set_id=batch_no).first()
            elif qualification_test != "":
                data = qualification_ocr_report.objects.filter(system_type=system_type, system_name=system_name,
                                                               assembly_name=assembly, sub_assembly_name=sub_assembly,
                                                               qualification_test=qualification_test,
                                                               batch_set_id=batch_no).first()
            else:
                data = qualification_ocr_report.objects.filter(system_type=system_type, system_name=system_name,
                                                               assembly_name=assembly, sub_assembly_name=sub_assembly,
                                                               qualification_report=qualification_report,
                                                               batch_set_id=batch_no).first()
            reference_criteria = ''
            ocr_data = ''
            if data is None:
                ocr_data = ''
            else:
                ocr_data = data.ocr_report
                reference_criteria = data.ref_criteria
            return JsonResponse(
                {'message': 'record found', 'success': True, 'data': ocr_data, 'ref_criteria': reference_criteria,
                 'status': 201},
                status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)

    @staticmethod
    def downloadFile(request):
        try:
            url = request.query_params['url']
            # response = requests.get(url)
            selected_file = ''
            if url.__contains__("myScannedReports/"):
                selected_file = url.split("myScannedReports/")[1]

            with open(url, 'rb') as f:
                file_data = f.read()
                ext = os.path.splitext(selected_file)[1][1:].strip().lower()
                new_file_name = selected_file  # + str(uuid.uuid4().hex[:8])

                response = HttpResponse(file_data, content_type='application/force-download')
                response['Content-Disposition'] = "attachment; filename=" + selected_file
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return response

            # return response
            # print(fileReader)
            # return JsonResponse(
            #         {'message': 'record found', 'success': True, 'data': [], 'status': 403},
            #         status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)

    @staticmethod
    def checkBatchNo(request):
        try:
            system_type = request.query_params['system_type']
            system_name = request.query_params['system_name']
            data = assemblies.objects.filter(system_name=system_name).first()
            if data is None:
                return JsonResponse(
                    {'message': 'record found', 'success': False, 'data': [], 'status': 201},
                    status=201)
            else:
                return JsonResponse(
                    {'message': 'record found', 'success': True, 'data': [], 'status': 403},
                    status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)

    @staticmethod
    def getBatchList(request):
        try:

            data = batch_bhd_activity.objects.all()
            serializer = getSetIdsBhdActivitySerializer(data, many=True)

            if data is not None:
                return JsonResponse(
                    {'message': 'record found', 'success': False, 'data': serializer.data, 'status': 201},
                    status=201)
            else:
                return JsonResponse(
                    {'message': 'record found', 'success': True, 'data': [], 'status': 403},
                    status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)
