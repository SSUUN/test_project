import sqlite3,os
path = os.path.dirname(__file__)

class f:  # 사용자 물건 구매 클래스
    def __init__(self):  # 초기값 DB정보
        self.con = sqlite3.connect(path+"/mart.db")
        self.cur = self.con.cursor()
        self.login_value = False

    def log(self):  # 로그인 과정
        self.cur.execute(
            "select cus_id,cus_pw from customer")       # 사용자 id,pw 정보 가져옴
        d = self.cur.fetchall()

        self.cus_id = input("아이디 입력 : ")           # id입력
        self.cus_pw = input("패스워드 입력 : ")         # pw입력

        if (self.cus_id, self.cus_pw) in d:             # 가져온 사용자 정보와 입력값이 일치하는지 비교
            print("로그인 성공")
            self.login_value = True
            self.user_data = self.cur.execute(
                f"""select cus_num,cus_grade,cus_save  
                                            from customer
                                            where cus_id='{self.cus_id}'
                                            and cus_pw='{self.cus_pw}'"""
            ).fetchone()                                # 로그인동시에 유저 데이터 가져옴

        else:
            print("사용자 정보가 없습니다.")              # 정보가 없으면 출력

    # 출력할때 문자열 길이 맞춰주는 함수
    #
    def ward_len(self, x):
        s = 0
        for i in x:
            if ord(i) > 123:
                s += 1
        if s>=8:
            return int(s / 1.2)
        elif s==7:
            return int(s / 1.4)   
        elif s == 6:
            return int(s / 1.6)   
        elif s == 5:
            return int(s / 1.8)
        elif s == 4:
            return int(s / 2)
        elif s == 3:
            return int(s / 2.1)
        elif s == 2:
            return int(s / 2.2)
        elif s == 1:
            return int(s /3)
        else:
            return 0


        

    def serch(self):  # 특정 조건에 해당하는 품목들 출력하는 함수 (ex 할인품목
        a = input("""
----------------------------------------------
1.카테고리 확인 2.할인품목 확인 3.나가기
----------------------------------------------
    """)

        # 카테고리 별 품목
        if a == "1":
            self.cur.execute(
                "select mat_catename,category_num from category")  # 카테고리 정보 가져옴
            d = self.cur.fetchall()
            for i in d:  # 반복문 으로 카테고리목록 출력
                print(i[0], ":", i[1])
            ca = input("카테고리선택 : ")  # 어던 카테고리 보고싶은지 선택
            self.cur.execute(
                f"""select mat_name ,mat_discount,mat_price,mat_dis,mat_num 
                                from materiel_management
                                 where mat_category = '{ca}'"""
            )  # 선택한 카테고리에 해당하는 품목 가져오기
            print(f'{"품목명":<30}|  {"할인율":<5}|   {"가격":<7} | {"수량":<4}')

            for i in self.cur.fetchall():  # 선택한 카테고리에 해당하는 품목 출력
                aa = 32 - self.ward_len(i[0])  # 프린트 할때 길이 맞춰주는 함수

                print(
                    f'{i[0]:<{aa}}  {str(i[1])+"%":<7}  {(i[2]-(i[2]*(i[1]/100)) if i[3] else i[2]):<7}       {i[4]:<4}'
                )

        # 할인하는 품목 가져오기
        elif a == "2":
            self.cur.execute(
                """select mat_name ,mat_discount,mat_price ,mat_num
                                from materiel_management
                                 where mat_dis = '1'""")  # 할인품목 가져오기
            print(f'{"품목명":<40} | {"할인율":<5}| {"가격":<7} | {"수량":<4}')
            for i in self.cur.fetchall():
                aa = 42 - self.ward_len(i[0])  # 프린트 할때 길이 맞춰주는 함수#할인품목 출력
                print(
                    f'{i[0]:<{aa}}  {str(i[1])+"%":<7}  {i[2]-(i[2]*i[1]/100):<9}   {i[3]:<4}'
                )

        elif a == "3":  # 종료
            return

    # 물품 입력받아서 구매
    def buy(self):
        if not self.login_value:
            print("로그인 하세요 !")
            return
        self.cur.execute(
            """select mat_name ,mat_discount,mat_price,mat_dis,mat_num ,mat_index
                            from materiel_management
                             """)  # 물품 정보 가져오기
        d = self.cur.fetchall()
        d_name = list(map(lambda x: x[0], d))  # 품목 이름만 가져오기
        # 판매반복문
        while True:
            name = input("구매할 물품명 입력 종료(q): ")  # 구매할 물품 선택
            if name == "q":  # 종료 q
                break
            
            # 특정이름 들어간 상품이 여러개일때 데이터 
            name_list=self.cur.execute(
            f"""select mat_name ,mat_discount,mat_price,mat_dis,mat_num ,mat_index
                            from materiel_management
                            where mat_name like '%{name}%' 
                             """).fetchall()       # 물품 정보 가져오기
            
            # 특정이름 들어간 상품이 여러개일때 실행 
            if len(name_list)>1:
                print( )
                for it_n,item_n in enumerate(name_list):   # 상품리스트 출력 
                    print( f"{it_n}. {item_n[0]}")
                print( )
                u_name=input("상품의 번호 또는 상품명을 입력하세요.  종료(q): ")  # 번호또는 이름입력 
                if name == "q":  # 종료 q
                    break
                
                #숫자일때 인덱스로 이름 찾음 
                if u_name.isdecimal():                  
                    if 0<=int(u_name)<len(name_list):
                        name=name_list[int(u_name)][0]
                    else:
                        print("없는 숫자 입니다")
                else:
                    name=u_name #이름은 그냥이름 

            
            if name in d_name:  # 입력한 품목이 db에 있으면 개수 입력으로 넘어감
                while True:
                    count = input("구매개수 입력 종료(q) : ")
                    if count == "q":  # 종료 q
                        break
                    #숫자인지 확이나는 과정
                    if count.isdecimal():
                        count = int(count)
                    
                        
                    #  입력된 제품의 정보를 db에서 가져옴
                        d_discount, d_price, d_dis, d_num, d_index = self.cur.execute(
                                                                    f"""select mat_discount,
                                                                                mat_price,
                                                                                mat_dis,
                                                                                mat_num ,
                                                                                mat_index
                                                                    from materiel_management
                                                                    where mat_name='{name}'
                                                                     """).fetchone(
                            )

                        rc = d_num
                        tt1 = 0
                        # 남은 수량
                        if count > rc:
                            print(f"물품 수량부족 남은 수량 {rc}개")  # 남은거보다 사는게 많으면 판매불가
                        else:  # 사는게 더 적으면 가능
                            if self.user_data[2] > 0:  # 적립금이 있으면
                                
                                tt = input("적립금을 사용하시겠습니까? (y/n)")  # 물어보고
                                if tt == "y":
                                    while True:
                                        tt1 = input(
                                                f"현재 적립금{self.user_data[2]}원 사용금액 입력 취소(q): "
                                            )  # 얼마 남아있는지 알려주고 사용금액 입력
                                        if tt1.isdecimal():
                                            tt1=int(tt1)
                                            break
                                        
                                        else:
                                            print("숫자를 입력하세요")
                                            continue

                                    if tt1 <= self.user_data[
                                            2]:  # 남아있는적립금보다 작게쓰면 가능
                                        pass
                                    else:
                                        tt1 = self.user_data[
                                            2]  # 남아있는적립금보다 많이 입력하면 전체다 사용

                                # 구매 하면 물품 개수 차감,적립금 사용자 전체사용금액, 영수증? 테이블 업데이트
                            self.buy_update(name, d_num, d_price, tt1, d_dis,
                                                d_discount, d_index, count)
                            self.buy_log_last()
                                # print("구매 완료")# 구매성공
                            break
                    else:
                        print("숫자를 입력하세요")
            else:
                print("없는 상품 입니다.")  # 없는 물품 입력시 없다고 한다
                
    def buy_log_last(self):
            i=self.cur.execute("select * from buy order by buy_date").fetchall()[-1]
            ww=self.cur.execute(f"select mat_name from materiel_management where mat_index={i[1]} ").fetchone()[0]
            print(f"영수증 번호 : {i[0]} ")
            print(f"사용자 번호 : {i[2]} ")
            print(f"사용자 등급 : {i[3]} ")
            print(f"물품 명     : {ww} ")
            
            print(f"구매 지점   : {i[4]} ")
            print(f"구매 총액   : {i[6]} ")
            print(f"구매 시간   : {i[-1]} ")
                
    # 구매하면 DB데이블 업데이트 해주는 함수
    def buy_update(self, item_name, item_num, item_price, user_save, dis,
                   discount, index, count):  # 상품 구매시 데이터 베이스 업데이트

        # 일단 지점 아이디 처음값가져옴 (위치를 모르니까 아무값이나 )
        pid = self.cur.execute("select market_id from branch").fetchone()[0]
        if not pid:
            pid = 1
        # 물품 개수와 할인율 적립금 등을 적용하여 전테금액 계산
        
        price1 = (item_price * count - item_price * count * discount / 100
                  if dis else item_price * count) - user_save

        # 구매한 물품 개수많큼 남은 개수 차감
        self.cur.execute(
            f"""update materiel_management set mat_num= mat_num-{count}
                            where mat_name='{item_name}'""")

        # 사용자의 적립금을 사용한만큼 빼준다
        self.cur.execute(f"""update customer set cus_save=cus_save-{user_save}
                                where cus_id='{self.cus_id}'
                                and cus_pw='{self.cus_pw}'""")

        # 사용자의 적립금을 추가해준다
        self.cur.execute(
            f"""update customer set cus_save=cus_save+{int(price1*0.01)}
                                where cus_id='{self.cus_id}'
                                and cus_pw='{self.cus_pw}'""")

        # 사용자가 지금까지 사용한 전체 금액에  지금 사용한 금액을 추가해줌
        self.cur.execute(f"""update customer set cus_total=cus_total+{price1}
                                where cus_id='{self.cus_id}'
                                and cus_pw='{self.cus_pw}'""")
        # 회원등급 게산용 총금액
        grade = self.cur.execute(f"""select cus_total 
                                from customer 
                                where cus_id='{self.cus_id}'
                                and cus_pw='{self.cus_pw}'""").fetchone()[0]
        # 등급표 가져오기 
        gra_list=self.cur.execute("select * from customer_grade order by grade_cost desc").fetchall()
        
        # 등급 업데이트 
        for i,j in gra_list:
            if grade>=j:
                self.cur.execute(f"""update customer set cus_grade='{i}'
                                where cus_id='{self.cus_id}'
                                and cus_pw='{self.cus_pw}'""")
                break
                
        # 구매한 영수증 ? 을 업데이트한다
        self.cur.execute(
            f"""insert into buy ("mat_index","cus_num","cus_grade","market_id",
"mat_num","mat_price","mat_dis","mat_discount","cus_savebool","buy_date")
                            values(
                            '{index}',
                            {self.user_data[0]},
                            '{self.user_data[1]}',
                            {pid},
                            {count},
                            {price1} ,
                            {1 if dis else 0 },
                            {discount*dis},
                            {1 if user_save else 0},
                            datetime('now','+9 hours'))""")
        # 구매완료 결제정보 출력
        print(f"{item_name} {count}개 {price1}원 결제완료({int(price1*0.01)}원 적립)\n")
        self.con.commit()
        # 업데이트 된 사용자 정보 업데이트 
        self.user_data = self.cur.execute(
                f"""select cus_num,cus_grade,cus_save  
                                            from customer
                                            where cus_id='{self.cus_id}'
                                            and cus_pw='{self.cus_pw}'"""
            ).fetchone()  # 로그인동시에 유저 데이터 가져옴

