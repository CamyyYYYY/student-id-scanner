import cv2
import tkinter as tk
import threading
import time
from datetime import datetime
import easyocr

#stores the frame thats on (this will be the frame that gets saved as a screenshot basically)
frame = None

reader=easyocr.Reader(['en'], gpu=False)

#What Button does

def button_pressed():
    print("Scanning")

    if frame is not None:

        #save frame using current time via timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshot_{timestamp}.jpg"
        cv2.imwrite(screenshot_path, frame)
        print("Scan Saved")

        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Processing...")
        text_window.update()

        
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Student Attendance:")
        text_window.update()

        print("Processing...")
        try:
            results = reader.readtext(frame)

            text_box.delete(1.0, tk.END)

            if results:
                for i, (bbox, text, confidence) in enumerate(results, 1):
                    print(f"{i}. Student & Or School: '{text}'")
                    text_box.insert(tk.END, f"{i}. {text}\n")
                    print("-" * 40)
            else:
                print("No ID Found")
                text_box.insert(tk.END, "No ID Found")
                

        except Exception as e:
            print("Scanning error")
            text_box.insert(tk.END, "Scanning Error")
    else:
        print("Scan Not Saved, Please Try Again :(")
        text_box.insert(tk.END, "Scan Not Saved")

#camera
def camera_loop():
    global frame
    stream = cv2.VideoCapture(0)

    if not stream.isOpened():
        print ("Streaming Unavailable")
        exit()

    cv2.namedWindow("MyStudent", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("MyStudent", 740,505)
    cv2.moveWindow("MyStudent", 100, 100)  # Position camera window at specific location

    while True:
        ret, frame = stream.read()
        if not ret:
            print ("No More Streaming")
            break

        frame = frame.copy()

        cv2.imshow("MyStudent", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    stream.release()
    cv2.destroyAllWindows()

def position_button_window(): #uses time delay to keep button next to camera by suspending its use

    time.sleep(2) #wait longer for camera first

    while True: 
        try:
            camera_window=cv2.getWindowImageRect("MyStudent")

            if camera_window != (-1, -1, -1, -1): #uses negative so it works as long as the camera exists basically
                x, y, width, height = camera_window

                #where to place button
                button_x = x
                button_y = y + height + 5

                root.geometry(f"150x60+{button_x}+{button_y}") #uses button name so it can adjust x and y accordingly to button window

                text_x=button_x + 160
                text_y = button_y
                text_window.geometry(f"300x100+{text_x}+{text_y}")

                third_x=text_x+310
                third_y=button_y
                third_window.geometry(f"250x100+{third_x}+{third_y}")

            time.sleep(0.1)
        except Exception as e:
            time.sleep(0.1)

threading.Thread(target=camera_loop, daemon=True).start()

time.sleep(1) #wait for camera window first so it can be more cohesive

    #window for button
root=tk.Tk()
root.title("Scanner")
root.geometry("150x60+100+500")
root.resizable(False, False)

button=tk.Button(root, text="Scan ID", command=button_pressed)
button.pack(pady=20)

text_window=tk.Toplevel(root)
text_window.title("Results")
text_window.geometry("300x100+300+500")
text_window.resizable(False, False)

text_box=tk.Text(text_window, width=35, height=5)
text_box.pack(pady=5, padx=10)
text_box.insert(tk.END, "Scanner Is Ready")

third_window = tk.Toplevel(root)
third_window.title("Student Attendance")
third_window.geometry("250x100+610+500")
third_window.resizable(False, False)

third_box=tk.Text(third_window, width=30, height=6)
third_box.pack(pady=5, padx=20)
third_box.insert(tk.END, "Student Attendance (Type name/ ID Below!):")

threading.Thread(target=position_button_window, daemon=True).start()

root.mainloop()
