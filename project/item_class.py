import sqlite3, os

# 23-2-22 16시 수정
# 23_02_22_v01 수정본

path = os.path.dirname(__file__)

class Item:

    def __init__(self):
        conn = sqlite3.connect(path + '/mart.db') 
        cur = conn.cursor()
        # cur.execute('''
        # create table if not exists items(
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

# 데이터 입력 함수
    def insert_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        while True:
            mat_category = int(input('카테고리(그로서리:10, 축산:20, 수산:30, 농산:40) >>> '))
            check = 0
            if mat_category not in (10, 20, 30, 40):
                print('10, 20, 30, 40만 입력해주세요.')
                check = 1 
            if check == 0:
                break 
        while True:
            check = 0
            mat_name = input('물품명 >>> ')
            for item in cur.execute('select * from materiel_management'):
                if item[2] == mat_name: 
                    check = 1
            if check == 0:
                break 
            print('중복되는 물품명이 있습니다.')
        mat_num  = input('수량 >>> ')
        while True:
            mat_price = input('가격 >>> ')
            if mat_price.isdigit() == False:
                print('숫자로 입력해주세요.') 
            elif mat_price == '0': 
                print('0은 입력할 수 없습니다.') 
            elif mat_price.isdigit() == True:
                break        
        mat_discount = input('할인율 >>> ')
        sql = 'insert into items(mat_category, mat_name, mat_num, mat_price, mat_discount) values(?,?,?,?,?)'
        cur.execute(sql,(mat_category,mat_name,mat_num,mat_price,mat_discount)) 
        # 물품번호는 자동 생성, 카테고리명은 다른 곳에서 끌어오는 거라서 제외
        # mat_index = 물품번호
        # mat_category = 카테고리 넘버
        # mat_name = 물품 번호
        # mat_price = 가격
        # mat_discount = 할인 유무
        conn.commit()
        conn.close()        

# 데이터 수정 함수
    def update_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        while True:
            mat_index = int(input('수정할 물품번호 >>> '))
            for item in cur.execute('select * from materiel_management'):
                check = 0
                if item[0] == mat_index:
                    col = input('수정할 칼럼(mat_category,mat_name,mat_num,mat_price,mat_discount,mat_dis)')
                    if col in('mat_category','mat_name','mat_num','mat_price','mat_discount','mat_dis'): 
                        value = input(f'{col}칼럼 수정할 내용 입력 >>> ')
                        sql = f'update materiel_management set {col} = ? where mat_index = ?'
                        cur.execute(sql,(value,mat_index))
                        check = 1
                        cur.execute(f'select * from materiel_management where mat_index = {mat_index}')
                        print(cur.fetchall(), '수정되었습니다.')
                        break
                else:
                    print('해당 물품번호가 없습니다.')
            if check == 1:
                break
        conn.commit()
        conn.close()
                               

# 데이터 삭제 함수
    def delete_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('삭제할 물품번호 >>> '))
        for item in cur.execute('select * from materiel_management'):
            check = 0
            if item[0] == mat_index:
                sql = f'delete from materiel_management where mat_index = {mat_index}'
                cur.execute(sql)
                check = 1
                print('삭제되었습니다.')
                break
        if check == 0:
            print('해당 물품번호가 없습니다.')                   

        conn.commit()
        conn.close()

# 데이터 조회 함수        
    def search_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('조회할 물품번호 >>> '))
        for i in cur.execute('select * from materiel_management'):
            check = 0
            if i[0] == mat_index:
                cur.execute(f'select * from materiel_management where mat_index={mat_index}')
                check = 1
                item = cur.fetchone()
                print(f'''
물품 번호 : {item[0]:>7}
카테 고리 : {item[1]:>7}
물 품 명 : {item[2]:^9}
수   량 : {item[3]:>9}
가   격 : {item[4]:>9} 
할 인 율 : {item[5]:>8}            
                ''')
                break
        if check == 0:
            print('해당 물품번호가 없습니다.')                   

        conn.close()
    
# 입고
    def input_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('입고할 물품번호 >>> '))
        mat_num = int(input('입고할 물품 수량 >>> '))
        for item in cur.execute('select * from materiel_management'):
            if item[0] == mat_index:
                sum = mat_num + item[3]
                cur.execute(f'update materiel_management set mat_num = {sum} where mat_index={mat_index}')
                break
        conn.commit()
        conn.close()

# 출고            
    def output_item(self):
        conn = sqlite3.connect(path + '/mart.db')
        cur = conn.cursor()
        mat_index = int(input('출고할 물품번호 >>> '))
        mat_num = int(input('출고할 물품 수량 >>> '))
        for item in cur.execute('select * from materiel_management'):
            if item[0] == mat_index:
                sum =  item[3] - mat_num
                cur.execute(f'update materiel_management set mat_num = {sum} where mat_index={mat_index}')
                break
        conn.commit()
        conn.close()


a = Item()
# a.insert_item()
# a.update_item()
# a.delete_item()
# a.output_item()
# a.search_item()