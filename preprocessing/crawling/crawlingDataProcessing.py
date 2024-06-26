import pandas as pd
import numpy as np
college = pd.read_csv('./crawling/대학교.csv',encoding='cp949') #크롤링한 파일 불러오기

college = college[college['매장명'].str.endswith('')] #중복되는 행 제거

college.to_csv('./crawling1/고등학교.csv',index=False) #csv파일 저장