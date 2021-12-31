from django.shortcuts import render,redirect
from backlog.models import Jobhdr, Orgtbl, Jobtas
import datetime
from django.db.models import Q, OuterRef, Subquery
import datetime
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
import pandas as pd
import json



pcm_closed=pd.DataFrame()

pcn_b_closed=pd.DataFrame()

pcn_c_closed=pd.DataFrame()
ptm_d_closed=pd.DataFrame()
ptm_e_closed=pd.DataFrame()
pmf_closed=pd.DataFrame()
pmi_closed=pd.DataFrame()
pms_closed=pd.DataFrame()
pmn_closed=pd.DataFrame()
pmw_closed=pd.DataFrame()

# Outstanding
outstanding=pd.DataFrame()
pcm_outstanding=pd.DataFrame()
pcn_b_outstanding=pd.DataFrame()
pcn_c_outstanding=pd.DataFrame()
ptm_d_outstanding=pd.DataFrame()
ptm_e_outstanding=pd.DataFrame()
pmf_outstanding=pd.DataFrame()
pmi_outstanding=pd.DataFrame()
pms_outstanding=pd.DataFrame()
pmn_outstanding=pd.DataFrame()
pmw_outstanding=pd.DataFrame()


#from Josh
# elect_util=	1406.8
# inst_util=	1124.0
# mech_util=	1662.5
# syqfg_util=	139.7
# elect_sl	=644.8
# inst_sl=	963.7
# mech_sl	=2170.8
# syqfg_sl	=235.5
# elect_lhu	=1096.1
# inst_lhu	=1376.8
# mech_lhu	=1384.9
# syqfg_lhu	=232.0
# elect_t123	=1182.2
# inst_t123	=2051.6
# mech_t123	=2396.2
# syqfg_t123=	319.0
# elect_t456	=3183.5
# inst_t456	=1650.0
# mech_t456	=3819.6
# syqfg_t456=	409.5
# civ_insul=	0
# civ_paint	=0
# civ_infstr=	324.4
# hvac_ia	=0
# msc_lift_r=	7520.1
# msc_light	=7903.1
# msc_scaff	=2466.6
# wk_access	=1283.0

# Data from 2021
elect_util=	41.7
inst_util	=44.2
mech_util=	47.1
syqfg_util=	9.5
elect_sl=	23.1
inst_sl=	41.2
mech_sl=	50.9
syqfg_sl=	10.2
elect_lhu=	30.9
inst_lhu=	75.6
mech_lhu=	42.9
syqfg_lhu	=5.9
elect_t123	=32
inst_t123	=92.1
mech_t123	=62
syqfg_t123	=14.9
elect_t456	=63.4
inst_t456	=63.4
mech_t456	=162.5
syqfg_t456	=13.6
civ_insul	=333.4
civ_paint	=458.6
civ_infstr	=151.9
hvac_ia	=76
msc_lift_r	=46.3
msc_light	=177.7
msc_scaff	=48.6
wk_access	=17.6
pmn_mech=	14.3
pmn_inst	=0
pmn_elect=	0
fab_wkshop=	623
elect_shop=	72.9
hd_wkshop=	165.8
inst_wkshop=	31.7
elect_smart=	27.9
mech_wkshop=	31
mc_wkshop=	72.9
machin_shop=	26.6
ovhd_crane=	31.5
inst_supp=	2.3



raw_data= {'jobtas__ja_orgn_id__orgn_code':['ELEC_UTIL','INST_UTIL','MECH_UTIL','SYQFG_UTIL','ELEC_SL','INST_SL','MECH_SL','SYQFG_SL','ELEC_LHU','INST_LHU','MECH_LHU','SYQFG_LHU','ELEC_T123','INST_T123','MECH_T123','SYQFG_T123',
'ELEC_T456','INST_T456','MECH_T456','SYQFG_T456','CIV_INSUL','CIV_PAINT','CIV_INFSTR','HVAC_IA','MSC_LIFT&R','MSC_LIGHT','MSC_SCAFF','WK_ACCESS','PMN_MECH','PMN_INST','PMN_ELEC',
      'FABWKSHOP','ELECTSHOP','HDWKSHOP','INSTWKSHOP','ELECSMART','MECHWKSHOP','MC_WKSHOP','MACHINSHOP','OVHDCRANE','INST_SUPP'
],'actual_manhrs':[elect_util,inst_util,mech_util,syqfg_util,elect_sl,inst_sl,mech_sl,syqfg_sl,elect_lhu,inst_lhu,mech_lhu,syqfg_lhu,elect_t123,inst_t123,mech_t123,syqfg_t123,
elect_t456,inst_t456,mech_t456,syqfg_t456,civ_insul,civ_paint,civ_infstr,hvac_ia,msc_lift_r,msc_light,msc_scaff,wk_access,pmn_mech,pmn_inst,pmn_elect,fab_wkshop,elect_shop,hd_wkshop
       ,inst_wkshop,elect_smart,mech_wkshop,mc_wkshop,machin_shop,ovhd_crane,inst_supp]}
