import struct, ast, array


##计时装饰器
# import time
# def timer(func):
#     def wapper():
#         start_time = time.time()
#         func()
#         end_time = time.time()
#         print('耗时%s秒' % (end_time - start_time))
#     return wapper


# from utils.readfiles import ReadFlies

# from mongoengine import connect
# connect('Thickness')

# read_path = "static/upload_files/1.lsa"
# read_file = ReadFlies(read_path)
#
# ret = read_file.handle_files()

# ret = models.DataFile.objects.filter(create_time="2019-09-08")
# for item in ret:
#     msg = eval(item.message)
#     print(msg)
# class tes(object):
#     def lsa(self):
#         print('qwer')
#
# tes = tes()
#
# read_path = "static/upload_files/1.lsa"
# Suffix = os.path.splitext(read_path)[1][1:]
# func = getattr(tes, Suffix)
# func()
# d = {}
# dic = {'Range': ' 1X,2048', 'Material': ' 碳钢,3254.0,0.53', 'Temperature': ' 25', 'Frequency': ' 高频', 'Average': ' 5', 'Gate': '', 'Detector': ' 射频波,0'}
# dic1 = {'qq': 'ww', 'Range': ' 1X,20'}
# d.update(dic)
# d.update(dic1)
# print(d)

# after_dict = {'X': '-5570820', 'Y': '-986258681', 'Thickness': '30.699756311475415', 'Gain': '60', 'Data': '2225,2891,4087,1082,0,0,1877,4089,4089,4089,1761,0,0,0,0,4066,4089,4089,4089,4089,0,0,0,0,0,4089,4089,4089,4089,787,0,0'}
#
# print([int(item) for item in after_dict['Data'].split(',')])

# li = ['2019-09-18', '', '', '2019-09-08', '', '', '2019-09-19', '', '', '2019-09-17', '', '']
# for i in range(0, len(li), 3):
#     print(li[i:i+3])
# models.DataFile.objects.create(message='qwer')


# import psycopg2
#
# conn = psycopg2.connect(database="Thickness", user="postgres", password="123456", host="localhost", port="5432")
#
# print("Opened database successfully")

# a = [{'value': '1', 'title': datetime.date(2019, 9, 20)}]
import json, datetime
# b = json.dumps(a)
# print(type(b))
#
# t = datetime.date(2019, 9, 20)
# print(t)

# l = ['2019-09-20', '2019-09-21', '2019-09-23', '2019-09-22']
# a = sorted(l)
# print(a)

