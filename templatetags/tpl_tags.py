from django.template import Library
from django.utils.safestring import mark_safe
from thickness import models

register = Library()

@register.simple_tag
def render_sorted_arrow(item, sorted_index):
    """生成排序的上下箭头html ele"""
    if item in sorted_index:  # 这一列被排序
        last_sort_index = sorted_index[item]
        if last_sort_index.startswith('-'):
            arrow_direction = 'desc'
        else:
            arrow_direction = 'asc'
        ele = """<span class="layui-table-sort layui-inline" lay-sort="%s">
                    <i class="layui-edge layui-table-sort-asc" title="升序"></i>
                    <i class="layui-edge layui-table-sort-desc" title="降序"></i>
                </span>""" % arrow_direction
    else:
        ele = """<span class="layui-table-sort layui-inline" lay-sort="">
                    <i class="layui-edge layui-table-sort-asc" title="升序"></i>
                    <i class="layui-edge layui-table-sort-desc" title="降序"></i>
                </span>"""
    return mark_safe(ele)

