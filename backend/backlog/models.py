
from django.db import models


class Femast(models.Model):
    id = models.ForeignKey('Jobhdr', on_delete=models.CASCADE, primary_key=True, db_column='ID', blank=True, null=True)
    fe_type = models.CharField(max_length=50, blank=True, null=True)
    fe_key = models.CharField(max_length=50, blank=True, null=True)
    fe_desc = models.CharField(max_length=200, blank=True, null=True)
    vet_flag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'r_femast'
        verbose_name_plural = 'FEMAST'

    def __str__(self):
        return self.fe_key


class Userrg(models.Model):
    user_id = models.ForeignKey('Jobhdr', on_delete=models.CASCADE, db_column='USER_ID', blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'r_userrg'
        verbose_name_plural = 'Users Table'

    def __str__(self):
        return self.user_name


class Jobhdr(models.Model):
    job_num = models.IntegerField(primary_key=True, db_column='JOB_NUM', blank=True, null=True)
    fe_id = models.IntegerField(blank=True, null=True)
    f_id = models.IntegerField(db_column='F_ID', blank=True, null=True)
    job_status = models.CharField(max_length=6, blank=True, null=True)
    work_type = models.CharField(max_length=6, blank=True, null=True)
    pri_code = models.CharField(max_length=6, blank=True, null=True)
    target_end_date = models.DateTimeField(blank=True, null=True)
    next_step = models.CharField(max_length=6, blank=True, null=True)
    ser_code = models.IntegerField(blank=True, null=True)
    rqtr = models.CharField(db_column='RQTR', max_length=6, blank=True, null=True)
    rqt_date = models.DateTimeField(blank=True, null=True)
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    plan_start_date = models.DateTimeField(blank=True, null=True)
    tot_est_lab_amt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  
        db_tablespace = "DLDATA"
        db_table = 'R_JOBHDR'
        verbose_name_plural = 'JOBHDR Jobs'

    def __str__(self) -> str:
        return str(self.job_num) + " - " + self.job_status


class Estmis(models.Model):
    rqt_no = models.ForeignKey(Jobhdr, on_delete=models.CASCADE, primary_key=True, db_column='RQT_NO', unique=False, blank=True, null=True)
    unit_rate = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    task_num = models.IntegerField(blank=True, null=True)
    ref_desc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'R_ESTMIS'
        verbose_name_plural = 'Estmis'

    def __str__(self) -> str:
        return self.rqt_no


class Jobtas(models.Model):
    job_num = models.ForeignKey(Jobhdr, on_delete=models.CASCADE, primary_key=True, db_column='JOB_NUM', unique=False, blank=True, null=True)
    task_num = models.IntegerField(blank=True, null=True)
    task_status = models.CharField(max_length=6, blank=True, null=True)
    task_title = models.CharField(max_length=100, blank=True, null=True)
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    plan_start_date = models.DateTimeField(blank=True, null=True)
    target_end_date = models.DateTimeField(blank=True, null=True)
    work_order_id = models.IntegerField(blank=True, null=True)
    fin_unit_code = models.CharField(max_length=6, blank=True, null=True)
    assurance_task = models.CharField(max_length=6, blank=True, null=True)
    prod_crit_eqpt = models.CharField(max_length=6, blank=True, null=True)
    est_lab_amt = models.IntegerField(blank=True, null=True)
    ja_orgn_id = models.ForeignKey('Orgtbl', on_delete=models.CASCADE, db_column='JA_ORGN_ID', blank=True, null=True)
    est_misc_amt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'r_jobtas'
        verbose_name_plural = 'JOBTAS Jobs'

    def __str__(self) -> str:
        return str(self.task_status) + " - " + self.task_title


class Orgtbl(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID', blank=True, null=True)
    orgn_code = models.CharField(max_length=100, db_column='ORGN_CODE', blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'r_orgtbl'
        verbose_name_plural = 'Organization Code'

    def __str__(self):
        return self.orgn_code


# class Dept(models.Model):
#     DEPT = (
#         ('PCM', 'PCM'),
#         ('PCN-B', 'PCN-B'),
#         ('PCN-C', 'PCN-C'),
#         ('PGM', 'PGM'),
#         ('PIC', 'PIC'),
#         ('PII', 'PII'),
#         ('PIQ', 'PIQ'),
#         ('PIR', 'PIR'),
#         ('PMF', 'PMF'),
#         ('PMI', 'PMI'),
#         ('PMS', 'PMS'),
#         ('PMN', 'PMN'),
#         ('PMT', 'PMT'),
#         ('PMW', 'PMW'),
#         ('PTM-D', 'PTM-D'),
#         ('PTM-E', 'PTM-E'),
#         ('TPP', 'TPP'),
#         ('HSE', 'HSE'),
#     )
#     orgtbl = models.ForeignKey(Orgtbl, on_delete=models.CASCADE)
#     dept = models.CharField(max_length=10, choices=DEPT, blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Departments'

#     def __str__(self):
#         return self.dept


class Feasoc(models.Model):
    parent_fe_id = models.ForeignKey(Femast, on_delete=models.CASCADE, db_column='PARENT_FE_ID', related_name='parent', blank=True, null=True)
    child_fe_id = models.ForeignKey(Femast, on_delete=models.CASCADE, db_column='CHILD_FE_ID', related_name='child', blank=True, null=True)
    vet_flag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False  
        db_table = 'r_feasoc'
        verbose_name_plural = 'FEASOC'

    def __str__(self):
        return self.parent_fe_id



# class Jobhdtas(models.Model):
#     id = models.IntegerField(primary_key=True, blank=True, null=True)
#     jobhdr = models.ForeignKey(Jobhdr, on_delete=models.CASCADE, blank=True, null=True)
#     jobtas = models.ForeignKey(Jobtas, on_delete=models.CASCADE)
#     femast = models.ForeignKey(Femast, on_delete=models.CASCADE, blank=True, null=True)
#     orgtbl = models.ForeignKey(Orgtbl, on_delete=models.CASCADE, blank=True, null=True)
#     dept = models.ForeignKey(Dept, on_delete=models.CASCADE, blank=True, null=True)
#     userrg = models.ForeignKey(Userrg, on_delete=models.CASCADE, blank=True, null=True)



