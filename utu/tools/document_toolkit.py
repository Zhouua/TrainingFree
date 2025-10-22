"""Document toolkit for parsing documents and support Q&A.

Support backends:

- Chunkr: <https://github.com/lumina-ai-inc/chunkr>
- pymupdf: <https://github.com/pymupdf/PyMuPDF>
"""

from ..config import ToolkitConfig
from ..utils import CACHE_DIR, FileUtils, SimplifiedAsyncOpenAI, get_logger
from .base import TOOL_PROMPTS, AsyncBaseToolkit, register_tool

logger = get_logger(__name__)


class DocumentToolkit(AsyncBaseToolkit):
    def __init__(self, config: ToolkitConfig = None) -> None:
        """Initialize the DocumentToolkit, with configed parser and llm."""
        super().__init__(config)
        if self.config.config.get("parser") == "chunkr":
            from .documents.chunkr_parser import ChunkrParser

            self.parser = ChunkrParser(self.config.config)
        elif self.config.config.get("parser") == "pymupdf":
            from .documents.pdf_parser import PDFParser

            self.parser = PDFParser(self.config.config)
        else:
            raise ValueError(f"Unsupported parser: {self.config.config.get('parser')}")
        self.text_limit = self.config.config.get("text_limit", 100_000)
        self.llm = SimplifiedAsyncOpenAI(**self.config.config_llm.model_provider.model_dump())
        self.md5_to_path = {}

    async def parse_document(self, md5: str) -> str:
        logger.info(f"[tool] parse_document: {self.md5_to_path[md5]}")
        return await self.parser.parse(self.md5_to_path[md5])

    def handle_path(self, path: str) -> str:
        md5 = FileUtils.get_file_md5(path)
        if FileUtils.is_web_url(path):
            # download document to data/_document, with md5
            fn = CACHE_DIR / "documents" / f"{md5}{FileUtils.get_file_ext(path)}"
            fn.parent.mkdir(parents=True, exist_ok=True)
            if not fn.exists():
                path = FileUtils.download_file(path, fn)
                logger.info(f"Downloaded document file to {path}")
                path = fn
        self.md5_to_path[md5] = path  # record md5 to map
        return md5

    @register_tool
    async def document_qa(self, document_path: str, question: str | None = None) -> str:
        """Get file content summary or answer questions about attached document.

        Supported file types: pdf, docx, pptx, xlsx, xls, ppt, doc

        Args:
            document_path (str): Local path or URL to a document.
            question (str, optional): The question to answer. If not provided, return a summary of the document.
        """
        md5 = self.handle_path(document_path)
        document_markdown = await self.parse_document(md5)
        if len(document_markdown) > self.text_limit:
            document_markdown = document_markdown[: self.text_limit] + "\n..."
        messages = [
            {"role": "system", "content": TOOL_PROMPTS["document_sp"]},
            {"role": "user", "content": document_markdown},
        ]
        if question:
            messages.append({"role": "user", "content": TOOL_PROMPTS["document_qa"].format(question=question)})
        else:
            messages.append({"role": "user", "content": TOOL_PROMPTS["document_summary"]})
        output = await self.llm.query_one(messages=messages, **self.config.config_llm.model_params.model_dump())
        if not question:
            output = (
                f"You did not provide a particular question, so here is a detailed caption for the document: {output}"
            )
        return output