org_data=pd.DataFrame(raw_data)
# pcm_est=499
# pcn_b_est=468
# pcn_c_est=573
# ptm_d_est=549.5
# ptm_e_est=844
# pmf_est=2500
# pmi_est=1031
# pms_est=800
# pmn_est=110
# pmw_est=1170


#2020 Data
# pcm_est=189.5
# pcn_b_est=93.4
# pcn_c_est=141.2
# ptm_d_est=186.7
# ptm_e_est=174.5
# pmf_est=1767.4
# pmi_est=324.4
# pms_est=419.6
# pmn_est=8.2
# pmw_est=948.3

#2021 Data
pcm_est=143.8
pcn_b_est=121.8
pcn_c_est=160
ptm_d_est=200.7
ptm_e_est=292.4
pmf_est=781.8
pmi_est=151.9
pms_est=303.5
pmn_est=14.3
pmw_est=849.8
pw_est=2506.85

def backlog(request):
        # Outstanding
    global outstanding
    global pcm_outstanding
    global pcn_b_outstanding
    global pcn_c_outstanding
    global ptm_d_outstanding
    global ptm_e_outstanding
    global pmf_outstanding
    global pmi_outstanding
    global pms_outstanding
    global pmn_outstanding
    global pmw_outstanding


    outstanding = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
    Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
    Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
    Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_UTIL','INST_UTIL','MECH_UTIL','SYQFG_UTIL','ELEC_SL','INST_SL','MECH_SL','SYQFG_SL','ELEC_LHU','INST_LHU','MECH_LHU','SYQFG_LHU','ELEC_T123','INST_T123','MECH_T123','SYQFG_T123',
    'ELEC_T456','INST_T456','MECH_T456','SYQFG_T456','CIV_INSUL','CIV_PAINT','CIV_INFSTR','HVAC_IA','MSC_LIFT&R','MSC_LIGHT','MSC_SCAFF','WK_ACCESS','PMN_MECH','PMN_INST','PMN_ELEC',
      'FABWKSHOP','ELECTSHOP','HDWKSHOP','INSTWKSHOP','ELECSMART','MECHWKSHOP','MC_WKSHOP','MACHINSHOP','OVHDCRANE','INST_SUPP']) &
    ~Q(next_step__in=["RM","JV"]) &
    Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
    ~Q(rqtr__in=['PACER']) &
    ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values()))
    data = outstanding

     # Outstanding
    pcm_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_UTIL', 'INST_UTIL', 'MECH_UTIL', 'SYQFG_UTIL'])]

    pcn_b_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_SL', 'INST_SL', 'MECH_SL', 'SYQFG_SL'])]

    pcn_c_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_LHU', 'INST_LHU', 'MECH_LHU', 'SYQFG_LHU'])]

    ptm_d_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_T123', 'INST_T123', 'MECH_T123', 'SYQFG_T123'])]

    ptm_e_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_T456', 'INST_T456', 'MECH_T456', 'SYQFG_T456'])]

    pmf_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['CIV_INSUL', 'CIV_PAINT'])]

    pmi_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['CIV_INFSTR'])]

    pms_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['HVAC_IA', 'MSC_LIFT&R', 'MSC_LIGHT', 'MSC_SCAFF', 'WK_ACCESS'])]

    pmn_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['PMN_CIVIL', 'PMN_ELEC', 'PMN_MECH', 'PMN_INST'])]

    pmw_outstanding=outstanding.loc[outstanding['jobtas__ja_orgn_id__orgn_code'].isin(['ELECSMART'
    'ELECTSHOP', 'FABWKSHOP', 'HDWKSHOP','INST_SUPP','INSTWKSHOP', 'MACHINSHOP', 'MC_WKSHOP', 'MECHWKSHOP', 'OVHDCRANE'])]
    
    
    
    # PCM
    #data['jobtas__est_misc_amt']=pd.to_numeric(data['jobtas__est_misc_amt'])
    data = pcm_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median(),inplace=True)
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line
    # Q1=data['total_labour'].quantile(0.25)
    # Q3=data['total_labour'].quantile(0.75)
    # IQR=Q3-Q1
    # upper_whisker=(Q3 + 1.5 * IQR)
    # data.loc[data['total_labour']>upper_whisker,'total_labour']=upper_whisker
    pcm_blog=round(data['total_labour'].astype('float64').sum()/pcm_est,1)
    pcm_count = len(data)
    pcm=data['total_labour'].sum()

  
    
    

    # PCN-B
    data = pcn_b_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pcn_b_blog=round(data['total_labour'].astype('float64').sum()/pcn_b_est,1)
    pcn_b_count = len(data)
    pcn_b=data['total_labour'].sum()

   


    # PCN-C


    data = pcn_c_outstanding
    #data['jobtas__est_misc_amt']=pd.to_numeric(data['jobtas__est_misc_amt'])
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pcn_c_blog=round(data['total_labour'].astype('float64').sum()/pcn_c_est,1)
    pcn_c_count = len(data)
    pcn_c=data['total_labour'].sum()
    
    

    # PTM-D
    data = ptm_d_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    ptm_d_blog=round(data['total_labour'].astype('float64').sum()/ptm_d_est,1)
    ptm_d_count = len(data)
    ptm_d=data['total_labour'].sum()


    # PTM-E
    data = ptm_e_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    ptm_e_blog=round(data['total_labour'].astype('float64').sum()/ptm_e_est,1)
    ptm_e_count = len(data)
    ptm_e=data['total_labour'].sum()


    # PMF
    data = pmf_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')

   
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pmf_blog=round(data['total_labour'].astype('float64').sum()/pmf_est,1)
    pmf_count = len(data)
    pmf=data['total_labour'].sum()
      
    
    # PMI
    data = pmi_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pmi_blog=round(data['total_labour'].astype('float64').sum()/pmi_est,1)
    pmi_count = len(data)
    pmi=data['total_labour'].sum()
      
    # PMS
    data = pmi_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pms_blog=round(data['total_labour'].astype('float64').sum()/pms_est,1)
    pms_count = len(data)
    pms=data['total_labour'].sum()
      

    # PMN
    data =pmn_outstanding
    data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pmn_blog=round(data['total_labour'].astype('float64').sum()/pmn_est,1)
    pmn_count = len(data)
    pmn=data['total_labour'].sum()
      
    # PMW
    data = pmw_outstanding
    data['total_labour']=data['jobtas__est_misc_amt'].astype('float64')+ data['jobtas__est_lab_amt'].astype('float64')
    ##This is where I should remove the outliers before calculating the backlog in the next line

    pmw_blog=round(data['total_labour'].astype('float64').sum()/pmw_est,1)
    pmw_count = len(data)
    pmw=data['total_labour'].sum()
      
   


    plant_wide = pcm  + pcn_b + pcn_c + ptm_d + ptm_e + pmf + pmi + pms + pmn + pmw
    pw_count = len(outstanding)
    #pw_blog = round(plant_wide / 11873.98, 1)
    pw_blog = round(float(plant_wide) / pw_est, 1)





    context = {
        'pcm' : pcm_blog,
        'pcm_c' : pcm_count,
        'pcn_b' : pcn_b_blog,
        'pcn_b_c' : pcn_b_count,
        'pcn_c' : pcn_c_blog,
        'pcn_c_c' : pcn_c_count,
        'ptm_d' : ptm_d_blog,
        'ptm_d_c' : ptm_d_count,
        'ptm_e' : ptm_e_blog,
        'ptm_e_c' : ptm_e_count,
        'pmf' : pmf_blog,
        'pmf_c' : pmf_count,
        'pmi' : pmi_blog,
        'pmi_c' : pmi_count,
        'pms' : pms_blog,
        'pms_c' : pms_count,
        'pmn' : pmn_blog,
        'pmn_c' : pmn_count,
        'pmw' : pmw_blog,
        'pmw_c' : pmw_count,
        'pw' : pw_blog,
        'pw_count' : pw_count
    }

    return render(request, 'index.html', context)
