import sqlite3, os

# 23-2-23 주석

path = os.path.dirname(__file__)

class Item:

    def __init__(self):
        conn = sqlite3.connect(path + '/mart.db') 
        # cur = conn.cursor()
        # cur.execute('''
        # create table if not exists materiel_management(
        # mat_index INTEGER PRIMARY KEY AUTOINCREMENT,
        # mat_category INTEGER,
        # mat_name text,
        # mat_num INTEGER,
        # mat_price INTEGER,
        # mat_discount INTEGER)
        # ''')
        # mat_index = 물품번호
        # mat_category = 카테고리 넘버
        # mat_name = 물품명
        # mat_price = 가격
        # mat_discount = 할인율
        # conn.commit()
        conn.close()

# insert_item 함수
# 물품 목록을 작성하는 함수
    def insert_item(self):
        conn = sqlite3.connect(path + '/mart.db') # SQLite DB 연결
        cur = conn.cursor() #connection으로부터 cursor 생성
        #입력한 카테고리와 카테고리가 일치할 때까지 반복됨
        while True:
            mat_category = int(input('카테고리(그로서리:10, 축산:20, 수산:30, 농산:40) >>> '))
            check = 0
            if mat_category not in (10, 20, 30, 40):
                print('10, 20, 30, 40만 입력해주세요.')
                check = 1  #카테고리에 10,20,30,40이 아니면 입력 불가
            if check == 0:
                break  #그렇지 않으면 break. 카테고리 입력하라는 메세지가 뜸     
        while True:
            check = 0
            mat_name = input('물품명 >>> ')
            for item in cur.execute('select * from materiel_management'): #item을 m_m의 변수로 설정
                if item[2] == mat_name: 
                    check = 1 #물품명이 일치하면 다음으로 넘어가고 그렇지 않으면 메세지 뜨고 다시 반복
            if check == 0:
                break 
            print('중복되는 물품명이 있습니다.') 
        mat_num  = input('수량 >>> ')
        while True: #가격이 숫자로 입력되지 않을 경우 메세지가 뜨고 다시 처음으로 돌아감
            mat_price = input('가격 >>> ') 
            if mat_price.isdigit() == False:
                print('숫자로 입력해주세요.') #가격에 0은 입력될 수 없음
            elif mat_price == '0': 
                print('0은 입력할 수 없습니다.') 
            elif mat_price.isdigit() == True:
                break          #가격이 숫자면 다음으로 넘어감       
        mat_discount = input('할인율 >>> ')
        sql = 'insert into materiel_management(mat_category, mat_name, mat_num, mat_price, mat_discount) values(?,?,?,?,?)' #sql 명령어를 통해 items라는 테이블에 정보 입력
        cur.execute(sql,(mat_category,mat_name,mat_num,mat_price,mat_discount)) #sql 명령 실행, 실행한 문장은 인자를 가질 수 있음
        # 물품번호는 자동 생성, 카테고리명은 다른 곳에서 끌어오는 거라서 제외
        # mat_index = 물품번호
        # mat_category = 카테고리 넘버
        # mat_name = 물품 번호
        # mat_price = 가격
        # mat_discount = 할인 유무
        conn.commit()
        conn.close()        

# update_item 함수
# 물품 목록 정보를 수정하는 함수
    def update_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        #수정할 물품번호가 일치하지 않으면 맞을 때까지 물품번호 다시 입력해야함 
        while True:
            mat_index = input('수정할 물품번호 >>> ')
            if not mat_index.isdigit():
                continue
            else:
                mat_index=int(mat_index)
            for item in cur.execute('select * from materiel_management'): #materiel_management로 부터 모든 데이터 가져오고 sql 명령 실행
                check = 0
                if item[0] == mat_index:
                    col = input('수정할 칼럼(mat_category,mat_name,mat_num,mat_price,mat_discount,mat_dis)') #물품번호가 일치하면 수정할 칼럼 입력할 수 있음
                    if col in('mat_category','mat_name','mat_num','mat_price','mat_discount','mat_dis'): 
                        value = input(f'{col}칼럼 수정할 내용 입력 >>> ') #칼럼이 일치하면 수정할 내용을 입력할 수 있음
                        sql = f'update materiel_management set {col} = ? where mat_index = ?'
                        cur.execute(sql,(value,mat_index)) #sql 명령 실행
                        check = 1
                        cur.execute(f'select * from materiel_management where mat_index = {mat_index}') #물품번호가 일치할 때 m.m으로 가져와 실행
                        print(cur.fetchall(), '수정되었습니다.') #조회된 결과 모두를 리스트로 반환
                        break
            else:
                print('해당 물품번호가 없습니다.')
            if check == 1:
                break
        conn.commit()
        conn.close()
                               

