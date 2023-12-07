from django.db import models

class Ocr(models.Model):
    # DOCUMENT_TYPE_CHOICES = [
    #     ('BHD', 'BHD'),
    #     ('BHD1', 'BHD1'),
    # ]choices=DOCUMENT_TYPE_CHOICES
    document_type = models.CharField(max_length=300 )
    BHD_No = models.CharField(max_length=300)
    Job_Card_No = models.CharField(max_length=300)
    Dated = models.DateTimeField(auto_now_add=False, null=True)
    sys_type = models.CharField(max_length=300,null=True)
    sys_name = models.CharField(max_length=300,null=True)
    Type_of_System = models.CharField(max_length=300)
    Batch_Set_NO = models.CharField(max_length=300)
    Ref_Criteria = models.CharField(max_length=300)
    Type_of_activity = models.CharField(max_length=300)
    Status = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class assemblies(models.Model):
    id = models.AutoField(primary_key=True)
    system_type = models.CharField(max_length=300)
    system_name = models.CharField(max_length=300)
    assembly_name = models.CharField(max_length=300)
    batch_set_id = models.CharField(max_length=300, null=True)
    bhd_no = models.CharField(max_length=300, null=True)
    activity_type = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    ref_criteria = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)


class sub_assemblies(models.Model):
    id = models.AutoField(primary_key=True)
    system_type = models.CharField(max_length=300)
    system_name = models.CharField(max_length=300)
    assembly_name = models.CharField(max_length=300)
    sub_assembly_name = models.CharField(max_length=300)
    batch_set_id = models.CharField(max_length=300, null=True)
    bhd_no = models.CharField(max_length=300, null=True)
    activity_type = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    ref_criteria = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)


class qualification_test(models.Model):
    id = models.AutoField(primary_key=True)
    system_type = models.CharField(max_length=300)
    system_name = models.CharField(max_length=300)
    assembly_name = models.CharField(max_length=300)
    sub_assembly_name = models.CharField(max_length=300)
    qualification_test = models.CharField(max_length=300)
    batch_set_id = models.CharField(max_length=300, null=True)
    bhd_no = models.CharField(max_length=300, null=True)
    activity_type = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    ref_criteria = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)



class batch_bhd_activity(models.Model):
    id = models.AutoField(primary_key=True)
    system_name = models.CharField(max_length=300)
    batch_set_id = models.CharField(max_length=300, null=True)
    bhd_no = models.CharField(max_length=300, null=True)
    activity_type = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    ref_criteria = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)


class qualification_ocr_report(models.Model):
    id = models.AutoField(primary_key=True)
    system_type = models.CharField(max_length=300)
    system_name = models.CharField(max_length=300)
    assembly_name = models.CharField(max_length=300)
    sub_assembly_name = models.CharField(max_length=300)
    qualification_test = models.CharField(max_length=300)
    batch_set_id = models.CharField(max_length=300, null=True)
    bhd_no = models.CharField(max_length=300, null=True)
    activity_type = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=300, null=True)
    ref_criteria = models.CharField(max_length=300, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)
    ocr_report = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