def cm_units(request, dept):
    unit=dept
    if unit =='pcm':
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_UTIL', 'INST_UTIL', 'MECH_UTIL', 'SYQFG_UTIL']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
    
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit=='ptm_e':
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_T456', 'INST_T456', 'MECH_T456', 'SYQFG_T456']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])
        ).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
       
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit =='ptm_d':
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_T123', 'INST_T123', 'MECH_T123', 'SYQFG_T123']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
      
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit =='pcn_b':
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_SL', 'INST_SL', 'MECH_SL', 'SYQFG_SL']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
        
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit=='pcn_c':
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_LHU', 'INST_LHU', 'MECH_LHU', 'SYQFG_LHU']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
       
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
        
    elif unit =='pmf':
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['CIV_INSUL', 'CIV_PAINT']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])
        ).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
        
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit == 'pmi':
        data= pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['CIV_INFSTR']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])
        ).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
        
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit =='pms':
        data= pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['HVAC_IA', 'MSC_LIFT&R', 'MSC_LIGHT', 'MSC_SCAFF', 'WK_ACCESS']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) & 
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])
        ).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
        #data['jobtas__est_misc_amt']=pd.to_numeric(data['jobtas__est_misc_amt'])
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit =='pmn':
    
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['PMN_CIVIL', 'PMN_ELEC', 'PMN_MECH', 'PMN_INST']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])
        ).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
       

        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    elif unit =='pmw':
        
        data = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        Q(job_status__in=['A', 'AE', 'C', 'IP', 'JE', 'JR', 'JV', 'JW', 'C']) &
        Q(jobtas__task_status__in=['A', 'ER', 'IP', 'JW', 'NE']) & 
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELECTSHOP', 'FABWKSHOP', 'HDWKSHOP','INST_SUPP','INSTWKSHOP', 'MACHINSHOP', 'MC_WKSHOP', 'MECHWKSHOP', 'OVHDCRANE']) &
        ~Q(next_step__in=["RM","JV"]) &
        Q(target_end_date__gte=(datetime.datetime(2010, 1, 1, 0, 0, 1))) &
        ~Q(rqtr__in=['PACER']) &
        ~Q(work_type__in=['OS', 'SD', 'SF', 'MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code','jobtas__est_lab_amt','jobtas__est_misc_amt')))
       
        data['jobtas__est_misc_amt'].fillna(data['jobtas__est_misc_amt'].median())
        dept_backlog=round(data['jobtas__est_misc_amt'].astype('float64').sum() + data['jobtas__est_lab_amt'].astype('float64').sum()/pcm_est,1)
        dept_outstanding = len(data)
        data['total_labour']=data['jobtas__est_lab_amt']+data['jobtas__est_misc_amt']
        data2=pd.DataFrame( data.groupby( [ "jobtas__ja_orgn_id__orgn_code"] )['total_labour'].agg(['sum','size'])).reset_index()
       
        print(data2)
        data3=pd.merge(data2,org_data,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['sum'].astype('float64')/(data3['actual_manhrs'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':dept_backlog,'outstanding':dept_outstanding,'unit':unit}
        return render(request, 'unit.html', context)
    else:
        return HttpResponse('<h1> Please Select a valid department </h1>')
    #print(ptm_e_data.query)
    


    # Calculates Backlog In Weeks
def weeksbacklog(request):
    today = datetime.datetime.today() - datetime.timedelta(days=365)

    closed = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
    Q(job_status__in=['C', 'HF','EC']) &
    Q(jobtas__task_status__in=['C']) & 
    Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_UTIL','INST_UTIL','MECH_UTIL','SYQFG_UTIL','ELEC_SL','INST_SL','MECH_SL','SYQFG_SL','ELEC_LHU','INST_LHU','MECH_LHU','SYQFG_LHU','ELEC_T123','INST_T123','MECH_T123','SYQFG_T123',
    'ELEC_T456','INST_T456','MECH_T456','SYQFG_T456','CIV_INSUL','CIV_PAINT','CIV_INFSTR','HVAC_IA','MSC_LIFT&R','MSC_LIGHT','MSC_SCAFF','WK_ACCESS','PMN_MECH','PMN_INST','PMN_ELEC',
    'FABWKSHOP','ELECTSHOP','HDWKSHOP','INSTWKSHOP','ELECSMART','MECHWKSHOP','MC_WKSHOP','MACHINSHOP','OVHDCRANE','INST_SUPP'
    ]) &
    Q(next_step__in=["JO"]) &
    Q(jobtas__actual_end_date__gte=(today)) &
    ~Q(work_type__in=['OS', 'SD','MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values('jobtas__ja_orgn_id__orgn_code')))
    
    global pcm_closed
    global outstanding

    global pcn_b_closed

    global pcn_c_closed
    global ptm_d_closed
    global ptm_e_closed
    global pmf_closed
    global pmi_closed
    global pms_closed
    global pmn_closed
    global pmw_closed

    

    
    pcm_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_UTIL', 'INST_UTIL', 'MECH_UTIL', 'SYQFG_UTIL'])]

    pcn_b_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_SL', 'INST_SL', 'MECH_SL', 'SYQFG_SL'])]

    pcn_c_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_LHU', 'INST_LHU', 'MECH_LHU', 'SYQFG_LHU'])]

    ptm_d_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_T123', 'INST_T123', 'MECH_T123', 'SYQFG_T123'])]

    ptm_e_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['ELEC_T456', 'INST_T456', 'MECH_T456', 'SYQFG_T456'])]

    pmf_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['CIV_INSUL', 'CIV_PAINT'])]

    pmi_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['CIV_INFSTR'])]

    pms_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['HVAC_IA', 'MSC_LIFT&R', 'MSC_LIGHT', 'MSC_SCAFF', 'WK_ACCESS'])]

    pmn_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['PMN_CIVIL', 'PMN_ELEC', 'PMN_MECH', 'PMN_INST'])]

    pmw_closed=closed.loc[closed['jobtas__ja_orgn_id__orgn_code'].isin(['ELECSMART'
    'ELECTSHOP', 'FABWKSHOP', 'HDWKSHOP','INST_SUPP','INSTWKSHOP', 'MACHINSHOP', 'MC_WKSHOP', 'MECHWKSHOP', 'OVHDCRANE'])]

   

   


    context = {
        'pcm' : round(len(pcm_outstanding)/(len(pcm_closed)/52),1),
        'pcm_c' :len(pcm_outstanding),
        'pcn_b' : round(len(pcn_b_outstanding)/(len(pcn_b_closed)/52),1),
        'pcn_b_c' : len(pcn_b_outstanding),
        'pcn_c' : round(len(pcn_c_outstanding)/(len(pcn_c_closed)/52),1),
        'pcn_c_c' : len(pcn_c_outstanding),
        'ptm_d' : round(len(ptm_d_outstanding)/(len(ptm_d_closed)/52),1),
        'ptm_d_c' : len(ptm_d_outstanding),
        'ptm_e' : round(len(ptm_e_outstanding)/(len(ptm_e_closed)/52),1),
        'ptm_e_c' : len(ptm_e_outstanding),
        'pmf' : round(len(pmf_outstanding)/(len(pmf_closed)/52),1),
        'pmf_c' : len(pmf_outstanding),
        'pmi' : round(len(pmi_outstanding)/(len(pmi_closed)/52),1),
        'pmi_c' : len(pmi_outstanding),
        'pms' : round(len(pms_outstanding)/(len(pms_closed)/52),1),
        'pms_c' : len(pms_outstanding),
        'pmn' : round(len(pmn_outstanding)/(len(pmn_closed)/52),1),
        'pmn_c' : len(pmn_outstanding),
        'pmw' : round(len(pmw_outstanding)/(len(pmw_closed)/52),1),
        'pmw_c' : len(pmw_outstanding),
        'pw' : round(len(outstanding)/(len(closed)/52),1),
        'pw_count' : len(outstanding)
    }


    print("No of completed jobs for the past one year :{}".format(len(closed.index)))
    return render(request, 'weeks.html',context=context)

