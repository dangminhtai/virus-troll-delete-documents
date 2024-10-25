import tkinter as tk
import os
import threading
import time
import random
from tkinter import messagebox

# Biến toàn cục để lưu trữ danh sách các tệp tin cần xóa
files_to_delete = []
current_file_index = 0
allow_closing = False  # Biến để kiểm tra xem có cho phép đóng cửa sổ hay không
start_time = None  # Thời gian bắt đầu
is_scanning = False  # Biến để kiểm soát quá trình quét

# Biến để đếm số lượng file theo loại
file_counts = {
    '.txt': 0,
    '.jpg': 0,
    '.png': 0,
    '.docx': 0,
    '.pdf': 0
}

# Hàm để quét và xóa tệp tin (giả)
def scan_and_delete():
    global current_file_index, start_time, is_scanning
    file_types = ['.txt', '.jpg', '.png', '.docx', '.pdf']
    
    # Xóa nội dung trong Text widget trước khi hiển thị mới
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Đang quét...\n")
    root.update()

    # Ghi lại thời gian bắt đầu
    start_time = time.time()
    is_scanning = True  # Bắt đầu quét

    # Duyệt qua tất cả các ổ đĩa
    for drive in range(65, 91):  # Từ A (65) đến Z (90)
        drive_letter = f"{chr(drive)}:/"
        if os.path.exists(drive_letter):
            if drive_letter == "C:/":
                # Chỉ quét thư mục Documents trên ổ C:
                documents_path = os.path.join(os.path.expanduser("~"), "Documents")
                if os.path.exists(documents_path):
                    for root_dir, dirs, files in os.walk(documents_path):
                        for file in files:
                            file_type = os.path.splitext(file)[1]
                            if file_type in file_types:
                                # Tạo thông điệp để hiển thị
                                file_path = os.path.join(root_dir, file)
                                message = f"Đang xóa file: {file_path}\n"
                                output_text.insert(tk.END, message)
                                root.update()

                                # Cập nhật số lượng file đã xóa
                                file_counts[file_type] += 1

                                current_file_index += 1
                                output_text.see(tk.END)  # Cuộn đến cuối Text widget

                                # Thay đổi thời gian nghỉ giữa các thông báo
                                time.sleep(0.05)  # Thời gian nghỉ 1 giây khi xóa ở ổ C
            else:
                # Duyệt các thư mục khác trên các ổ đĩa khác
                for root_dir, dirs, files in os.walk(drive_letter):
                    for file in files:
                        file_type = os.path.splitext(file)[1]
                        if file_type in file_types:
                            # Tạo thông điệp để hiển thị
                            file_path = os.path.join(root_dir, file)
                            message = f"Đang xóa file: {file_path}\n"
                            output_text.insert(tk.END, message)
                            root.update()

                            # Cập nhật số lượng file đã xóa
                            file_counts[file_type] += 1

                            current_file_index += 1
                            output_text.see(tk.END)  # Cuộn đến cuối Text widget

                            # Thay đổi thời gian nghỉ giữa các thông báo
                            root.after(1)  # Giữ cho ứng dụng mượt mà

    # Thông báo hoàn tất
    output_text.insert(tk.END, "Quá trình quét và xóa hoàn tất.\n")
    output_text.see(tk.END)  # Cuộn đến cuối sau khi hoàn tất

    # Thông báo số lượng file đã xóa
    deleted_message = (
        f"Đã xóa:\n"
        f"- {file_counts['.txt']} file .txt\n"
        f"- {file_counts['.jpg']} file .jpg\n"
        f"- {file_counts['.png']} file .png\n"
        f"- {file_counts['.docx']} file .docx\n"
        f"- {file_counts['.pdf']} file .pdf\n"
    )
    output_text.insert(tk.END, deleted_message)
    
    # Cho phép đóng cửa sổ sau 30 giây
    global allow_closing
    allow_closing = True
    output_text.insert(tk.END, "Troll thôi mà, đừng dỗi nhé ~ \n", "red")  # Thêm tag "red"
    output_text.see(tk.END)
    is_scanning = False  # Kết thúc quá trình quét

# Hàm để cập nhật thời gian đã trôi qua
def update_timer():
    if start_time is not None and is_scanning:  # Chỉ cập nhật nếu đang quét
        elapsed_time = time.time() - start_time  # Tính thời gian đã trôi qua
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text=f"Thời gian xóa tệp tin  {hours:02}:{minutes:02}:{seconds:02}")  # Cập nhật label
    root.after(1000, update_timer)  # Cập nhật mỗi giây

