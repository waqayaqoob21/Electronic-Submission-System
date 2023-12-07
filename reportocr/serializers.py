from rest_framework import serializers
from .models import Ocr, assemblies, sub_assemblies, qualification_test, batch_bhd_activity, qualification_ocr_report


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


class qual_testSerializer(serializers.ModelSerializer):
    class Meta:
        model = qualification_test
        fields = '__all__'


class ocr_reportSerializer(serializers.ModelSerializer):
    class Meta:
        model = qualification_ocr_report
        fields = '__all__'


class getSetIdsBhdActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = batch_bhd_activity
        fields = '__all__'
