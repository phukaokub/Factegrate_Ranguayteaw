from time import sleep
import urllib3

'''
ตัวอย่างการอ่านข้อมูลจาก Sensor ตัวหมายเลข 0 ที่ติดตั้งอยู่ใน TeleSorting System หมายเลข 0
'''

http    = urllib3.PoolManager()

for t in range(10000):

    res = http.request( "GET",
                        "http://localhost/tss/0/sensor/0"
                        )
    text    = res.data.decode("utf-8")
    print(text)

    sleep(0.1)