# Computes the backlog in weeks for each Unit
def weeks_units(request, dept):
    if len(pcn_b_outstanding)==0:
        return redirect('backlog')
    unit=dept
    if unit =='pcm':
        closed = pd.DataFrame({'closed_count' : pcm_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pcm_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pcm_outstanding)/(len(pcm_closed)/52),1),'outstanding':len(pcm_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit=='ptm_e':
        closed = pd.DataFrame({'closed_count' : ptm_e_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : ptm_e_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(ptm_e_outstanding)/(len(ptm_e_closed)/52),1),'outstanding':len(ptm_e_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit =='ptm_d':
        closed = pd.DataFrame({'closed_count' : ptm_d_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : ptm_d_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = [] 
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(ptm_d_outstanding)/(len(ptm_d_closed)/52),1),'outstanding':len(ptm_d_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit =='pcn_b':
        closed = pd.DataFrame({'closed_count' : pcn_b_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pcn_b_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pcn_b_outstanding)/(len(pcn_b_closed)/52),1),'outstanding':len(pcn_b_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit=='pcn_c':
        closed = pd.DataFrame({'closed_count' : pcn_c_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pcn_c_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pcn_c_outstanding)/(len(pcn_c_closed)/52),1),'outstanding':len(pcn_c_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
        
    elif unit =='pmf':
        closed = pd.DataFrame({'closed_count' : pmf_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pmf_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pmf_outstanding)/(len(pmf_closed)/52),1),'outstanding':len(pmf_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit == 'pmi':
        closed = pd.DataFrame({'closed_count' : pmi_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pmi_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pmi_outstanding)/(len(pmi_closed)/52),1),'outstanding':len(pmi_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit =='pms':
        closed = pd.DataFrame({'closed_count' : pms_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pms_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pms_outstanding)/(len(pms_closed)/52),1),'outstanding':len(pms_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit =='pmn':
        closed = pd.DataFrame({'closed_count' : pmn_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pmn_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pmn_outstanding)/(len(pmn_closed)/52),1),'outstanding':len(pmn_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    elif unit =='pmw':
        closed = pd.DataFrame({'closed_count' : pmw_closed.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        outstanding = pd.DataFrame({'outstanding_count' : pmw_outstanding.groupby( [ "jobtas__ja_orgn_id__orgn_code"] ).size()}).reset_index()
        data3=pd.merge(closed,outstanding,on='jobtas__ja_orgn_id__orgn_code')
        data3['backlog']=round(data3['outstanding_count'].astype('float64')/(data3['closed_count'].astype('float64')/52))
        print(data3.head())
        json_records = data3.to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        context = {'data': data,'backlog':round(len(pmw_outstanding)/(len(pmw_closed)/52),1),'outstanding':len(pmw_outstanding),'unit':unit}
        return render(request, 'weeks_unit.html', context)
    else:
        return HttpResponse('<h1> Please Select a valid department </h1>')
    #print(ptm_e_data.query)

def live_report(request):
    today = datetime.datetime.today() - datetime.timedelta(days=30)
    generated_live=pd.DataFrame.from_records(list(Jobhdr.objects.filter(
        ~Q(job_status__in=["CM", "RM",""]) &
        Q(femast__vet_flag__in=["Y", "M"]) &
        Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_UTIL','INST_UTIL','MECH_UTIL','SYQFG_UTIL','ELEC_SL','INST_SL','MECH_SL','SYQFG_SL','ELEC_LHU','INST_LHU','MECH_LHU','SYQFG_LHU','ELEC_T123','INST_T123','MECH_T123','SYQFG_T123',
        'ELEC_T456','INST_T456','MECH_T456','SYQFG_T456','CIV_INSUL','CIV_PAINT','CIV_INFSTR','HVAC_IA','MSC_LIFT&R','MSC_LIGHT','MSC_SCAFF','WK_ACCESS','PMN_MECH','PMN_INST','PMN_ELEC',
        'FABWKSHOP','ELECTSHOP','HDWKSHOP','INSTWKSHOP','ELECSMART','MECHWKSHOP','MC_WKSHOP','MACHINSHOP','OVHDCRANE','INST_SUPP'
        ]) &
        Q(rqt_date__range__gte=(today)
    )).values()))

    closed_live = pd.DataFrame.from_records(list(Jobhdr.objects.filter(
    Q(job_status__in=['C', 'HF','EC']) &
    Q(jobtas__task_status__in=['C']) & 
    Q(jobtas__ja_orgn_id__orgn_code__in=['ELEC_UTIL','INST_UTIL','MECH_UTIL','SYQFG_UTIL','ELEC_SL','INST_SL','MECH_SL','SYQFG_SL','ELEC_LHU','INST_LHU','MECH_LHU','SYQFG_LHU','ELEC_T123','INST_T123','MECH_T123','SYQFG_T123',
    'ELEC_T456','INST_T456','MECH_T456','SYQFG_T456','CIV_INSUL','CIV_PAINT','CIV_INFSTR','HVAC_IA','MSC_LIFT&R','MSC_LIGHT','MSC_SCAFF','WK_ACCESS','PMN_MECH','PMN_INST','PMN_ELEC',
    'FABWKSHOP','ELECTSHOP','HDWKSHOP','INSTWKSHOP','ELECSMART','MECHWKSHOP','MC_WKSHOP','MACHINSHOP','OVHDCRANE','INST_SUPP'
    ]) &
    Q(next_step__in=["JO"]) &
    Q(jobtas__actual_end_date__gte=(today)) &
    ~Q(work_type__in=['OS', 'SD','MM'])).select_related('jobtas__ja_orgn_id__orgn_code').values()))
    return render(request, 'index.html', {'qs': })