# 관리자가 매출관리과 직원들 관리
class branch:
    # 초기 데이터베이스값

    def __init__(self):
        self.con = sqlite3.connect(path+"/mart.db")
        self.cur = self.con.cursor()
        self.login_value = False  # 보안이 중요하기 때문에 로그인 안하면 사용불가 로그인 변수로 제어

    # 최고관리자 추가하는함수
    def king_update(self):
        if not self.login_value:
            print("로그인 하세요!")
            return
        # 관리자 아이디 입력
        m_id = input("관리자 id : ")
        # 없는 지점에서 일하는건 불가능 하니까 있는지점에서만 가능
        while True:
            m_pl = input("지점 id : ")
            if m_pl.isdecimal():
                m_pl=int(m_pl)
                if (m_pl, ) not in self.cur.execute(
                        "select market_id from branch").fetchall():
                    print("없는 지점id")
                else:
                    break
            else:
                print("숫자를 입력하세요")
        # 이름 직급 번호ㅈ들 아무값이나 상관없음
        m_n = input("이름 : ")
        #m_r = input("직급: ")
        m_p = input("전화번호: ")

        # 관리품목도 존재하는거만 관리함없으면 계속
        while True:
            m_c = input("관리품목 : ")
            ll = self.cur.execute(
                "select category_num from category").fetchall()
            if (m_c, ) not in ll:
                print("없는 관리품목 입니다\n 현재 관리품목은")
                print(ll)
            else:
                break
        # 입력한 데이터들 테이블에 추가
        self.cur.execute(
            f"""insert into Manager values('{m_id}','{m_pl}','{m_n}','king','{m_p}','{m_c}')"""
        )
        self.con.commit()
        print("추가완료")

    def log(self):  # 로그인
        self.cur.execute("select manager_id from Manager")  # 관리자 정보 가져와서
        d = self.cur.fetchall()
        self.cus_id = input("아이디 입력 : ")  # 일치하는지 보고
        if (self.cus_id, ) in d:
            print("로그인 성공")  # 있으면 로그인
            self.login_value = True  # 로그안 변수도 변경해주고
            # 관리자의 직급을 가져온다 (직급별로 권한 달라서)
            self.rank = self.cur.execute(f"""select manager_rank
                    from Manager
                    where manager_id='{self.cus_id}'
                   """).fetchone()[0]

        else:
            print("사용자 정보가 없습니다.")  # 정보 없으면 없다한다

    # 지점별 매출조회
    def price_check_place(self):
        # 로그인 안하면 함수 접근 불가
        if not self.login_value:
            print("로그인 하세요!")
            return

        place_id = input("조회할 지점의 id를 입력하세요 -모든지점조회(all) : ")  # 입력
        plist = self.cur.execute(
            """select market_id from branch""").fetchall()  # 지점 정보 가져옴
        if place_id == "all":
            # 모든 지점의 매출을 집계하여 가져온다
            d = self.cur.execute("""select market_id ,sum(mat_price) 
                                from buy
                                group by market_id""").fetchall()
            # 모두 출력
            if len(d) == 0:
                print("매출없음")
            else:
                for i in d:
                    print(f"{i[0]}지점 매출 {i[1]:>10}원")

        # 입력값과 지점중 일치하는 곳이 있으면 실행
        elif (int(place_id), ) in plist:
            # 매출집계는 같은데 입력한 지점 한곳의 매출만 가져옴
            d = self.cur.execute(f"""select sum(mat_price) 
                                from buy
                                where market_id='{place_id}'
                                group by market_id""").fetchone()
            # 매출이 없으면 0
            if not d:
                d = 0
            else:
                d = d[0]
            print(f"{place_id}지점 매출 {d:>10}원")
        else:
            print("없는 지점 입니다.")  # 없는지점

    # 기간별 매출 조회
    def price_check_time(self):
        ll = {"1": "%Y", "2": "%Y%m", "3": "%Y%m%d"}  # 입력 값과 년도값 매핑
        # 로그인 안하면 접근 불가
        if not self.login_value:
            print("로그인 하세요!")
            return
        # 년 월 일 별로 집계기능
        dat = input("단위 선택 - 1.년 2.월 3.일")
        # 입력값이 딕셔너리 키에 있다면 실행
        if dat in ll.keys():
            # DB에 시간 함수 사용해서 입력값 (년,월,일) 로 집계
            data = self.cur.execute(
                f"""select strftime('{ll[dat]}',buy_date), sum(mat_price) 
                                from buy
                                group by strftime('{ll[dat]}',buy_date)"""
            ).fetchall()
            # 집계값 출력
            for i in data:
                print(i[0], i[1])
        else:
            print("잘못된 입력 1,2,3 중 선택")  # 입력 오류

    # 관리자 추가제거수정 관리

    def manager_update(self):
        # 로그인 안하면 접근불가
        if not self.login_value:
            print("로그인 하세요!")
            return
        # 여기는 더 중요한 기능이라 최고 관리자만 접근가능
        if self.rank == "king":
            man = input("1.관리자 추가 2.관리자 제거 3.관리자 정보수정")
            # 관리자 추가
            if man == "1":
                m_id = input("관리자 id : ")

                # 없는 지점에서 일하는건 불가능 하니까 있는지점에서만 가능
                while True:
                    m_pl = input("지점 id : ")
                    if m_pl.isdecimal():
                        m_pl=int(m_pl)
                        if (m_pl, ) not in self.cur.execute(
                                "select market_id from branch").fetchall():
                            print("없는 지점id")
                        else:
                            break
                    else:
                        print("숫자를 입력하세요")
                # 이름 직급 번호ㅈ들 아무값이나 상관없음
                m_n = input("이름 : ")
                m_r = input("직급: ")
                m_p = input("전화번호: ")

                # 관리품목도 존재하는거만 관리함없으면 계속
                while True:
                    m_c = input("관리품목 : ")
                    ll = self.cur.execute(
                        "select category_num from category").fetchall()
                    if m_c.isdecimal():
                        
                        if (int(m_c), ) not in ll:
                            print("없는 관리품목 입니다\n 현재 관리품목은")
                            print(ll)
                        else:
                            break
                    else:
                        print("숫자를 입력하세요")
                # 입력한 데이터들 테이블에 추가
                self.cur.execute(
                    f"""insert into Manager values('{m_id}','{m_pl}','{m_n}','{m_r}','{m_p}','{m_c}')"""
                )
                self.con.commit()
                print("추가완료")

            # 관리자 제거하는 기능
            elif man == "2":
                drop_man = input("제거할 관리자 아이디 입력 : ")
                # 제거할 사람이 현재 존재한는 사람인지 확인
                if (drop_man, ) in self.cur.execute(
                        "select manager_id from Manager").fetchall():
                    self.cur.execute(
                        f"""delete from Manager where manager_id='{drop_man}'"""
                    )
                    self.con.commit()
                    print("삭제완료")
                else:
                    # 없는사람이면 끝
                    print("없는 정보 입니다.")

            # 관리자 정보 수정하는 곳
            elif man == "3":
                ma_id = input("수정할 관리자 아이디 입력 : ")
                # 관리자 정보가 있는지 확인
                if (ma_id, ) in self.cur.execute(
                        "select manager_id from Manager").fetchall():
                    pi = input("""
----------------------------------------------
1.관리지점 수정 2.직급수정 3.전화번호 수정 4.관리품목 수정
----------------------------------------------
    """)
                    # 관리지점 수정 -일하는곳 바꿈
                    if pi == "1":
                        # 근무지 선택 존재하는곳에서만 근무가능 반복문으로 계속확인
                        while True:
                            m_pl = input("관리지점 입력 종료(q) : ")
                            if m_pl == "q":  # q이면 종료
                                break
                            # 없는곳이면 없다한다
                            if m_pl.isdecimal():
                                
                                if (int(m_pl), ) not in self.cur.execute(
                                        "select market_id from branch").fetchall():
                                    print("없는 지점id")
                                # 있으면 근무지 수정
                                else:
                                    self.cur.execute(
                                        f"""update Manager set market_id='{m_pl}' where manager_id='{ma_id}'"""# cus_id는 로그인함수에서 저장한 self.id를 가져옴
                                    )
                                    self.con.commit()
                                    print("수정완료")
                                    break
                            else:
                                print("숫자를입력하세요")

                    # 직급 바꾸는 과정
                    elif pi == "2":
                        m_pl = input("직급 입력 : ")

                        # 입력받은 직급으로 변경
                        self.cur.execute(
                            f"""update Manager set manager_rank='{m_pl}' where manager_id='{ma_id}'"""
                        )
                        self.con.commit()
                        print("수정완료")
                    # 전화번호 바꾸는기능
                    elif pi == "3":
                        m_pl = input("전화번호 입력 : ")
                        # 아무번호나 써라
                        self.cur.execute(
                            f"""update Manager set manager_phone='{m_pl}' where manager_id='{ma_id}'"""
                        )
                        self.con.commit()
                        print("수정완료")
                    # 관리하는 품목 변경
                    elif pi == "4":
                        # 이거도 존재하는 품목만 관리가능
                        while True:
                            m_pl = input("관리품목 입력 종료 (q): ")
                            if m_pl == "q":
                                break
                            # 찾아서 없으면 없다함
                            if m_pl.isdecimal():
                                m_pl=int(m_pl)
                                if (m_pl, ) not in self.cur.execute(
                                        """select category_num from category"""
                                ).fetchall():
                                    print("없는 카테고리")
                                # 그게아니고 찾아서 있으면 관리하는 품목 변경
                                else:
                                    self.cur.execute(
                                        f"""update Manager set category_num='{m_pl}' where manager_id='{ma_id}'"""
                                    )
                                    self.con.commit()
                                    print("수정완료")
                                    break
                            else:
                                print("숫자를 입력하세요")

                else:
                    # 관리자 정보가 없으면 출력
                    print("없는 정보입니다.")

        else:
            # 최고 관리자가 아니면 접근 불가
            print("권한이 없다.")

    # 지점 추가제거수정 함수
    def branch_update(self):
        # 로그인 안하면 접근불가
        if not self.login_value:
            print("로그인 하세요!")
            return
        # 여기는 더 중요한 기능이라 최고 관리자만 접근가능
        if self.rank == "king":
            man = input("1.지점 추가 2.지점 제거 3.지점 정보수정")
            # 지점 추가
            if man == "1":
                while True:
                    m_pl = input("추가할 지점 입력 종료(q) : ")
                    if m_pl == "q":  # q이면 종료
                        break
                    if m_pl.isdecimal():
                        
                        # 추가할 지점 이랑 이미 있는곳이랑 겹치면 추가 못함
                        if (int(m_pl), ) in self.cur.execute(
                                "select market_id from branch").fetchall():
                            print("이미 있는 지점id")
                        else:
                            break
                    else:
                        print("숫자를 입력하세요")

                # 주소 아무거나 상관없음
                m_p = input("지점주소: ")

                # 지점 관리자는 존재하는 사람만 없으면 못함
                while True:
                    m_c = input("지점관리자 : ")
                    ll = self.cur.execute(
                        "select manager_id from manager").fetchall()
                    if (m_c, ) not in ll:
                        print("없는 관리자입니다")
                        print(f"관리자 목록 \n{ll}")
                    else:
                        break
                # 입력한 데이터들 테이블에 추가
                self.cur.execute(
                    f"""insert into branch values("{m_pl}",'{m_c}','{m_p}')""")
                self.con.commit()
                print("추가완료")

            # 지점 제거하는 기능
            elif man == "2":
                drop_man = input("제거할 지점 입력 : ")
                # 입력값이 존재하는 지점인지 확인
                if drop_man.isdecimal():
                    
                    if (int(drop_man), ) in self.cur.execute(
                            "select market_id from branch").fetchall():
                        self.cur.execute(
                            f"""delete from branch where market_id='{drop_man}'""")
                        self.con.commit()
                        print("삭제완료")
                    else:
                        # 없는지점이면 끝
                        print("없는 정보 입니다.")
                else:
                    print("숫자를 입력하세요")
                    
            # 지점 정보수정
            elif man == "3":
                ma_id = input("수정할 지점 아이디 입력 : ")
                # 지점 정보가 있ㄴㄴ지 확인
                if ma_id.isdecimal():
                    ma_id=int(ma_id)
                    if (int(ma_id), ) in self.cur.execute(
                            "select market_id from branch").fetchall():
                        pi = input("""
    ----------------------------------------------
    1.지점관리자 수정 2.지점주소 수정 
    ----------------------------------------------
        """)
                        # 지점관리자 수정
                        if pi == "1":
                            # 관리자가 존재하지않으면 못바꿈
                            while True:
                                m_pl = input("관리자 입력 종료(q) : ")
                                if m_pl == "q":  # q이면 종료
                                    break
                                # 없으면 없는관리자 출력
                                if (m_pl, ) not in self.cur.execute(
                                        "select manager_id from manager").fetchall(
                                        ):
                                    print("없는 관리자 id")
                                # 있으면 관리자 수정
                                else:
                                    self.cur.execute(
                                        f"""update branch set manager_id='{m_pl}' where market_id='{ma_id}'"""
                                    )
                                    self.con.commit()
                                    print("수정완료")
                                    break

                        # 주소바꾸기  주소는 확인할 필요없음
                        elif pi == "2":
                            m_pl = input("주소 입력 : ")

                            # 입력받은 주소으로 변경
                            self.cur.execute(
                                f"""update branch set market_address='{m_pl}' where market_id='{ma_id}'"""
                            )
                            self.con.commit()
                            print("수정완료")
                    else:
                        # 지점 정보가 없으면 출력
                        print("없는 정보입니다.")
                else:
                    print("숫자를 입력하세요")
        else:
            # 최고 관리자가 아니면 접근 불가
            print("권한이 없다.")
            
#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end#end
            
            
