from rest_framework import serializers
from .models import *


class OcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocr
        fields = '__all__'


class assembliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = assemblies
        fields = '__all__'


class sub_assembliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = sub_assemblies
        fields = '__all__'


class acceptance_testSerializer(serializers.ModelSerializer):
    class Meta:
        model = acceptance_test
        fields = '__all__'

class qual_testSerializer(serializers.ModelSerializer):
    class Meta:
        model = qualification_test
        fields = '__all__'

class sample_qualification_reportSerializer(serializers.ModelSerializer):
    class Meta:
        model = sample_qualification_reports
        fields = '__all__'
class ocr_reportSerializer(serializers.ModelSerializer):
    class Meta:
        model = qualification_ocr_report
        fields = '__all__'


class getSetIdsBhdActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = batch_bhd_activity
        fields = '__all__'
