import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import re
from concurrent.futures import ThreadPoolExecutor

# Yêu cầu người dùng nhập đường dẫn tải ảnh
url = input("Nhập đường dẫn tải ảnh: ")

# Tạo thư mục mới dựa trên tên cuối cùng của đường dẫn ảnh
folder_name = url.split('/')[-1].split('.')[0]
output_dir = f"D:/2023/Anh trang teeturtle/{folder_name}"

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Tải HTML của trang web
response = requests.get(url)
html_content = response.content

# Phân tích cú pháp HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Tìm tất cả các thẻ hình ảnh có lớp là "product-image"
image_tags = soup.find_all('img', class_='product-image')

# Lưu danh sách các đường dẫn ảnh cần tải
image_urls = []

# Lặp qua từng thẻ hình ảnh và lấy đường dẫn (attribute 'src')
for img_tag in image_tags:
    # Kiểm tra các thuộc tính khác nhau chứa đường dẫn ảnh
    if 'src' in img_tag.attrs:
        image_url = img_tag['src']
    elif 'data-src' in img_tag.attrs:
        image_url = img_tag['data-src']
    elif 'data-original' in img_tag.attrs:
        image_url = img_tag['data-original']
    else:
        continue

    # Thay đổi đường dẫn ảnh từ -500x500 thành -1000x1000
    image_url = re.sub(r'-500x500\.', '-1000x1000.', image_url)

    # Kiểm tra xem đường dẫn có đầy đủ hay không
    if not urllib.parse.urlparse(image_url).scheme:
        # Nếu không có scheme (http, https), thêm đường dẫn gốc vào trước
        image_url = urllib.parse.urljoin(url, image_url)

    image_urls.append(image_url)

# Hàm tải xuống và lưu ảnh
def download_image(image_url):
    # Tạo đường dẫn tệp lưu trữ ảnh
    image_filename = image_url.split('/')[-1]
    image_path = os.path.join(output_dir, image_filename)

    # Tải xuống và lưu ảnh
    response = requests.get(image_url)
    with open(image_path, 'wb') as file:
        file.write(response.content)

    print(f"Đã tải xuống và lưu {image_filename}")

# Sử dụng ThreadPoolExecutor để tải xuống các ảnh đồng thời
with ThreadPoolExecutor() as executor:
    # Chạy các luồng tải xuống
    executor.map(download_image, image_urls)

print("Hoàn thành tải xuống và lưu ảnh.")