#--------------------------------------------
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MeasureThickness.settings")
django.setup()
from thickness import models
# ##查询个数
# @timer
# def count_row():
#     count = models.DataFile.objects.all().count()
#     print('总行数', count)
# count_row()
##批量插入
# test_list = []
# for i in range(100):
#     test_list.append(models.Testmodel(name=i, message="{'Material': ' 碳钢,3254.0,0.53', 'Temperature': ' 25', 'Frequency': ' 高频', 'Average': ' 9', 'Gain': ' 76', 'Data': [3204, 4089, 4089, 4089, 0, 0, 0, 4089, 4089, 4089, 211, 0, 2386, 1578, 9, 0, 3846, 4089, 4089, 4089, 4089, 0, 0, 0, 0, 0, 70, 4089, 4089, 4089, 3639, 0, 0, 3478, 4089, 4089, 4089, 4089, 4089, 4082, 0, 0, 0, 0, 2039, 4089, 4089, 4089, 4089, 0, 0, 0, 0, 2044, 4089, 4089, 4089, 4089, 4089, 0, 0, 0, 0, 0, 1171, 4089, 4089, 4089, 4089, 4089, 356, 0, 0, 0, 0, 0, 3523, 4089, 4089, 4089, 4089, 4089, 0, 0, 0, 0, 0, 2035, 3066, 3146, 3457, 1569, 1026, 1614, 4089, 4089, 4089, 4089, 4087, 1303, 680, 0, 0, 0, 0, 0, 47, 347, 664, 1216, 3022, 3990, 4089, 4089, 4089, 4089, 4089, 4089, 4089, 4048, 3102, 1521, 564, 0, 0, 0, 0, 0, 0, 3, 20, 475, 1380, 2630, 3769, 4025, 4079, 4085, 4087, 4089, 4088, 4081, 4000, 3638, 2829, 1863, 965, 350, 112, 45, 27, 41, 101, 264, 633, 1237, 1873, 2498, 3069, 3510, 3742, 3835, 3841, 3763, 3602, 3333, 3007, 2665, 2345, 2063, 1817, 1612, 1452, 1337, 1276, 1275, 1328, 1416, 1533, 1677, 1834, 1998, 2162, 2305, 2409, 2467, 2487, 2476, 2443, 2407, 2369, 2322, 2265, 2212, 2168, 2131, 2101, 2076, 2050, 2027, 2018, 2018, 2024, 2034, 2048, 2065, 2087, 2114, 2138, 2153, 2160, 2163, 2161, 2159, 2162, 2164, 2163, 2156, 2147, 2139, 2138, 2143, 2147, 2149, 2138, 2118, 2093, 2079, 2081, 2097, 2115, 2130, 2143, 2151, 2156, 2156, 2147, 2135, 2127, 2125, 2121, 2117, 2114, 2117, 2126, 2139, 2150, 2153, 2149, 2140, 2129, 2119, 2114, 2117, 2126, 2130, 2125, 2112, 2108, 2130, 2173, 2209, 2204, 2155, 2078, 2013, 1991, 2029, 2124, 2251, 2361, 2385, 2280, 2066, 1838, 1711, 1762, 1986, 2298, 2570, 2686, 2586, 2300, 1940, 1650, 1548, 1665, 1945, 2270, 2512, 2596, 2513, 2316, 2090, 1913, 1837, 1866, 1967, 2094, 2200, 2258, 2267, 2243, 2202, 2161, 2126, 2097, 2075, 2066, 2071, 2091, 2122, 2153, 2172, 2176, 2162, 2140, 2117, 2102, 2100, 2105, 2114, 2128, 2145, 2160, 2166, 2158, 2138, 2117, 2106, 2106, 2116, 2127, 2137, 2139, 2135, 2130, 2132, 2137, 2140, 2136, 2127, 2119, 2117, 2119, 2124, 2127, 2129, 2133, 2142, 2152, 2155, 2146, 2129, 2112, 2102, 2101, 2110, 2128, 2146, 2157, 2156, 2143, 2126, 2114, 2113, 2122, 2135, 2142, 2139, 2128, 2119, 2116, 2120, 2131, 2141, 2147, 2147, 2140, 2131, 2123, 2114, 2111, 2113, 2119, 2129, 2138, 2145, 2151, 2151, 2143, 2131, 2120, 2116, 2114, 2115, 2117, 2120, 2126, 2137, 2149, 2155, 2152, 2141, 2127, 2115, 2110, 2112, 2120, 2129, 2136, 2138, 2135, 2131, 2132, 2134, 2134, 2130, 2126, 2126, 2131, 2134, 2133, 2129, 2126, 2125, 2127, 2130, 2132, 2134, 2135, 2134, 2134, 2131, 2126, 2116, 2111, 2117, 2133, 2148, 2152, 2144, 2132, 2126, 2126, 2129, 2130, 2126, 2124, 2124, 2126, 2126, 2126, 2131, 2138, 2141, 2139, 2135, 2133, 2130, 2123, 2111, 2104, 2110, 2129, 2151, 2165, 2163, 2147, 2126, 2114, 2109, 2110, 2112, 2115, 2120, 2133, 2152, 2165, 2165, 2147, 2123, 2104, 2098, 2104, 2114, 2127, 2140, 2151, 2153, 2143, 2128, 2116, 2121, 2133, 2143, 2139, 2127, 2117, 2115, 2122, 2129, 2131, 2131, 2131, 2132, 2137, 2146, 2153, 2151, 2133, 2107, 2085, 2083, 2102, 2132, 2161, 2178, 2181, 2166, 2139, 2105, 2080, 2074, 2092, 2124, 2155, 2173, 2170, 2150, 2126, 2109, 2103, 2109, 2126, 2151, 2169, 2167, 2143, 2108, 2077, 2064, 2078, 2115, 2163, 2204, 2214, 2191, 2144, 2097, 2071, 2069, 2085, 2110, 2134, 2150, 2158, 2160, 2157, 2151, 2142, 2131, 2118, 2105, 2097, 2098, 2107, 2127, 2149, 2164, 2163, 2148, 2131, 2118, 2114, 2119, 2130, 2139, 2141, 2133, 2119, 2109, 2113, 2129, 2148, 2155, 2145, 2126, 2111, 2109, 2119, 2133, 2145, 2153, 2152, 2138, 2118, 2104, 2105, 2118, 2134, 2144, 2147, 2144, 2137, 2130, 2122, 2118, 2120, 2126, 2133, 2136, 2134, 2135, 2137, 2136, 2130, 2121, 2115, 2116, 2128, 2143, 2152, 2146, 2130, 2114, 2108, 2115, 2130, 2143, 2150, 2147, 2141, 2130, 2119, 2107, 2098, 2102, 2124, 2156, 2179, 2175, 2150, 2121, 2105, 2101, 2105, 2112, 2125, 2141, 2153, 2153, 2143, 2129, 2119, 2110, 2100, 2101, 2118, 2153, 2190, 2207, 2188, 2134, 2070, 2025, 2024, 2064, 2134, 2206, 2251, 2251, 2204, 2128, 2053, 2009, 2010, 2056, 2124, 2184, 2218, 2220, 2201, 2171, 2135, 2096, 2066, 2054, 2063, 2088, 2118, 2151, 2179, 2196, 2200, 2186, 2150, 2103, 2063, 2053, 2071, 2109, 2148, 2175, 2182, 2170, 2147, 2124, 2109, 2105, 2109, 2118, 2128, 2137, 2143, 2141, 2134, 2129, 2131, 2134, 2134, 2129, 2124, 2121, 2125, 2129, 2132, 2132, 2131, 2131, 2130, 2130, 2132, 2138, 2142, 2141, 2131, 2119, 2112, 2114, 2124, 2129, 2129, 2128, 2131, 2139, 2148, 2152, 2150, 2137, 2115, 2099, 2098, 2114, 2136, 2152, 2155, 2144, 2129, 2121, 2124, 2136, 2142, 2135, 2118, 2101, 2093, 2105, 2132, 2162, 2176, 2170, 2150, 2127, 2111, 2109, 2123, 2141, 2145, 2123, 2083, 2053, 2062, 2113, 2188, 2251, 2273, 2240, 2161, 2061, 1975, 1944, 1984, 2080, 2191, 2276, 2303, 2271, 2199, 2113, 2043, 2007, 2014, 2056, 2113, 2159, 2181, 2179, 2168, 2160, 2158, 2150, 2134, 2113, 2098, 2094, 2101, 2115, 2131, 2143, 2149, 2148, 2139, 2130, 2125, 2126, 2130, 2134, 2139, 2137, 2128, 2117, 2111, 2112, 2119, 2130, 2142, 2153, 2159, 2156, 2141, 2123, 2108, 2104, 2109, 2115, 2124, 2133, 2142, 2148, 2148, 2143, 2134, 2127, 2123, 2122, 2121, 2120, 2119, 2122, 2130, 2139, 2145, 2144, 2138, 2129, 2126, 2130, 2136, 2135, 2125, 2116, 2112, 2116, 2124, 2132, 2137, 2143, 2153, 2161, 2155, 2129, 2097, 2077, 2085, 2116, 2152, 2173, 2176, 2165, 2146, 2126, 2104, 2085, 2079, 2094, 2127, 2157, 2167, 2159, 2147, 2144, 2150, 2148, 2128, 2098, 2079, 2085, 2112, 2146, 2168, 2171, 2158, 2135, 2109, 2091, 2093, 2119, 2158, 2187, 2185, 2150, 2099, 2058, 2051, 2079, 2128, 2177, 2209, 2216, 2195, 2149, 2093, 2052, 2046, 2073, 2113, 2144, 2159, 2164, 2167, 2169, 2165, 2149, 2126, 2105, 2091, 2088, 2098, 2113, 2130, 2143, 2152, 2159, 2159, 2152, 2141, 2129, 2119, 2114, 2112, 2111, 2110, 2116, 2126, 2137, 2150, 2160, 2163, 2153, 2128, 2100, 2080, 2083, 2111, 2154, 2190, 2201, 2182, 2137, 2084, 2046, 2041, 2075, 2136, 2198, 2230, 2219, 2170, 2108, 2064, 2058, 2091, 2137, 2152, 2114, 2041, 1996, 2051, 2229, 2456, 2594, 2521, 2206, 1727, 1299, 1181, 1503, 2169, 2921, 3428, 3425, 2866, 1981, 1137, 671, 773, 1398, 2270, 3031, 3398, 3277, 2761, 2086, 1527, 1272, 1353, 1669, 2062, 2392, 2571, 2579, 2452, 2261, 2076, 1946, 1899, 1931, 2019, 2117, 2187, 2212, 2204, 2185, 2172, 2166, 2156, 2132, 2096, 2059, 2041, 2051, 2090, 2149, 2208, 2243, 2239, 2197, 2134, 2069, 2027, 2024, 2056, 2110, 2164, 2197, 2203, 2189, 2162, 2131, 2100, 2074, 2058, 2062, 2087, 2134, 2195, 2250, 2280, 2266, 2199, 2082, 1955, 1871, 1863, 1944, 2096, 2278, 2435, 2512, 2471, 2314, 2087, 1870, 1733, 1713, 1808, 1992, 2215, 2415, 2535, 2541, 2436, 2252, 2034, 1836, 1713, 1711, 1848, 2084, 2332, 2501, 2530, 2418, 2216, 2001, 1855, 1829, 1921, 2074, 2219, 2302, 2309, 2262, 2188, 2109, 2040, 2001, 2006, 2055, 2129, 2190, 2221, 2218, 2197, 2164, 2126, 2090, 2064, 2057, 2071, 2103, 2145, 2182, 2200, 2190, 2159, 2126, 2103, 2093, 2087, 2087, 2102, 2135, 2176, 2201, 2190, 2146, 2096, 2063, 2060, 2081, 2117, 2159, 2199, 2222, 2211, 2167, 2102, 2043, 2018, 2033, 2082, 2139, 2186, 2212, 2217, 2204, 2181, 2149, 2104, 2050, 2011, 2010, 2054, 2126, 2200, 2252, 2269, 2248, 2194, 2117, 2038, 1984, 1976, 2016, 2090, 2173, 2242, 2277, 2267, 2213, 2133, 2054, 2008, 2012, 2060, 2129, 2183, 2203, 2189, 2153, 2116, 2093, 2092, 2111, 2145, 2179, 2197, 2183, 2137, 2073, 2028, 2024, 2067, 2136, 2202, 2241, 2241, 2205, 2138, 2063, 2005, 1995, 2044, 2139, 2239, 2300, 2291, 2208, 2081, 1959, 1906, 1951, 2080, 2233, 2341, 2356, 2278, 2150, 2027, 1953, 1946, 2006, 2108, 2207, 2257, 2244, 2190, 2136, 2116, 2124, 2128, 2105, 2066, 2042, 2059, 2108, 2168, 2216, 2243, 2240, 2197, 2115, 2023, 1966, 1982, 2067, 2174, 2246, 2256, 2218, 2170, 2134, 2107, 2085, 2071, 2074, 2090, 2108, 2116, 2113, 2116, 2138, 2186, 2235, 2264, 2254, 2199, 2096, 1969, 1865, 1848, 1955, 2158, 2367, 2480, 2446, 2287, 2084, 1930, 1876, 1920, 2025, 2139, 2216, 2234, 2201, 2151, 2125, 2145, 2194, 2230, 2212, 2129, 2016, 1931, 1926, 2011, 2146, 2270, 2332, 2318, 2243, 2146, 2063, 2022, 2025, 2056, 2090, 2111, 2114, 2108, 2113, 2139, 2184, 2233, 2262, 2253, 2201, 2110, 2013, 1951, 1948, 2001, 2087, 2176, 2252, 2297, 2301, 2256, 2172, 2078, 2007, 1980, 1999, 2049, 2110, 2164, 2196, 2202, 2191, 2178, 2175, 2173, 2157, 2120, 2073, 2041, 2041, 2072, 2119, 2164, 2193, 2203, 2194, 2168, 2128, 2083, 2048, 2041, 2073, 2133, 2201, 2246, 2250, 2203, 2122, 2029, 1962, 1953, 2022, 2152, 2285, 2357, 2327, 2216, 2087, 2002, 1981, 2002, 2034, 2068, 2114, 2182, 2257, 2299, 2289, 2226, 2129, 2024, 1933, 1895, 1949, 2099, 2286, 2415, 2408, 2266, 2064, 1905, 1860, 1937, 2088, 2242, 2339, 2345, 2264, 2133, 2010, 1945, 1965, 2050, 2156, 2232, 2249, 2211, 2148, 2096, 2084, 2110, 2149, 2173, 2166, 2124, 2070, 2034, 2040, 2092, 2164, 2223, 2243, 2223, 2174, 2113, 2059, 2027, 2033, 2077, 2141, 2191, 2204, 2183, 2153, 2135, 2131, 2130, 2120, 2102, 2088, 2087, 2101, 2119, 2141, 2164, 2185, 2193, 2177, 2137, 2089, 2057, 2056, 2086, 2129, 2169, 2191, 2192, 2178, 2152, 2120, 2088, 2064, 2064, 2090, 2132, 2171, 2190, 2185, 2160, 2127, 2099, 2089, 2105, 2136, 2162, 2162, 2136, 2097, 2067, 2065, 2099, 2157, 2214, 2245, 2229, 2167, 2090, 2032, 2013, 2032, 2073, 2122, 2171, 2213, 2235, 2227, 2193, 2144, 2093, 2056, 2039, 2041, 2066, 2110, 2162, 2204, 2220, 2205, 2173, 2133, 2098, 2072, 2064, 2073, 2098, 2132, 2165, 2188, 2194, 2179, 2145, 2106, 2080, 2076, 2094, 2118, 2136, 2144, 2150, 2157, 2163, 2160, 2143, 2117, 2094, 2086, 2098, 2118, 2136, 2147, 2151, 2152, 2154, 2155, 2151, 2136, 2115, 2095, 2084, 2093, 2121, 2151, 2165, 2159, 2139, 2119, 2110, 2114, 2127, 2141, 2151, 2153, 2149, 2140, 2129, 2121, 2117, 2114, 2108, 2098, 2091, 2093, 2114, 2152, 2194, 2219, 2213, 2180, 2134, 2088, 2052, 2031, 2030, 2055, 2113, 2193, 2268, 2300, 2268, 2181, 2066, 1970, 1926, 1956, 2053, 2184, 2296, 2343, 2302, 2196, 2069, 1974, 1950, 2000, 2100, 2201, 2260, 2257, 2206, 2143, 2091, 2065, 2065, 2083, 2108, 2129, 2139, 2139, 2138, 2144, 2155, 2167, 2171, 2157, 2126, 2090, 2069, 2074, 2097, 2127, 2160, 2188, 2202, 2190, 2149, 2094, 2051, 2044, 2078, 2131, 2179, 2198, 2186, 2154, 2120, 2101, 2098, 2110, 2128, 2146, 2151, 2139, 2115, 2092, 2086, 2108, 2149, 2193, 2212, 2189, 2131, 2067, 2031, 2044, 2099, 2165, 2210, 2220, 2199, 2156, 2107, 2066, 2045, 2053, 2085, 2131, 2175, 2208, 2219, 2201, 2157, 2101, 2051, 2029, 2045, 2094, 2156, 2208, 2230, 2216, 2172, 2115, 2066, 2046, 2060, 2098, 2139, 2169, 2178, 2170, 2150, 2129, 2114, 2112, 2118, 2125, 2125, 2122, 2124, 2135, 2147, 2150, 2143, 2135, 2130, 2124, 2112, 2103, 2103, 2121, 2148, 2165, 2163, 2143, 2119, 2106, 2109, 2127, 2147, 2159, 2155, 2132, 2099, 2074, 2074, 2107, 2160, 2208, 2222, 2191, 2131, 2070, 2037, 2047, 2092, 2149, 2190, 2198, 2177, 2144, 2121, 2113, 2116, 2118, 2113, 2104, 2101, 2115, 2138, 2162, 2173, 2168, 2150, 2127, 2103, 2088, 2090, 2112, 2147, 2177, 2183, 2159, 2115, 2079, 2070, 2088, 2123, 2159, 2182, 2183, 2164, 2134, 2109, 2098, 2102, 2115, 2129, 2139, 2139, 2138, 2134, 2129, 2126, 2124, 2127, 2132, 2136, 2136, 2136, 2133, 2131, 2128, 2125, 2124, 2125, 2128, 2130, 2131, 2133, 2139, 2144, 2142, 2131, 2116, 2107, 2111, 2130, 2150, 2161, 2158, 2142, 2120, 2098, 2085, 2085, 2102, 2133, 2169, 2197, 2207, 2190, 2151, 2101, 2058, 2036, 2044, 2083, 2140, 2195, 2227, 2219, 2179, 2124, 2080, 2060, 2064, 2089, 2121, 2154, 2180, 2187, 2170, 2138, 2103, 2084, 2089, 2117, 2155, 2184, 2185, 2158, 2110, 2064, 2043, 2063, 2118, 2182, 2222, 2221, 2182, 2122, 2068, 2044, 2058, 2102, 2150, 2182, 2191, 2179, 2156, 2131, 2110, 2098, 2096, 2104, 2112, 2114, 2117, 2127, 2150, 2178, 2195, 2187, 2155, 2113, 2074, 2051, 2051, 2079, 2128, 2178, 2207, 2204, 2175, 2140, 2114, 2106, 2103, 2101, 2099, 2101, 2110, 2128, 2151, 2171, 2178, 2165, 2139, 2111, 2092, 2092, 2110, 2136, 2156, 2159, 2146, 2127, 2113, 2107, 2110, 2120, 2134, 2145, 2153, 2158, 2158, 2147, 2128, 2106, 2084, 2076, 2091, 2130, 2175, 2191, 2153, 2072, 2019, 2077, 2259, 2457, 2496, 2274, 1877, 1523, 1413, 1617, 2066, 2605, 3040, 3178, 2891, 2232, 1463, 966, 991, 1498, 2191, 2729, 2923, 2795, 2501, 2207, 2001, 1892, 1855, 1864, 1905, 1966, 2048, 2149, 2258, 2351, 2392, 2354, 2245, 2103, 1981, 1919, 1929, 1994, 2082, 2166, 2229, 2264, 2262, 2227, 2165, 2098, 2050, 2031, 2043, 2075, 2114, 2152, 2178, 2193, 2196]}"))
# start = time.time()
# start_id = models.Testmodel.objects.bulk_create(test_list)
# end = time.time()
# print('用时%s秒' % (end-start))
##删除
# models.DataSetTimeID.objects.filter(nid=30).delete()

