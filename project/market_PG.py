# 물품 관리 프로그램(김수빈조원)
from item_class import Item
# 고객 관리 프로그램(김아영조원)
from customer_class import Customer
# 지점,관리자 관리, 물품 구매 프로그램(선상준조원)
from buy_2 import f
from buy_2 import branch

# 23_02_22_v01 수정본

# 메인메뉴 while문으로 종료전까지 활성화
while True:
    # 클래스 생성
    # 물류관리 클래스
    item = Item()
    # 회원 관리 클래스
    customer = Customer()
    # 회원 물품 구매 클래스
    buy_f = f()
    # 지점, 관리자 관련 클래스 
    buy_branch = branch()

    # 메인 메뉴
    display = '''
    ┌─────────────────────────────────┐
    │ 마켓물류관리 프로그램 v1.01     │
    │ ※ 메뉴                          │
    │ 1. 고객 관리                    │
    │ 2. 물품 관리                    │
    │ 3. 지점 관리                    │
    │ 4. 고객 물품 구매               │
    │ 5. 종료                         │
    └─────────────────────────────────┘
    >>> '''
    menu = input(display)

    # 1번 고객 관리 메뉴
    if menu == '1':
        # 1번 고객 관리 메뉴 while문 활성화
        while True:
            menu1_display = '''
    ┌─────────────────────────────────┐
    │ 마켓 물류관리 프로그램 v1.01    │
    │ ● 고객 관리 메뉴                │
    │ 1. 회원가입                     │
    │ 2. 로그인 및 회원메뉴           │
    │ 3. 회원조회                     │
    │ 4. 상위 메뉴 돌아가기           │
    └─────────────────────────────────┘
            '''
            cos_memu = input(menu1_display)
            
            # 고객 회원가입 메뉴
            if cos_memu == '1':
                customer.signup_customer()

            # 로그인 및 회원메뉴
            elif cos_memu == '2':
                customer.login_customer()
                
                # 로그인 해야지만 가능 로그인 후 하위 메뉴 활성화
                while True:
                    customer_display = '''
    ┌─────────────────────────────────┐
    │ 마켓 물류관리 프로그램 v1.01    │
    │ ■ 회원전용 메뉴                 │
    │ 1. 조회                         │
    │ 2. 회원정보 수정                │
    │ 3. 회원정보 탈퇴 및 삭제        │
    │ 4. 상위 메뉴 돌아가기           │
    └─────────────────────────────────┘
                    '''
                    customer_menu = input(customer_display)
                    
                    # 회원정보 조회(로그인후)
                    if customer_menu == '1':
                       customer.view_customer() 
                    
                    # 회원정보 수정
                    elif customer_menu == '2':
                        customer.update_customer()

                    # 회원정보 삭제
                    elif customer_menu == '3':
                        customer.withdraw_customer()
                    
                    # 상위 메뉴로 돌아가기
                    elif customer_menu == '4':
                        print('상위 메뉴로 돌아갑니다!!')
                        break
                    else:
                        print("메뉴선택이 잘못됐습니다")
                        print("올바른 메뉴를 선택해주세요")
                        continue

            # 회원정보 조회(로그인하지 않고 조회기능)
            elif cos_memu == '3':
                customer.info_customer()

            # 상위 메뉴로 돌아가기
            elif cos_memu == '4':
                print('상위 메뉴로 돌아갑니다!!')
                break
            else:
                print("메뉴선택이 잘못됐습니다")
                print("올바른 메뉴를 선택해주세요")
                continue
        continue
    
    # 2번 물품 관리 메뉴
    elif menu == '2':
        # 2번 물품 관리 하위 메뉴 활성화
        while True:
            menu2_display = '''
    ┌─────────────────────────────────┐
    │ 마켓 물류관리 프로그램 v1.01    │
    │ ◎ 물품 관리 메뉴                │
    │ 1. 물품 추가                    │
    │ 2. 입고                         │
    │ 3. 출고                         │
    │ 4. 수정                         │
    │ 5. 조회                         │
    │ 6. 삭제                         │
    │ 7. 상위 메뉴로 돌아가기         │
    └─────────────────────────────────┘
            '''
            met_memu = input(menu2_display)
            
            # 물품 db에 추가 메뉴
            if met_memu == '1':
                item.insert_item()

            # 물품 입고 관련 메뉴
            elif met_memu == '2':
                item.input_item()

            # 물품 출고 관련 메뉴
            elif met_memu == '3':
                item.output_item()

            # 물품 db 데이터 수정 메뉴
            elif met_memu == '4':
                item.update_item()

            # 물품 조회 메뉴
            elif met_memu == '5':
                item.search_item()

            # 물품 db 데이터 삭제 메뉴
            elif met_memu == '6':
                item.delete_item()

            # 상위메뉴로 돌아가기
            elif met_memu == '7':
                print('상위 메뉴로 돌아갑니다!!')
                break
            
            # 잘못된 메뉴 선택으로 while문 다시 돌아가기
            else:
                print("메뉴선택이 잘못됐습니다")
                print("올바른 메뉴를 선택해주세요")
                continue
        continue
    
    # 3번 지점 관리 메뉴
    elif menu == '3':
        # 3번 지점, 관리자 하위 메뉴 활성화
        while True:
            menu3_display = '''
    ┌─────────────────────────────────┐
    │ 마켓 물류관리 프로그램 v1.01    │
    │ ◆ 지점 관리 메뉴                │
    │ 1. 관리자 로그인                │
    │ 2. 관리자 추가, 수정, 삭제관리  │
    │ 3. 지점 추가, 수정, 삭제관리    │
    │ 4. 지점 매출 확인(로그인후 가능)│
    │ 5. 기간 매출 확인(로그인후 가능)│
    │ 6. 상위 메뉴 돌아가기           │
    └─────────────────────────────────┘
            '''
            mart_memu = input(menu3_display)

            # 관리자 로그인(하위 메뉴시 점장만 사용가능)
            if mart_memu == '1':
                buy_branch.log()

            # 관리자 추가, 수정, 삭제관리
            elif mart_memu == '2':
                print("점장만 가능합니다.")
                buy_branch.manager_update()

            # 지점 추가, 수정, 삭제관리
            elif mart_memu == '3':
                buy_branch.branch_update()

            # 지점 매출 확인
            elif mart_memu == '4':
                buy_branch.price_check_place()

            # 기간 매출 확인
            elif mart_memu == '5':
                buy_branch.price_check_time()
            
            # 상위 메뉴 돌아가기
            elif mart_memu == '6':
                print('상위 메뉴로 돌아갑니다!!')
                break

            # 잘못된 메뉴 선택으로 다시 선택하기
            else:
                print("메뉴선택이 잘못됐습니다")
                print("올바른 메뉴를 선택해주세요")
                continue
        continue
    
    # 4번 고객 물품 구매 메뉴
    elif menu == '4':
        # 4번 고객 물품 구매 하위 메뉴 활성화
        while True:
            menu3_display = '''
    ┌─────────────────────────────────┐
    │ 마켓 물류관리 프로그램 v1.01    │
    │ ◆ 고객 물품 구매 메뉴           │
    │ 1. 고객 로그인                  │
    │ 2. 물품조회   │
    │ 3. 고객 결제                    │
    │ 4. 상위 메뉴 돌아가기           │
    └─────────────────────────────────┘
            '''
            met_memu = input(menu3_display)

            # 고객 로그인(하위 메뉴 로그인후 가능)
            if met_memu == '1':
                buy_f.log()
            
            # 물품조회
            elif met_memu == '2':
                buy_f.serch()

            # 고객 결제(적립금 사용여부 및 총구매금액 고객 db저장 / 물품 db 재고 차감
            elif met_memu == '3':
                buy_f.buy()
            
            # 상위 메뉴 돌아가기
            elif met_memu == '4':
                print('상위 메뉴로 돌아갑니다!!')
                break
            
            # 잘못된 메뉴 선택으로 메뉴선택 돌아가기
            else:
                print("메뉴선택이 잘못됐습니다")
                print("올바른 메뉴를 선택해주세요")
                continue
        continue
    
    # 5번 프로그램 종료
    elif menu == '5':
        print("프로그램 종료!")
        break
    
    #그 외 키 선택시 처음으로 다시 돌아가서 메뉴 선택 창을 띄운다.
    else:
        print("메뉴를 잘못입력하셨습니다.")
        continue
