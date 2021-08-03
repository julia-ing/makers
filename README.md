# makers
보안 공부를 위해 만든 개인 웹 프로젝트 <보안ING>
### 스택 : flask + mongodb 

<주요기능>
- 로그인 회원가입 기능 
- 뉴스 페이지 : 오늘의 뉴스, 주간 뉴스 크롤링 with requests + bs4
- 공모전 페이지 : 콘테스트코리아 크롤링
- 채용 페이지 : 자신이 원하는 기업의 링크와 간단한 메모를 저장, 저장 시 ogimage 노출, 회원마다 자신이 작성한 페이지로 연결
- 스터디 페이지 : 스터디 카테고리 및 레벨 CRUD 기능, 3일마다 페이지 변경, 회원마다 자신이 작성한 페이지로 연결

<db 관리>
- 유저 정보 관리 -> 채용 & 스터디 페이지 관리 (nosql mongodb)
