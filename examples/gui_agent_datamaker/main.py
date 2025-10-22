# pylint: disable=line-too-long
# ruff: noqa: E501

import asyncio
import pathlib

from utu.agents import SimpleAgent
from utu.config import ConfigLoader

INSTRUCTION = """You are an expert in agentic data construction and verification.
You should used tools to generate files that meet the user's requirements."""

VERIFY_FN = r"""def compare_font_names(docx_file, rules: List[Dict[str, Any]]):
    \"\"\"
    检查DOCX文档中所有文本是否使用指定字体

    参数:
        docx_file: DOCX文件路径
        rules: 包含期望字体名称的规则字典

    返回:
        int: 如果所有文本使用指定字体返回1，否则返回0
    \"\"\"
    if not docx_file:
        return 0

    try:
        doc = Document(docx_file)
    except Exception as e:
        logger.error(f"Error: {e}")
        return 0

    expected_font = rules["font_name"]

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            font_name = run.font.name
            if font_name != expected_font:
                return 0
    return 1
"""

query = f"""背景：我需要构造大量数据用于训练我的gui agent，训练数据由三要素组成（指令，初始文件，期待文件，验证器）。gui agent会根据指令对初始文件进行操作变成结果文件，验证器的作用就是通过对比结果文件和期待文件来检查gui agent是否完成了任务。

任务：现在，我已经给了你可以参考的验证函数 `compare_font_names`、初始文件 `Dublin_Zoo_Intro.docx`，我需要你生成：1. 指令 `instruction.txt` ；2. 期待文件 `expected_output.docx`；3. 验证脚本 `verifier.py`。

任务要求：
1. 指令要求：1）当前的gui-agent能力较差，只能完成很简单的指令，因此给出的任务指令不要太复杂，1个操作就能完成的那种最好；2）并且指令必须和我给定的验证函数有关；3）指令必须清晰、准确、无歧义，不能是含糊的指令，例如“添加文本”这种指令，具体是什么文本、添加在哪里，都没描述清楚，这种就是不好的；4）生成的指令保存在instruction.txt中。
2. 期待文件：1）初始文件就用我给定的就好，你不要再生成；2）你得写python脚本，让脚本基于初始文件进行修改得到期待文件，而且期待文件必须严格对应于对【初始文件】执行【instruction】的结果
3. 验证脚本：1）参考我提供的可验证函数，可以直接拿来用，也可以做适当的修改，但千万不能偏离验证函数的本意；2）假如要对提供的参考验证函数进行修改，千万别修改函数的形式参数，例如，如果参考函数是提供对比结果文件和期待文件来实现验证，那就不要改变这个验证思路。
4. 当你生成完（指令、期待文件、验证脚本）以后，你需要用初始文件和期待文件分别验证一下你的验证脚本是否按照预期work，按照预期的话初始文件应该返回0，期待文件返回1。如果验证没通过，你得找出问题并且修正，直到完成任务

这是参考的验证函数:
```py
{VERIFY_FN}
```

下面, 开始任务!
"""


async def main():
    config = ConfigLoader.load_agent_config("examples/gui_agent_datamaker")
    # setup worksapce
    assert "bash" in config.toolkits, "bash toolkit is not in config!"
    workspace_path = pathlib.Path(__file__).parent / "data"
    config.toolkits["bash"].config["workspace_root"] = str(workspace_path)

    async with SimpleAgent(config=config, name="gui-agent-toolmaker", instructions=INSTRUCTION) as agent:
        await agent.chat_streamed(query)


if __name__ == "__main__":
    asyncio.run(main())
