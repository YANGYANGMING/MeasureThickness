class LayuiPager(object):
    """Layui的分页，功能全"""
    def __init__(self, request, obj):
        self.request = request
        self.obj = list(obj)

    def pager(self):
        result = {'status': False, 'data_list': []}
        pageSize = int(self.request.POST.get('limit'))  # 每页显示的条数
        currentPage = int(self.request.POST.get('curr_page'))
        if currentPage == 1:
            start_range = currentPage - 1
            end_range = currentPage * pageSize
        else:
            start_range = (currentPage - 1) * pageSize
            end_range = currentPage * pageSize

        result['data_list'] = self.obj[start_range: end_range]
        result['status'] = True

        return result
