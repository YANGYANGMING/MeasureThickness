
from django.urls import re_path
from thickness.views import home, DataSet

urlpatterns = [

    re_path(r'^index/$', home.IndexView.as_view()),

    re_path(r'^change-pwd/$', home.ChangepwdView.as_view()),

    re_path(r'^upload-file/$', DataSet.UploadFileView.as_view()),

    re_path(r'^tag-manage/$', DataSet.tag_manage),
    re_path(r'^tag-manage-save-ajax/$', DataSet.tag_manage_save_ajax),

    re_path(r'^single-file-data/(\d+)/(.*)$', DataSet.single_file_data, name='single_file_data'),
    re_path(r'^single-file-run-alg-ajax/$', DataSet.single_file_run_alg_ajax),
    re_path(r'^select-version-ajax/$', DataSet.select_version_ajax),
    re_path(r'^batch-save-true-thickness-ajax/$', DataSet.batch_save_true_thickness_ajax),
    re_path(r'^remove-data-ajax/$', DataSet.remove_data_ajax),

    re_path(r'^generate-dataset-by-time/$', DataSet.GenerateDataSetView.as_view()),
    re_path(r'^generate-dataset-by-file-ajax/$', DataSet.generate_dataset_by_file_ajax),
    re_path(r'^remove-file-ajax/$', DataSet.remove_file_ajax),
    re_path(r'^search-tag-ajax/$', DataSet.search_file_ajax),

    re_path(r'^dataset-condition-list/$', DataSet.dataset_condition_list),
    re_path(r'^save-dataset-tag-ajax/$', DataSet.save_dataset_tag_ajax),

    re_path(r'^generate-dataset-ajax/$', DataSet.generate_dataset_ajax),

    re_path(r'^callback-zero-ajax/$', DataSet.callback_zero),

    re_path(r'^dataset-run-alg-ajax/$', DataSet.dataset_run_alg_ajax),
    re_path(r'^remove-dataset-ajax/$', DataSet.remove_dataset_ajax),

    re_path(r'^single-dataset-list/(\d+)$', DataSet.single_dataset_list, name='single_dataset_list'),
    re_path(r'^data-2048-chart/(\d+)/(-?\d+\.?\d*)$', DataSet.data_2048_chart, name='data_2048_chart'),
    re_path(r'^submit-true-thickness-ajax/$', DataSet.submit_true_thickness),

    re_path(r'^deviation-rate/(\d+)/(\w+)/$', DataSet.DeviationRate.as_view()),
    re_path(r'^deviation-rate-ajax/(\d+)/(\w+)/$', DataSet.deviation_rate_ajax),
    re_path(r'^column-click-event-ajax/(\d+)/$', DataSet.column_click_event_ajax),

    re_path(r'^alg-api/$', DataSet.AlgAPI.as_view()),

    re_path(r'^test/$', DataSet.test),

]
