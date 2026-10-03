# main.py
import cv2
import numpy as np
import socket
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label

# --- إعدادات الشبكة ---
UDP_IP = "192.168.1.100"  # ⚠️ ضع هنا عنوان IP للهاتف المستقبل
UDP_PORT = 5005

class CameraLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.camera = Image()
        self.info_label = Label(text="جاري التحميل...", size_hint=(1, 0.1))
        self.add_widget(self.camera)
        self.add_widget(self.info_label)
        
        # فتح الكاميرا
        self.capture = cv2.VideoCapture(0)
        
        # بدء التحديث الدوري (30 إطار في الثانية)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        # --- 📍 منطقة اكتشاف الكائن (هنا يوضع نموذج TFLite لاحقاً) ---
        # حالياً نستخدم إحداثيات ثابتة كتجربة لضمان نجاح البناء
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = int(w*0.3), int(h*0.3), int(w*0.7), int(h*0.7)
        
        # 1. رسم المربع الأحمر
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        # 2. حساب مركز الكائن
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # 3. إرسال الإحداثيات عبر UDP
        self.send_coordinates(center_x, center_y)
        
        # 4. تحديث الواجهة
        self.update_camera_view(frame)
        self.info_label.text = f"X: {center_x:.0f}, Y: {center_y:.0f}"

    def send_coordinates(self, x, y):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = json.dumps({"x": x, "y": y}).encode('utf-8')
            sock.sendto(data, (UDP_IP, UDP_PORT))
            sock.close()
        except Exception as e:
            print(f"خطأ في الإرسال: {e}")

    def update_camera_view(self, frame):
        # تحويل الإطار إلى تنسيق Kivy
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera.texture = texture

class ObjectTrackerApp(App):
    def build(self):
        return CameraLayout()

if __name__ == '__main__':
    ObjectTrackerApp().run()
