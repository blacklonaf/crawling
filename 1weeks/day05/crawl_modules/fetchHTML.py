import requests

def fetch_html(url, timeout=10): # timeout 변수 기본 값을 10으로 초기화 / 변수 기본 값으로, 이는 함수 실행해서 누락하면 기본 값 적용
    try:
        resp = requests.get(url, timeout=timeout) # timeout 판단 기준을 10초로 지정
        resp.raise_for_status # 상태 코드가 4xx(클라이언트 오류), 5xx(서버 오류)일 때, HTTPError 예외를 발생시킨다.
        # 단순 상태 코드를 반환하고 싶은 경우, resp.status_code를 이용

    except requests.exceptions.Timeout: # 타임아웃 예외가 발생했을 경우
        print(f"[ERROR] 요청 시간 초과 : {url}")
        return None
    except requests.exceptions.HTTPError as e: # HTTPError가 발생했을 경우
        print(f"[ERROR] HTTP 에러({e.response.status_code}) : {url}")
        return None
    except requests.exceptions.RequestException as e: # 이외의 모든 에러가 발생했을 경우,
        print(f"[ERROR] 요청 중 예외 발생 : {e}") # 해당 에러 내용을 그대로 출력함.
        return None
    else:
        return resp.text
    finally:
        print("finally는 예외처리 상관없이 항상 실행") 
        # 이는 db 연결 해제, 파일 세션 닫기 등 결과에 상관없이 수행되어야하는 동작에 적용한다.