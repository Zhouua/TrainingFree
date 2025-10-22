from docx import Document

# 打开docs文件
doc = Document("expected_output.docx")

# 修改所有段落文本的字体
for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        run.font.name = "Arial"

# 保存修改后的文件
doc.save("expected_output.docx")