#取出最后一条
# last = models.DataFile.objects.values('message_body_data').last()['message_body_data'].tobytes()
# last1 = models.DataFile.objects.all().order_by('-nid').values('message_head', 'message_body_param', 'message_body_data')[0]
# data_set_item = models.DataFile.objects.values('message_body_param').last()
# print(last)
# print(list(struct.unpack("<6144h", last)))
# print(last1)
# print(data_set_item)

# res = models.DataSetTimeID.objects.filter(nid=9).values('dataset__data_set')
# print(res)

# li = ["{'Material': ' 碳钢,3254.0,0.53', 'Temperature': ' 25', 'Frequency': ' 高频', 'Average': ' 9'}", ]
# print(eval(li[0]))

# with open('static/upload_files/1.lsa', 'r', encoding='UTF-8') as f:
#     for i in f.readlines():
#         print(i)

# s = '4.1.lsb'
# print(s.rsplit('.', 1))
# num = round(2/7*100)
# print(num)

# dic = {'aa': '12'}
# print(dic.get('aa'))
# print(dic['aa'])
# print(dic.get('bb', 'qwer'))
# print(dic['bb'])

# head = models.DataFile.objects.all().values('message_head')[0]['message_head']
# print(head)
# print(dir(head))
# print(type(head.tobytes().decode('UTF-8')))


