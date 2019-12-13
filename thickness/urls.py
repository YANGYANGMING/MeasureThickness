
from django.urls import re_path
from thickness.views import home, DataSet

urlpatterns = [

    re_path(r'^index/$', home.IndexView.as_view()),

    re_path(r'^change-pwd/$', home.ChangepwdView.as_view()),

    re_path(r'^upload-file/$', DataSet.UploadFileView.as_view()),

    re_path(r'^tag-manage/$', DataSet.tag_manage),
    re_path(r'^tag-manage-ajax/$', DataSet.tag_manage_ajax),

    re_path(r'^single-file-data/(\d+)$', DataSet.single_file_data, name='single_file_data'),
    re_path(r'^single-file-run-alg-ajax/$', DataSet.single_file_run_alg_ajax),

    re_path(r'^generate-dataset/$', DataSet.GenerateDataSetView.as_view()),

    re_path(r'^dataset-condition-list/$', DataSet.dataset_condition_list),

    re_path(r'^generate-dataset-ajax/$', DataSet.generate_dataset_ajax),

    re_path(r'^callback-zero-ajax/$', DataSet.callback_zero),

    re_path(r'^dataset-run-alg-ajax/$', DataSet.dataset_run_alg_ajax),
    re_path(r'^remove-dataset-ajax/$', DataSet.remove_dataset_ajax),

    re_path(r'^single-dataset-list/(\d+)$', DataSet.single_dataset_list, name='single_dataset_list'),
    re_path(r'^data-2048-chart/(\d+)/(-?\d+\.?\d*)$', DataSet.data_2048_chart, name='data_2048_chart'),

    re_path(r'^test/$', DataSet.test),

]