# Hàm để bắt đầu quá trình quét và xóa tệp trong luồng riêng
def start_deletion():
    global current_file_index, file_counts
    current_file_index = 0  # Reset chỉ số
    file_counts = {key: 0 for key in file_counts}  # Reset số lượng file
    button_start.config(state=tk.DISABLED)  # Vô hiệu hóa nút

    # Tạo Label cho thời gian đã trôi qua chỉ khi nhấn nút
    global timer_label
    timer_label = tk.Label(frame_controls, text="Thời gian xóa tệp tin 00:00:00", font=('Arial', 14,'bold'), bg='lightblue',fg='white')
    timer_label.pack(side=tk.TOP, pady=10)  # Đặt Label ngay bên trên nút

    # Reset thời gian hiển thị
    # timer_label.config(text="Thời gian đã trôi qua: 00:00:00")
    threading.Thread(target=scan_and_delete).start()
    update_timer()  # Bắt đầu cập nhật thời gian

    # Bắt đầu bộ đếm thời gian 20 giây sau khi nhấn nút
    root.after(20000, allow_closing_after_delay)

# Hàm để hiển thị thông điệp troll
def show_message():
    message_window = tk.Tk()
    message_window.title("Virus Angry")
    message_window.configure(bg="lightblue")  # Màu nền xanh nhạt

    label = tk.Label(message_window, text="Virus đang buồn, hệ thống tự động phá hủy...", 
                     font=("Arial", 20, "bold"), bg="lightblue", fg="white")
    label.pack(padx=20, pady=20)
    message_window.iconbitmap('virus.ico')
    message_window.after(5000, message_window.destroy)

    screen_width = message_window.winfo_screenwidth()
    screen_height = message_window.winfo_screenheight()
    x = random.randint(0, screen_width - 300)
    y = random.randint(0, screen_height - 200)
    message_window.geometry(f"+{x}+{y}")
    message_window.mainloop()

# Hàm để tạo sự kiện troll nhiều lần trước khi đóng ứng dụng
def troll():
    for _ in range(200):  # Hiển thị thông báo 200 lần
        threading.Thread(target=show_message).start()
        time.sleep(0.03)  
    root.destroy()

# Hàm để xử lý sự kiện khi nhấn "Ừm" trong hộp thoại
def on_yes():
    threading.Thread(target=troll).start()

# Hàm ngăn chặn đóng cửa sổ
def on_closing():
    if not allow_closing:  # Nếu chưa được phép đóng
        return  
    # Tạo một hộp thoại tùy chỉnh
    dialog = tk.Toplevel(root)
    dialog.title("Virus Question")
    dialog.geometry("300x150")
    dialog.configure(bg='lightblue')
    dialog.iconbitmap('virus.ico')
    message = tk.Label(dialog, text="Bạn giận tôi rồi sao ಥ_ಥ", bg='lightblue',fg='white',font=("Arial", 13,"bold"))
    message.pack(pady=20)

    # Nút "Ừm" và "Hơm"
    button_frame = tk.Frame(dialog, bg='lightblue')
    button_frame.pack(pady=10)

    # Nút "Ừm"
    yes_button = tk.Button(button_frame, text="Ừm", command=on_yes, bg='white', fg='lightblue', width=10,font=("Arial", 10,"bold"))
    yes_button.pack(side=tk.LEFT, padx=5)

    # Nút "Hơm"
    no_button = tk.Button(button_frame, text="Hơm", command=dialog.destroy, bg='white', fg='lightblue', width=10,font=("Arial", 10,"bold"))
    no_button.pack(side=tk.LEFT, padx=5)

    dialog.iconbitmap('virus.ico')  

# Hàm cho phép đóng cửa sổ sau 20 giây
def allow_closing_after_delay():
    global allow_closing
    allow_closing = True

# Tạo giao diện ứng dụng
root = tk.Tk()
root.title("Virus Thân Thiện")
root.iconbitmap('virus.ico')
root.geometry("600x400")
root.configure(bg="lightblue")
frame_controls = tk.Frame(root, bg="lightblue")
frame_controls.pack(pady=10)

button_start = tk.Button(frame_controls, text="Ấn zô đi :))", font=("Arial", 16), command=start_deletion, bg='white', fg='lightblue')
button_start.pack(pady=10)

output_text = tk.Text(root, wrap=tk.WORD, width=70, height=15, font=("Arial", 10))
output_text.tag_configure("red", foreground="red")
output_text.pack(pady=10)

# Xử lý khi đóng cửa sổ
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