# print("Hello World!")
#
# b = "2225,2891,4087,1082,0,0,1877,4089,4089,4089,1761,0,0,0,0,4066,4089,4089,4089,4089,0,0,0,0,0,4089,4089,4089,4089,787,0,0,0,0,3848,4089,4089,4089,527,0,0,0,4089,4089,4089,4089,0,0,0,0,4089,4089,4089,4089,4089,0,0,0,0,2522,4089,4089,4089,4089,0,0,0,0,0,35,4089,4089,4089,4089,4089,1624,0,0,0,0,0,0,803,3546,4089,4089,4089,4089,4089,4089,3116,57,0,0,0,734,2390,2957,2463,1407,1019,929,994,2036,3292,4072,4089,4089,4089,4089,4089,4089,4069,3957,3684,2984,2288,1652,1123,714,449,330,359,512,781,1109,1457,1778,2048,2259,2407,2510,2579,2616,2619,2603,2562,2508,2443,2378,2313,2248,2197,2150,2113,2083,2055,2033,2017,2007,2007,2017,2034,2057,2077,2098,2110,2118,2130,2144,2163,2175,2183,2180,2175,2160,2151,2147,2147,2141,2134,2122,2108,2098,2097,2102,2112,2121,2126,2124,2125,2122,2124,2135,2141,2142,2144,2135,2133,2131,2130,2128,2127,2137,2143,2145,2143,2134,2124,2119,2119,2118,2121,2124,2130,2133,2135,2137,2135,2137,2135,2130,2125,2119,2116,2121,2128,2137,2141,2143,2144,2136,2131,2129,2128,2126,2123,2121,2119,2124,2129,2135,2139,2140,2138,2135,2133,2128,2125,2125,2124,2128,2129,2127,2126,2128,2130,2138,2140,2141,2134,2127,2119,2120,2122,2125,2132,2139,2142,2142,2143,2134,2125,2118,2120,2123,2128,2137,2138,2138,2135,2127,2125,2131,2135,2138,2134,2130,2128,2130,2126,2126,2129,2132,2132,2133,2132,2133,2134,2141,2133,2128,2120,2116,2117,2123,2133,2145,2149,2149,2133,2119,2113,2122,2132,2140,2141,2133,2123,2116,2118,2120,2130,2139,2149,2148,2143,2130,2121,2114,2115,2119,2125,2140,2146,2144,2140,2132,2125,2124,2121,2123,2125,2125,2127,2127,2133,2139,2141,2142,2139,2130,2123,2122,2125,2126,2128,2129,2131,2129,2128,2125,2132,2138,2143,2147,2136,2126,2115,2118,2124,2131,2129,2129,2127,2129,2135,2138,2142,2141,2136,2124,2119,2118,2119,2126,2130,2136,2144,2147,2139,2130,2120,2120,2128,2140,2143,2135,2113,2096,2090,2108,2152,2196,2218,2197,2136,2062,2015,2013,2063,2136,2212,2250,2248,2198,2127,2060,2021,2028,2072,2134,2183,2203,2197,2168,2131,2098,2084,2088,2110,2133,2152,2156,2150,2139,2124,2113,2113,2116,2126,2135,2139,2143,2144,2141,2133,2123,2117,2118,2120,2129,2135,2136,2142,2139,2135,2130,2125,2125,2126,2126,2127,2125,2126,2127,2136,2137,2138,2134,2131,2127,2129,2130,2133,2128,2126,2124,2127,2124,2125,2125,2132,2142,2145,2142,2134,2122,2118,2121,2123,2127,2129,2133,2134,2137,2138,2135,2128,2127,2128,2127,2127,2127,2130,2131,2133,2126,2127,2132,2133,2133,2135,2134,2130,2126,2125,2126,2131,2132,2130,2127,2130,2135,2139,2139,2134,2127,2122,2123,2123,2126,2133,2131,2132,2132,2133,2134,2135,2134,2131,2128,2124,2125,2123,2121,2125,2133,2136,2140,2135,2133,2127,2127,2128,2130,2130,2131,2126,2122,2122,2126,2133,2142,2145,2142,2134,2125,2124,2122,2122,2122,2125,2127,2132,2131,2137,2137,2137,2135,2130,2125,2123,2119,2121,2127,2132,2137,2135,2131,2133,2138,2150,2160,2157,2136,2099,2061,2048,2070,2117,2185,2239,2251,2219,2148,2071,2011,1995,2031,2100,2179,2228,2240,2212,2159,2105,2068,2059,2078,2104,2136,2159,2169,2166,2148,2129,2115,2111,2113,2122,2131,2140,2140,2140,2136,2132,2124,2120,2120,2119,2123,2130,2138,2145,2145,2138,2133,2124,2117,2119,2123,2129,2132,2137,2136,2135,2132,2131,2132,2135,2132,2125,2119,2117,2119,2127,2134,2141,2144,2145,2140,2130,2123,2118,2116,2118,2128,2134,2140,2139,2130,2127,2127,2130,2135,2135,2132,2128,2125,2128,2127,2123,2121,2128,2137,2141,2141,2137,2132,2124,2118,2119,2122,2122,2132,2135,2138,2140,2141,2136,2128,2125,2123,2125,2128,2129,2130,2131,2127,2126,2125,2128,2136,2145,2143,2141,2129,2122,2116,2119,2125,2130,2134,2132,2132,2132,2132,2134,2136,2132,2127,2121,2119,2120,2125,2135,2138,2142,2142,2134,2128,2125,2124,2125,2130,2130,2127,2122,2124,2127,2130,2131,2137,2135,2139,2142,2131,2123,2121,2123,2126,2126,2118,2112,2135,2181,2208,2177,2085,1982,1945,2015,2167,2312,2394,2383,2291,2141,1973,1828,1731,1745,1897,2166,2460,2677,2719,2550,2214,1841,1572,1511,1667,1972,2317,2570,2645,2530,2287,2023,1831,1767,1837,1994,2171,2308,2362,2332,2244,2127,2035,1991,2001,2055,2117,2173,2200,2200,2182,2150,2120,2099,2091,2096,2109,2121,2137,2147,2152,2147,2137,2129,2124,2127,2129,2132,2130,2127,2124,2127,2130,2132,2132,2131,2130,2132,2128,2130,2132,2135,2130,2128,2126,2124,2128,2131,2134,2136,2138,2131,2133,2130,2129,2127,2126,2122,2122,2128,2133,2137,2137,2134,2135,2133,2131,2130,2127,2125,2125,2125,2125,2127,2127,2132,2137,2137,2135,2132,2130,2130,2129,2132,2131,2125,2120,2123,2126,2131,2136,2138,2136,2135,2130,2125,2125,2126,2127,2130,2131,2126,2125,2125,2133,2144,2145,2138,2125,2114,2114,2123,2132,2137,2137,2135,2130,2130,2130,2132,2134,2130,2129,2123,2124,2121,2126,2132,2139,2140,2139,2133,2123,2123,2123,2130,2135,2133,2130,2127,2126,2126,2128,2133,2136,2136,2135,2136,2132,2135,2132,2128,2115,2106,2104,2116,2135,2157,2171,2173,2156,2130,2095,2076,2073,2094,2133,2166,2186,2182,2162,2129,2102,2084,2090,2110,2136,2154,2160,2152,2136,2123,2110,2107,2116,2136,2146,2154,2144,2131,2117,2114,2119,2125,2133,2137,2133,2133,2133,2136,2136,2135,2127,2118,2116,2116,2123,2134,2141,2144,2139,2132,2127,2130,2134,2129,2128,2124,2119,2124,2129,2132,2134,2131,2133,2135,2138,2136,2132,2128,2124,2120,2119,2123,2127,2137,2145,2143,2137,2132,2123,2121,2116,2126,2134,2135,2130,2127,2124,2129,2132,2138,2137,2136,2129,2120,2121,2126,2127,2135,2134,2131,2122,2121,2129,2136,2143,2143,2136,2128,2118,2115,2116,2122,2135,2139,2142,2140,2135,2134,2129,2123,2122,2122,2126,2125,2129,2129,2132,2141,2145,2139,2130,2124,2123,2126,2126,2125,2125,2129,2132,2132,2130,2131,2134,2141,2143,2139,2131,2120,2112,2120,2128,2134,2135,2134,2132,2135,2137,2141,2138,2132,2121,2114,2114,2116,2127,2135,2143,2150,2151,2141,2122,2103,2098,2112,2138,2166,2178,2164,2128,2081,2051,2060,2110,2172,2220,2230,2197,2137,2076,2039,2038,2068,2121,2172,2207,2212,2189,2146,2102,2069,2060,2079,2114,2150,2177,2181,2171,2145,2122,2104,2098,2103,2119,2136,2146,2148,2140,2128,2123,2119,2118,2123,2132,2141,2147,2143,2136,2123,2117,2116,2121,2125,2136,2141,2142,2139,2134,2130,2126,2124,2125,2125,2126,2128,2131,2129,2130,2132,2136,2136,2137,2133,2130,2130,2128,2126,2124,2123,2121,2124,2126,2135,2144,2150,2142,2134,2120,2120,2121,2126,2130,2130,2127,2125,2126,2133,2136,2139,2140,2133,2125,2118,2116,2120,2127,2135,2141,2139,2138,2133,2129,2124,2126,2127,2130,2133,2127,2122,2116,2121,2133,2145,2146,2144,2140,2128,2118,2115,2120,2126,2135,2137,2135,2129,2125,2126,2130,2137,2138,2136,2133,2129,2123,2120,2121,2122,2130,2139,2140,2139,2134,2134,2134,2135,2131,2122,2115,2118,2121,2130,2134,2140,2144,2140,2134,2127,2120,2119,2128,2135,2139,2138,2132,2124,2121,2123,2129,2133,2141,2141,2132,2125,2119,2122,2124,2127,2131,2139,2143,2147,2143,2134,2122,2110,2102,2113,2134,2154,2160,2149,2125,2105,2104,2115,2138,2160,2161,2152,2131,2110,2097,2096,2113,2135,2155,2165,2161,2145,2130,2111,2105,2102,2108,2123,2138,2148,2149,2146,2142,2135,2127,2120,2119,2121,2125,2128,2133,2133,2131,2125,2126,2132,2137,2139,2139,2134,2131,2128,2129,2127,2125,2122,2118,2122,2132,2141,2149,2149,2145,2135,2120,2112,2111,2115,2122,2131,2138,2146,2150,2146,2133,2128,2121,2120,2123,2130,2130,2131,2130,2130,2130,2134,2139,2142,2139,2131,2120,2116,2117,2126,2136,2137,2137,2128,2126,2130,2137,2139,2142,2137,2126,2119,2113,2112,2120,2133,2141,2142,2141,2135,2129,2129,2132,2130,2129,2124,2122,2122,2125,2128,2134,2137,2143,2138,2134,2128,2122,2121,2126,2130,2132,2130,2132,2133,2133,2131,2128,2130,2135,2138,2136,2130,2124,2116,2116,2123,2134,2143,2150,2147,2138,2132,2123,2114,2112,2114,2122,2132,2144,2142,2136,2132,2129,2135,2138,2137,2129,2119,2112,2111,2118,2134,2164,2191,2209,2180,2090,1964,1882,1923,2124,2427,2659,2648,2312,1774,1300,1190,1579,2328,3074,3418,3143,2354,1425,803,791,1380,2283,3094,3456,3235,2569,1779,1200,1049,1342,1910,2496,2858,2888,2631,2227,1852,1651,1654,1827,2074,2294,2415,2412,2316,2177,2050,1976,1964,2010,2085,2161,2211,2225,2208,2174,2130,2091,2073,2072,2091,2118,2148,2166,2169,2159,2142,2126,2113,2108,2113,2123,2130,2135,2135,2130,2130,2128,2135,2143,2143,2138,2129,2116,2114,2120,2129,2138,2142,2136,2131,2126,2126,2131,2133,2130,2133,2132,2132,2133,2131,2129,2124,2121,2126,2131,2145,2146,2140,2129,2118,2117,2119,2127,2135,2139,2139,2133,2127,2128,2132,2134,2132,2130,2127,2127,2128,2132,2132,2130,2128,2130,2131,2130,2131,2136,2137,2136,2133,2124,2117,2117,2117,2128,2136,2147,2149,2142,2131,2120,2118,2121,2128,2131,2130,2131,2132,2132,2132,2133,2131,2138,2134,2129,2122,2114,2117,2126,2139,2144,2140,2133,2127,2124,2121,2130,2133,2130,2128,2129,2130,2133,2132,2129,2125,2124,2126,2133,2141,2142,2137,2126,2117,2110,2119,2125,2138,2142,2142,2137,2128,2124,2126,2128,2133,2136,2130,2127,2123,2120,2120,2126,2138,2147,2153,2148,2135,2124,2112,2111,2113,2121,2132,2138,2143,2143,2141,2138,2132,2125,2123,2123,2123,2127,2127,2130,2129,2134,2140,2141,2137,2133,2126,2119,2120,2123,2129,2132,2134,2135,2138,2134,2131,2130,2127,2128,2128,2127,2128,2128,2127,2131,2135,2129,2127,2131,2137,2137,2136,2133,2128,2129,2123,2121,2121,2125,2130,2135,2141,2139,2136,2131,2126,2120,2117,2120,2126,2137,2143,2142,2137,2132,2125,2124,2130,2134,2135,2129,2125,2121,2122,2126,2132,2134,2134,2135,2137,2136,2133,2128,2128,2129,2132,2128,2126,2124,2125,2126,2133,2137,2142,2143,2139,2127,2113,2106,2111,2126,2137,2145,2142,2138,2133,2133,2130,2132,2130,2128,2125,2126,2127,2128,2124,2123,2125,2134,2144,2146,2143,2134,2122,2113,2117,2123,2131,2139,2136,2133,2126,2127,2132,2134,2137,2134,2130,2130,2126,2119,2111,2109,2120,2145,2169,2179,2165,2134,2095,2067,2070,2097,2134,2168,2191,2190,2172,2137,2096,2064,2056,2075,2122,2178,2210,2205,2167,2117,2069,2052,2063,2105,2156,2196,2212,2192,2150,2098,2069,2061,2083,2120,2157,2179,2179,2157,2130,2115,2106,2111,2116,2121,2128,2130,2135,2141,2149,2147,2144,2136,2120,2112,2111,2121,2126,2131,2139,2140,2133,2132,2129,2131,2133,2134,2132,2128,2120,2118,2121,2131,2138,2143,2137,2132,2128,2124,2129,2135,2136,2132,2126,2120,2123,2125,2124,2128,2132,2135,2138,2138,2138,2134,2130,2125,2120,2119,2121,2128,2132,2140,2139,2135,2134,2132,2131,2129,2126,2120,2113,2115,2128,2140,2147,2146,2142,2132,2125,2121,2120,2121,2124,2130,2133,2136,2133,2129,2124,2125,2133,2140,2141,2138,2131,2122,2115,2117,2123,2133,2136,2137,2132,2128"
#
# start = time.time()
# for i in range(3150):
#     c = tuple([int(item) for item in b.split(',')])
# print(len(c))
# bts = struct.pack("<2048h", *c)
# end = time.time()
# print('pack时间：', end - start)
# print(bts)
#
# d = struct.unpack("<2048h", bts)
# print(d)

