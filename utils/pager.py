
class Pagination():
    def __init__(self, totalCount, currentPage, nid, perPageItemNum=14, maxPageNum=7):
        #数据总个数
        self.total_count = totalCount
        self.currentPage = currentPage
        self.nid = nid
        #当前页
        try:
            v = int(self.currentPage)
            if v <= 0:
                self.current_page = 1
            else:
                self.current_page = v
        except Exception as e:
            self.current_page = 1
        #每页显示行数
        self.per_page_item_num = perPageItemNum
        #最多显示页码
        self.max_page_num = maxPageNum

    def start(self):
        return (self.current_page - 1) * self.per_page_item_num

    def end(self):
        return self.current_page * self.per_page_item_num

    @property
    def num_pages(self):
        a, b = divmod(self.total_count, self.per_page_item_num)
        if b == 0:
            return a
        else:
            return a + 1

    def pager_num_range(self):
        # 当前页
        # self.current_page
        # 最多显示页码数量
        # self.per_pager_number
        # 总页数
        # self.num_pages
        if self.num_pages < self.max_page_num:
            return range(1, (self.num_pages + 1))
        part = self.max_page_num // 2
        if self.current_page <= part:
            return range(1, self.max_page_num+1)
        if (self.current_page + part) > self.num_pages:
            return range((self.num_pages - self.max_page_num + 1), (self.num_pages + 1))
        return range((self.current_page - part), (self.current_page + part + 1))

    def page_str(self):
        page_list = []
        
        first = "<a href='/thickness/single-dataset-list/%s?p=1'>首页</a>" % self.nid
        page_list.append(first)

        if self.current_page == 1:
            prev = '<a href="javascript:;" data-page="">上一页</a>'
        else:
            prev = "<a href='/thickness/single-dataset-list/%s?p=%s'>上一页</a>" % (self.nid, self.current_page - 1)
        page_list.append(prev)

        for i in self.pager_num_range():
            if i == self.current_page:
                temp = '<span class="layui-laypage-curr"><em class="layui-laypage-em" style="background-color:#38c7cb;"></em><em>%s</em></span>' % (i)
            else:
                temp = '<a href="/thickness/single-dataset-list/%s?p=%s">%s</a>' % (self.nid, i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = '<a href="javascript:;" data-page="">下一页</a>'
        else:
            nex = "<a href='/thickness/single-dataset-list/%s?p=%s'>下一页</a>" % (self.nid, self.current_page + 1)
        page_list.append(nex)

        last = "<a href='/thickness/single-dataset-list/%s?p=%s'>尾页</a>" % (self.nid, self.num_pages)
        page_list.append(last)

        sp = "<span>%s/%s</span>" % (self.current_page, self.num_pages)
        page_list.append(sp)

        return ''.join(page_list)











