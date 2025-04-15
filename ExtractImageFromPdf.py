import os
import fitz  # PyMuPDF
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import base64
from io import BytesIO
import re
import webbrowser

def get_image_hash(image_data):
    return hashlib.md5(image_data).hexdigest()

def extract_images_from_pdf(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_data = base_image["image"]
            images.append((f"page_{page_num + 1}_img_{img_index + 1}.png", image_data))
    return sorted(images, key=lambda x: extract_page_number(x[0]))

def compare_images(images1, images2):
    images1_dict = {get_image_hash(img_data): (img_name, img_data) for img_name, img_data in images1}
    images2_dict = {get_image_hash(img_data): (img_name, img_data) for img_name, img_data in images2}
    
    common_images = []
    for hash_value in set(images1_dict.keys()) & set(images2_dict.keys()):
        img1_name, img1_data = images1_dict[hash_value]
        img2_name, img2_data = images2_dict[hash_value]
        common_images.append((img1_name, img1_data, img2_name, img2_data))
    
    return sorted(common_images, key=lambda x: extract_page_number(x[0]))



def save_images(images, output_dir, pdf_filenames):
    for pdf_filename in pdf_filenames:
        # 创建以 PDF 文件名为目录
        pdf_output_dir = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_filename))[0])
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # 保存图片到对应的目录
        for img_name, img_data in images:
            img_path = os.path.join(pdf_output_dir, img_name)
            # 将 bytes 转换为 PIL.Image 对象
            image = Image.open(BytesIO(img_data))
            image.save(img_path)
            #print(f"Saved {img_path}")

def generate_html(common_images, output_dir):
    html_content = '<html><head><title>PDF Image Comparison Result</title></head><body>\n'
    html_content += '<h1>PDF 图片对比结果</h1>\n'

    if not common_images:
        html_content += '<p>No common images found between the two PDFs(俩个文件中没有相同图片).</p>\n'
    else:
        html_content += '<table>\n'
        for img1_name, img1_data, img2_name, img2_data in common_images:
            img1_base64 = base64.b64encode(img1_data).decode('utf-8')
            img2_base64 = base64.b64encode(img2_data).decode('utf-8')
            html_content += '<tr>\n'
            html_content += f'<td><img src="data:image/png;base64,{img1_base64}" alt="{img1_name}"> (Page: {extract_page_number(img1_name)})</td>\n'
            html_content += f'<td><img src="data:image/png;base64,{img2_base64}" alt="{img2_name}"> (Page: {extract_page_number(img2_name)})</td>\n'
            html_content += '</tr>\n'
        html_content += '</table>\n'

    html_content += '</body></html>\n'
    
    html_path = os.path.join(output_dir, 'result.html')
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    return html_path
    
def extract_page_number(filename):
    match = re.search(r'page_(\d+)_img_\d+\.\w+', filename)
    if match:
        return int(match.group(1))
    return None

def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 选择两个 PDF 文件
    file_paths = filedialog.askopenfilenames(title="请选择俩个PDF文件", filetypes=[("PDF files", "*.pdf")])
    if len(file_paths) != 2:
        print("请按Ctrl键选中俩个PDF文件")
        
        messagebox.showerror("错误", "请按Ctrl键选中俩个PDF文件")
        return

    file1_path = file_paths[0]
    file2_path = file_paths[1]

    print(f"File 1: {file1_path}")
    print(f"File 2: {file2_path}")

    # 提取图片
    images1 = extract_images_from_pdf(file1_path)
    images2 = extract_images_from_pdf(file2_path)

    # 比较图片
    common_images = compare_images(images1, images2)

    pdf_filenames = [file1_path, file2_path]
    # 保存图片
    output_dir = 'static/output'
    file_01=output_dir+""
    save_images([(img1_name, img1_data) for img1_name, img1_data, _, _ in common_images], output_dir,pdf_filenames)

    # 生成 HTML 文件
    html_path = generate_html(common_images, output_dir)

    # 自动打开生成的 HTML 文件
    webbrowser.open(html_path)

    print(f"Result saved to {html_path}")

if __name__ == '__main__':
    main()