# for i in range(3150):
#     c = tuple([int(item) for item in b.split(',')])
#     a =array.array("h", c)
# bts = a.tobytes()
# print(bts)
# b = b.strip("'").split(',')
# print(b)
# print(type(b))
# print(list(map(int, b)))

# from utils.handel_data import HandleImgs
#
# hand = HandleImgs()
# hand.compress_image('static/upload-imgs/beizi.jpg')

# ll = {'q', 'w', 'e', 'r'}
# lll = {'a', 's', 'e'}
#
# print(ll - lll)

# dic = {'status': True, 'data_list': [{'time': '2019-11-15', 'data_id': 4, 'thickness': ''}, {'time': '2019-11-15', 'data_id': 5, 'thickness': ''}, {'time': '2019-11-08', 'data_id': 1, 'thickness': ''}, {'time': '2019-11-08', 'data_id': 2, 'thickness': ''}]}
#
# print(json.dumps(dic))
# data_obj = models.VersionToThcikness.objects.filter(data_id=12, version='2').values('data_id', 'version__version', 'run_alg_thickness')[0]
# print(data_obj)
# li = "(3, 4, 11, 12, 13)"
# li = '(20, 21, 22, 23, 24, 25)'
# try:
#     ret = models.VersionToThcikness.objects.raw("select id, data_id_id, run_alg_thickness from thickness_versiontothcikness where data_id_id in %s and version_id=3 order by data_id_id" % li)
#     for item in ret:
#         print(item)
# except Exception as e:
#     print(e)
# try:  # 批量查找
#     dataset_id_list_obj = models.VersionToThcikness.objects.raw(
#         "select id, data_id_id, deviation from thickness_versiontothcikness where data_id_id in %s and version_id=%s order by data_id_id" % (li, '2'))
#     print(dataset_id_list_obj)
#     for data_item in dataset_id_list_obj:
#         # data_id = data_item.data_id_id
#         # deviation = data_item.deviation
#         # print(data_id)
#         # print(deviation)
#         print('data_item', data_item)
# except:
#     pass

