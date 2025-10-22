import logging

from docx import Document

logger = logging.getLogger("desktopenv.metric.docs")


def verify(file_path: str) -> int:
    """
    验证文档中所有文本是否使用Times New Roman字体

    参数:
        file_path: 文件路径

    返回:
        int: 如果所有文本使用Times New Roman字体返回1，否则返回0
    """
    if not file_path:
        return 0

    try:
        doc = Document(file_path)
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f"Error: {e}")
        return 0

    expected_font = "Times New Roman"

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            font_name = run.font.name
            if font_name != expected_font:
                return 0
    return 1


def main():
    # 测试初始文件（应返回0）
    initial_result = verify("3/Dublin_Zoo_Intro.docx")
    print(f"初始文件验证结果: {initial_result} (应为0)")

    # 测试期待文件（应返回1）
    expected_result = verify("expected.docx")
    print(f"期待文件验证结果: {expected_result} (应为1)")


if __name__ == "__main__":
    main()
