# SỬ DỤNG EMAIL HỖ TRỢ ĐIỀU KHIỂN QUẢN TRỊ MÁY TÍNH TỪ XA

## Mục đích

Chương trình này được cài đặt nhằm có thể điều khiển máy tính cá nhân ở bất kì đâu thông qua việc gửi email và yêu cầu máy tính thực hiện mệnh lệnh bao gồm các chức năng chính:

* In ra cây thư mục gốc là thư mục có đường dẫn \<Path\>.
* In tất cả thư mục, file nằm trong thư mục có đường dẫn \<Path\>.
* In tất cả ổ đĩa trong máy tính.
* Xóa file có đường dẫn \<Path\>.
* Sao chép tệp đính kèm từ email được gửi từ client vào server tới đường dẫn \<Path\>.
* In ra tất cả ứng dụng đang chạy kèm port ID và thread.
* In ra tất cả tiến trình đang chạy kèm port ID và thread.
* Tắt tiến trình đang chạy tại port \<PortID\>.
* Mở ứng dụng \<App\>.
* Tắt/mở theo dõi bàn phím.
* In ra các phím đã bấm kèm thời gian.
* Khóa bàn phím.
* Mở khóa bàn phím.
* Chụp màn hình.
* Ghi màn hình \<n_seconds\> giây.
* Tắt máy.
* Đăng xuất tài khoản hiện tại trên máy.
* Quay camera <n_seconds> giây.
* Lấy giá trị của <name_value> tại key có đường dẫn \<Path\> của registry.
* Đặt giá trị của \<name_value\> tại key có đường dẫn \<Path\> của registry thành giá trị \<value\> với kiểu dữ liệu là \<value\> (\<value\> là một trong những giá trị ['REG_SZ', 'REG_BINARY', 'REG_DWORD', 'REG_QWORD', 'REG_MULTI_SZ', 'REG_EXPAND_SZ']).
* Tạo key \<Path\>.
* Xóa key \<Path\>.
## Cấu trúc chương trình

Mã nguồn chương trình gồm các file và folder sau:

* Folder <span style="color:red">**assets** </span> là ảnh của các button được sử dụng để xây dựng GUI.
* Folder <span style="color:red">**function** </span> chứa các file thực hiện các chức năng:
    * <span style="color:red">**utilities.py** </span> xử lý chuyển đối tượng về HTML.
    * <span style="color:red">**listener.py** </span> xử lý nhận mệnh lệnh từ email của client và từ đó gọi hàm để thực hiện mệnh lệnh.
    * <span style="color:red">**directory_tree_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**DIRECTORY** </span> như:
        * DIRECTORY LISTALL \<Path\>: in ra cây thư mục gốc là thư mục \<Path\>.
        * DIRECTORY LISTDIR \<Path\>: in ra tất cả thư mục, file nằm trong thư mục \<Path\>.
        * DIRECTORY LISTDISK: in ra tất cả ổ đĩa trong máy tính.
        * DIRECTORY DELETE \<Path\>: xóa file có đường dẫn \<Path\>.
        * DIRECTORY COPY \<Path\>: copy file từ file đính kèm tại email vào thư mục \<Path\>.
    * <span style="color:red">**app_process_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**PROCESS** </span> như:
        * PROCESS LISTAPPS: in ra tất cả ứng dụng đang chạy kèm port ID và thread.
        * PROCESS LISTPROCESSES: in ra tất cả tiến trình đang chạy kèm port ID và thread.
        * PROCESS KILL \<PortID\>: tắt tiến trình đang chạy tại port \<PortID\>.
        * PROCESS START \<App\>: mở ứng dụng \<App\>.
    * <span style="color:red">**keylogger_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**KEYLOGGER** </span> như:
        * KEYLOGGER HOOK: tắt/mở theo dõi bàn phím.
        * KEYLOGGER PRINT: in ra các phím đã bấm kèm thời gian.
        * KEYLOGGER LOCK: khóa bàn phím.
        * KEYLOGGER UNLOCK: mở khóa bàn phím.
    * <span style="color:red">**screen_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**SCREEN** </span> như:
        * SCREEN TAKE: chụp màn hình.
        * SCREEN CAPTURE \<n_seconds\>: ghi màn hình \<n_seconds\> giây. 
    * <span style="color:red">**camera_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**CAMERA** </span> như:
        * CAMERA \<n_seconds\>: quay camera \<n_seconds\> giây.
    * <span style="color:red">**registry_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**REGISTRY** </span> như:
        * REGISTRY GET_VALUE \<Path\> \<name_value\>: lấy giá trị của \<name_value\> tại key có đường dẫn \<Path\> của registry.
        * REGISTRY SET_VALUE \<Path\> \<name_value\> \<value\> \<type\>: đặt giá trị của \<name_value\> tại key có đường dẫn \<Path\> của registry thành giá trị <value> với kiểu dữ liệu là \<value\> (\<value\> là một trong những giá trị ["REG_SZ", "REG_BINARY", "REG_DWORD", "REG_QWORD", "REG_MULTI_SZ", "REG_EXPAND_SZ"]).
        * REGISTRY CREATE_KEY \<Path\>: tạo key tại đường dẫn \<Path\>.
        * REGISTRY DELETE_KEY \<Path\>: xóa key tại đường dẫn \<Path\>.
    * <span style="color:red">**shutdown_logout_server.py** </span> xử lý các nhiệm vụ liên quan tới <span style="color:blue">**SHUTDOWN & LOGOUT** </span> như:
        * SHUTDOWN: tắt máy.
        * LOGOUT: đăng xuất tài khoản hiện tại trên máy.
* Folder <span style="color:red">**gui** </span> chứa file <span style="color:red">**main.py** </span> đảm nhiệm vai trò xử lý giao diện.
* File <span style="color:red">**server.py** </span> khi chạy file này thì chương trình được thực thi, giao diện sẽ hiện lên màn hình và cho phép ta tương tác với chương trình. 
## Cách chạy chương trình
Có 2 cách để chạy chương trình:
* Cách 1:

    Tải về các gói:
    * <span style="color:green">**Pillow** </span> với cách tải tại đây [INSTALLING Pillow](https://pypi.org/project/Pillow/).
    * <span style="color:green">**pystray** </span> với cách tải tại đây [INSTALLING pystray](https://pypi.org/project/pystray/).
    * <span style="color:green">**psutil** </span> với cách tải tại đây [INSTALLING psutil](https://pypi.org/project/psutil/).
    * <span style="color:green">**keyboard** </span> với cách tải tại đây [INSTALLING keyboard](https://pypi.org/project/keyboard/).
    *  <span style="color:green">**pynput** </span> với cách tải tại đây [INSTALLING pynput](https://pypi.org/project/pynput/).
    *  <span style="color:green">**opencv-python** </span> với cách tải tại đây [INSTALLING opencv-python](https://pypi.org/project/opencv-python/).
    *  <span style="color:green">**PyAutoGUI** </span> với cách tải tại đây [INSTALLING PyAutoGUI](https://pypi.org/project/PyAutoGUI/).

    Sau đó, vào thư mục Source và chạy file <span style="color:red">**server.py** </span>.
* Cách 2:

    Ta có thể chạy thông qua file <span style="color:red">**server.exe** </span> ở thư mục Release mà không cần các gói về.