# from decimal import Decimal
# def export_result(num):
#     """不四舍五入保留1位小数"""
#     num_x, num_y = str(num).split('.')
#     num = float(num_x + '.' + num_y[0:1])
#     return num
# deviation = abs(Decimal('20') - Decimal('20.7'))
# print(deviation)
# count = 0
# test_list = [48376, 48377, 48378, 48379, 48380, 48381, 48382, 48383, 48384, 48385, 48386, 48387, 48388, 48389, 48390, 48391, 48392, 48393, 48394, 48395, 48396, 48397, 48398, 48399, 48400, 48401, 48402, 48403, 48404, 48405, 48406, 48407, 48408,48409, 48410, 48411, 48412, 48413, 48414, 48415, 48416, 48417, 48418, 48419, 48420, 48421, 48422, 48423, 48424, 48425, 48426, 48427, 48428, 48429, 48430, 48431, 48432, 48433, 48434, 48435, 48436, 48437, 48438, 48439, 48440, 48441, 48442, 48443, 48444, 48445, 48446, 48447, 48448, 48449, 48450, 48451, 48452, 48453, 48454, 48455, 48456, 48457, 48458, 48459, 48460, 48461, 48462, 48463, 48464, 48465, 48466, 48467, 48468, 48469, 48470, 48471, 48472, 48473, 48474, 48475, 48476, 48477, 48478, 48479, 48480, 48481, 48482, 48483, 48484, 48485, 48486, 48487, 48488, 48489, 48490, 48491, 48492, 48493, 48494, 48495, 48496, 48497, 48498, 48499, 48500, 48501, 48502, 48503, 48504, 48505, 48506, 48507, 48508, 48509, 48510, 48511, 48512, 48513, 48514, 48515, 48516, 48517, 48518, 48519, 48520, 48521, 48522, 48523, 48524, 48525, 48526, 48527, 48528, 48529, 48530, 48531, 48532, 48533, 48534, 48535, 48536, 48537, 48538, 48539, 48540, 48541, 48542, 48543, 48544, 48545, 48546, 48547, 48548, 48549, 48550, 48551, 48552, 48553, 48554, 48555, 48556, 48557, 48558, 48559, 48560, 48561, 48562, 48563, 48564, 48565, 48566, 48567, 48568, 48569, 48570, 48571, 48572, 48573, 48574, 48575, 48576, 48577, 48578, 48579, 48580, 48581, 48582, 48583, 48584, 48585, 48586, 48587, 48588, 48589, 48590, 48591, 48592, 48593, 48594, 48595, 48596, 48597]
# test_list = str(tuple(test_list))
#
# id_list = []
# data_id_list_obj = models.DataFile.objects.raw("select nid, message_head, message_body_data, message_body_param from thickness_datafile where nid in %s" % test_list)
# print(data_id_list_obj.__dir__())
# print(data_id_list_obj.__sizeof__())

