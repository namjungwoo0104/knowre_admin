import streamlit as st
import pandas as pd
from datetime import datetime
from pytz import timezone
from gspread_dataframe import get_as_dataframe, set_with_dataframe
pd.set_option('mode.chained_assignment', None)
from streamlit_gsheets import GSheetsConnection

#google sheet 데이터 불러오기 (몸짱 미국아저씨 코드)
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(worksheet="체험계정발급내역")
trial_raw = pd.DataFrame(data)
#st.dataframe(trial_raw, use_container_width=True)

#전처리 : 필요없는 column 삭제하기
trial=trial_raw.drop(['체험순서','성함','전화','이메일','체험계정 ID','체험계정 만료일','비고'], axis=1)
trial_NaN_deleted = trial.dropna(subset=['구분'], how='any', axis=0)
trial_date = trial_NaN_deleted
trial_date['체험계정발급일_datetime'] = pd.to_datetime(trial_date['체험계정 발급일'])
trial_date['체험연도']=trial_date['체험계정발급일_datetime'].dt.year
trial_date['체험월']=trial_date['체험계정발급일_datetime'].dt.month

#전처리 : 체험월 00월 형태의 str로 전환
trial_date1 = trial_date.loc[trial_date['체험월'] < 10]
trial_date1 = trial_date1.astype({'체험월':'str'})
trial_date1['체험신청월']="0"+trial_date1['체험월']+"월"
trial_date2 = trial_date.loc[trial_date['체험월'] > 9]
trial_date2 = trial_date2.astype({'체험월':'str'})
trial_date2['체험신청월']=trial_date2['체험월']+"월"

#테이블 병합
trial_date3 = pd.concat([trial_date1,trial_date2], ignore_index=True)
trial=trial_date3.drop(['체험월'], axis=1)
trial_db = trial
st.dataframe(trial_db, use_container_width=True)