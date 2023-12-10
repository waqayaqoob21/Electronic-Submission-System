import json

from django.http import JsonResponse
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

import os, shutil
import fitz
import io
import pandas as pd
import itertools
import math

from .serializers import OcrSerializer, assembliesSerializer, sub_assembliesSerializer, qual_testSerializer, \
    getSetIdsBhdActivitySerializer, ocr_reportSerializer


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
            if system_type != '' :
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

                        if item.__contains__("Test Report No:") or item.__contains__("test report no:"):
                            print(item)
                            report_number = item.split(":")[1]
                        if item.__contains__("ID No.") or item.__contains__("id no."):
                            print(item)
                            id_number = item.split("ID No.:")[1]
                        if item.__contains__("Results") or item.__contains__("results"):
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
            # item['value']
            modal.ocr_report = request.data['ocr_reports']
            modal.qualification_test = request.data['Q_test']
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
            excel_file = request.data['file']
            df = pd.read_excel(excel_file)
            assemblies_list = []
            sub_assemblies_list = []
            qualification_test_list = []
            curr_assembly = ''
            curr_sub_assembly = ''
            temp_data_sa = ''
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
                    temp_data_qt = curr_assembly + '=' + curr_sub_assembly + ':' + str(c)
                    qualification_test_list.append(temp_data_qt)

            for item in assemblies_list:
                # print(item)
                if item != '':
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
                    modal.qualification_test = curr_qt
                    modal.sub_assembly_name = curr_sub_ass
                    modal.assembly_name = curr_ass
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
    def getTreeData(request):
        try:
            system_type = request.query_params['system_type']
            system_name = request.query_params['system_name']
            # tree_data = []
            # cm_cursor = connection.cursor()
            # cm_query = "SELECT ocr.system_type,ocr.system_name,ocr.activity_type,ocr.batch_set_id,ocr.title," \
            #            "ocr.bhd_no,ocr.ref_criteria,ocr.date,ass.assembly_name,sub.sub_assembly_name,qt.qualification_test " \
            #            "FROM reportocr_qualification_ocr_report ocr " \
            #            "RIGHT JOIN reportocr_assemblies ass ON ass.system_name = ocr.system_name " \
            #            "INNER JOIN reportocr_sub_assemblies sub ON sub.assembly_name = ass.assembly_name " \
            #            "INNER JOIN reportocr_qualification_test qt ON qt.sub_assembly_name = sub.sub_assembly_name "\
            #            "WHERE qt.system_type = '"+system_type+"' and qt.system_name= '"+system_name+"' ORDER BY qt.id ASC;"
            # # data = Videos.objects.filter(user_id=id, is_pending=True)
            # # if data:
            # #     serializer = VideoSerializer(data, many=True)
            # cm_cursor.execute(cm_query)
            # cm_col_names = [col[0] for col in cm_cursor.description]
            # for row in cm_cursor.fetchall():
            #     row_dict = dict(zip(cm_col_names, row))
            #     print(row_dict)
            #     tree_data.append(row_dict)
            ass_data = assemblies.objects.filter(system_type = system_type, system_name = system_name)
            ass_serializer = assembliesSerializer(ass_data, many=True)
            ass_tree_data = ass_serializer.data

            sa_data = sub_assemblies.objects.filter(system_type = system_type, system_name = system_name)
            sa_serializer = sub_assembliesSerializer(sa_data, many=True)
            sa_tree_data = sa_serializer.data

            qt_data = qualification_test.objects.filter(system_type = system_type, system_name = system_name)
            qt_serializer = qual_testSerializer(qt_data, many=True)
            qt_tree_data = qt_serializer.data
            tree_data = {
                'assemblies': ass_tree_data,
                'sub_assemblies': sa_tree_data,
                'qualification_test': qt_tree_data
            }
            return JsonResponse(
                {'message': 'record found', 'success': True, 'data': tree_data, 'status': 201},
                status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Server Error'}, status=500)