# data_obj = models.DataFile.objects.filter(file_name_id=28).order_by('nid')
# print(data_obj)
# data_id_list = []
# for i in data_obj:
#     data_id_list.append(i.nid)
# print(data_id_list)
# t1 = time.time()
# data_time_condition_obj = models.DataSetCondition.objects.filter(id=37).values('time_and_id', 'data_set_id')[0]
# data_set_id = eval(data_time_condition_obj['data_set_id'])
# data_set_id = str(tuple(data_set_id))
# # # 查找所以的存在的数据id，防止删除了文件或者部分数据，已存储的数据id不对
# data_id_list_obj = models.DataFile.objects.raw("select nid, message_head, message_body_data, message_body_param from thickness_datafile where nid in (18988)")
# # count = data_id_list_obj.__len__()
# count = 0
# for i in data_id_list_obj:
#     count += 1
# print(count)
# tup = "(12,)"
# tup = tup.replace(',', '')
# print(tup)
# nid = 28
# data_obj = models.DataFile.objects.filter(file_name_id=nid).order_by('nid')
# count = data_obj.count()
# try:
#     file_obj = models.DataFile.objects.values('file_name_id', 'file_name__file_name').filter(
#         file_name_id=nid).first()
#     file_name = file_obj['file_name__file_name']
#     file_id = file_obj['file_name_id']
# except:
#     pass
# data_obj = models.DataFile.objects.filter(file_name_id=28).order_by('nid')
#
# file_obj = data_obj.values('file_name_id', 'file_name__file_name').first()
# print(file_obj)
# import base64, json
# data = '这里是要加密的内容！'
# json_data = json.dumps(data)
# a = base64.b64encode(json_data.encode('utf-8'))
# print(a)
# b = base64.b64decode(a.decode('utf-8'))
# print(json.loads(b))
a = (53989, 53990, 53991, 53992, 53993, 53994, 53995, 53996, 53997, 53998, 53999, 54000, 54001, 54002, 54003, 54004, 54005, 54006, 54007, 54008, 54009, 54010, 54011, 54012, 54013, 54014, 54015, 54016, 54017, 54018, 54019, 54020, 54021, 54023, 54024, 54025, 54026, 54027, 54029, 54032, 54033, 54034, 54036, 54040, 54043, 54047, 54050, 54053, 54057, 54069, 54072, 54075, 54078, 54081, 54082, 54083, 54084, 54085, 54086, 54087, 54088, 54089, 54090, 54091, 54092, 54093, 54094, 54095, 54096, 54097)

create_time = models.DataTag.objects.values('create_time').first()['create_time']
print(str(create_time).split('.')[0])