# delete_item 함수
# 물품 번호로 목록의 정보를 삭제하는 함수
    def delete_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('삭제할 물품번호 >>> '))
        for item in cur.execute('select * from materiel_management'): #materiel_management로 부터 모든 데이터 가져오고 sql 명령 실행
            check = 0
            if item[0] == mat_index:
                sql = f'delete from materiel_management where mat_index = {mat_index}' #물품번호가 일치할 때 삭제 가능
                cur.execute(sql) #sql 명령 실헹
                check = 1
                print('삭제되었습니다.')
                break
        if check == 0:
            print('해당 물품번호가 없습니다.')                   

        conn.commit()
        conn.close()

# search_item 함수
# 물품 번호로 물품 목록의 정보를 조회하는 함수        
    def search_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('조회할 물품번호 >>> '))
        for i in cur.execute('select * from materiel_management'): #materiel_management로 부터 모든 데이터 가져오고 sql 명령 실행
            check = 0
            if i[0] == mat_index: 
                cur.execute(f'select * from materiel_management where mat_index={mat_index}')
                check = 1
                item = cur.fetchone() #조회된 결과로부터 1개 데이터 반환
                print(f'''
물품 번호 : {item[0]:>7}
카테 고리 : {item[1]:>7}
물 품 명  : {item[2]:^9}
수   량   : {item[3]:>9}
가   격   : {item[4]:>9} 
할 인 율  : {item[5]:>8}            
                ''')
                break #물품번호가 일치할 경우 실행
        if check == 0:
            print('해당 물품번호가 없습니다.')                   

        conn.close()
    
# input_item 함수
# 물품 번호로 입고할 물품 수량에 기존 수량을 더하는 함수 
    def input_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('입고할 물품번호 >>> '))
        mat_num = int(input('입고할 물품 수량 >>> '))
        
        for item in cur.execute('select * from materiel_management'): 
            if item[0] == mat_index: 
                sum = mat_num + item[3] #sum은 기존 수량에 입고할 물품을 더 하는 변수
                cur.execute(f"insert into item_log values('{item[0]}','{item[2]}','입고','{mat_num}',datetime('now','+9 hours'))")
                cur.execute(f'update materiel_management set mat_num = {sum} where mat_index={mat_index}')
            
                break #물품번호가 일치하면 중지
        conn.commit()
        conn.close()

# output_item 함수 
# 물품 번호로 기존 수량에 출고할 물품 수량을 빼는 함수             
    def output_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('출고할 물품번호 >>> '))
        mat_num = int(input('출고할 물품 수량 >>> '))

        for item in cur.execute('select * from materiel_management'):
            if item[0] == mat_index:
                sum =  item[3] - mat_num #sum은 기존 수량에 출고할 물품을 빼는 함수
                cur.execute(f"insert into item_log values('{item[0]}','{item[2]}','출고','{mat_num}',datetime('now','+9 hours'))")
                cur.execute(f'update materiel_management set mat_num = {sum} where mat_index={mat_index}')
                break #물품번호가 일치하면 중지
        conn.commit()
        conn.close()

    # 입출고 로그 출력 함수
    def itemlog(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        sql = 'select * from item_log'
        cur.execute(sql) 
        
        for item in cur.fetchall(): 
            print(f'''
물품 번호    : {item[0]}
물 품 명     : {item[1]}
입출고 여부  : {item[2]}
입출고 수량  : {item[3]}
입출고 시간  : {item[4]}           
            ''')
                

        conn.close()

# a = Item()
# a.insert_item()
# a.update_item()
# a.delete_item()
# a.output_item()
# a.search_item()

