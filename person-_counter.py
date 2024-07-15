import cv2
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class PersonCounter:
    def __init__(self, video_source=0):
        self.cap = cv2.VideoCapture(video_source)
        self.total_persons = 0
        self.persons_in_minute = 0
        self.start_time = datetime.now()
        self.current_minute = self.start_time.minute
        self.alert_threshold = 10
        
        self.root = tk.Tk()
        self.root.title("Person Counter")
        
        self.total_label = tk.Label(self.root, text="Total Persons: 0")
        self.total_label.pack()
        
        self.current_label = tk.Label(self.root, text="Persons This Minute: 0")
        self.current_label.pack()
        
        self.check_alert()
        
        self.update_gui()
        self.detect_persons()
        self.root.mainloop()
    
    def update_gui(self):
        self.total_label.config(text=f"Total Persons: {self.total_persons}")
        self.current_label.config(text=f"Persons This Minute: {self.persons_in_minute}")
        self.root.after(1000, self.update_gui)  # Update every second
    
    def check_alert(self):
        if self.persons_in_minute > self.alert_threshold:
            messagebox.showwarning("Alert", f"More than {self.alert_threshold} persons detected in the last minute!")
        self.persons_in_minute = 0
        self.start_time = datetime.now()
        self.current_minute = self.start_time.minute
        self.root.after(60000, self.check_alert)  # Check every minute
    
    def detect_persons(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Implement person detection logic using OpenCV
            
            # Dummy code for demo (replace with actual person detection logic)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Use a pre-trained cascade classifier for person detection
            # Replace 'haarcascade_fullbody.xml' with the appropriate XML file
            cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
            detections = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Increment person count only once per appearance
                self.total_persons += 1
                self.persons_in_minute += 1
            
            cv2.imshow('Person Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = PersonCounter()
