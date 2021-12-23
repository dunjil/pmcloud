# from django.db import connection
# import pandas as pd
# import json
# def home(request):
#     cursor = connection.cursor()


#     cursor.execute(""" SELECT * FROM REPORTS.R_JOBHDR WHERE REPORTS.R_JOBHDR.JOB_STATUS = 'C' FETCH FIRST 20 ROWS ONLY """)
    
#     df = pd.DataFrame(cursor.fetchall())
    
#     cols = [row[0] for row in cursor.description] 
#     df.columns = cols
#     # df = df.rename(columns=cols, inplace=True)
#     df_data = df.reset_index().to_json(orient='records') 
#     # df = cursor.fetchall()
#     data = json.loads(df_data)
    
#     # print(df)
#     # print(df.head(1))
#     context = {"row":data}
#     # df2=df.head(1)
#     # print(df2.to_json())
#     return render(request, "index.html", context)






# Outstanding Jobs

# def backlog(request):
#     datez = datetime.datetime.now() + datetime.timedelta(days=50)
#     print(datez)
#     pcm = Jobhdr.objects.filter(
#         Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
#         Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
#         Q(jobtas__ja_orgn_id__orgn_code__in=['FIRE_S']) &
#         ~Q(next_step__in=["RM","JV"]) &
#         Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
#         # Q(femast__vet_flag__in=['Y', 'M']) &
#         ~Q(rqtr__in=['PACER'])
#      ).count()
#     print(pcm)
#     return render(request, 'indexx.html', {'qs': pcm})









# GENERATED JOBS
# def backlog(request):
  #    today = datetime.datetime.today() - 365
#     query = Jobhdr.objects.all()
#     pcm = query.filter(
#         ~Q(job_status__in=["CM", "RM"]) &
#         Q(femast__vet_flag__in=["Y", "M"]) &
#         Q(rqt_date__range=(datetime.datetime.now(), datetime.datetime.now()-))
#     ).count()
#     print(pcm)
#     return render(request, 'index.html', {'qs': pcm})

pcm = 'ELEC_UTIL', 'INST_UTIL', 'MECH_UTIL', 'SYQFG_UTIL'
pcn_b = 'ELEC_SL', 'INST_SL', 'MECH_SL', 'SYQFG_SL'
pcn_c = 'ELEC_LHU', 'INST_LHU', 'MECH_LHU', 'SYQFG_LHU'
ptmd = 'ELEC_T123', 'INST_T123', 'MECH_T123', 'SYQFG_T123'
pmf = 'CIV_INSUL', 'CIV_PAINT'
pms = 'HVAC_IA', 'MSC_LIFT&R', 'MSC_LIGHT', 'MSC_SCAFF', 'WK_ACCESS'
pmn = 'PMN_CIVIL', 'PMN_ELEC', 'PMN_MECH', 'PMN_INST'
pmw = 'ELECSMART'
'ELECTSHOP', 'FABWKSHOP', 'HDWKSHOP','INST_SUPP','INSTWKSHOP', 'MACHINSHOP', 'MC_WKSHOP', 'MECHWKSHOP', 'OVHDCRANE'

















































