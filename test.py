from utils.readfiles import ReadFlies


read_path = "static/upload_files/1.lsa"
read_file = ReadFlies(read_path)

ret = read_file.handle_files()


# import time, datetime
# current_day = datetime.datetime.now()
# print(current_day.strftime("%Y-%m-%d"))
# print(type(str(current_day)))
