from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50  # 默认每页显示多少条
    #127.0.0.1:8001/students/?page=5&page_size=10
    
    page_query_param = 'page'            # 页数关键字名
    page_size_query_param = 'page_size'  # 自定义页码的参数
    max_page_size = 10000                # 客户端请求数量最多不能超过的数值