"""Classes for parsing files of various types into valid quotes."""
import os
import subprocess
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

import pandas as pd
from docx import Document

from .Quote_Model import QuoteModel


class IngestorInterface(ABC):
    """An abstract base class for file ingestors."""

    @classmethod
    @abstractmethod
    def parse(cls, path: Path) -> List[QuoteModel]:
        """Return a parsed list of QuoteModel objects.

        :param path: (Path) specifying the data file's path.
        :return: list of QuoteModel's.
        """
        pass


class TextIngestor(IngestorInterface):
    """.txt file ingestor."""

    @classmethod
    def parse(cls, path: Path) -> List[QuoteModel]:
        """Return a parsed list of QuoteModel objects.

        :param path: (Path) specifying the data file's path.
        :return: list of QuoteModel's.
        """
        with open(path) as file:
            sep = ' - '
            return [QuoteModel(*line.split(' - '))
                    for line in file if sep in line]


class PdfIngestor(IngestorInterface):
    """.pdf file ingestor."""

    @classmethod
    def parse(cls, path: Path) -> List[QuoteModel]:
        """Return a parsed list of QuoteModel objects.

        :param path: (Path) specifying the data file's path.
        :return: list of QuoteModel's.
        """
        outfile = 'temp_text.txt'
        subprocess.run(['pdftotext', '-raw', path, outfile])
        with open(outfile) as file:
            sep = ' - '
            res = [QuoteModel(*(line.strip('\n')
                   .split(' - '))) for line in file
                   if sep in line]
        os.remove(outfile)
        return res


class DocxIngestor(IngestorInterface):
    """.docx file ingestor."""

    @classmethod
    def parse(cls, path: Path) -> List[QuoteModel]:
        """Return a parsed list of QuoteModel objects.

        :param path: Path specifying the data file's path.
        :return: list of QuoteModel's.
        """
        document = Document(docx=path)
        data = [p.text for p in document.paragraphs]
        sep = ' - '
        return [QuoteModel(*line.split(' - ')) for line in data if sep in line]


class CsvIngestor(IngestorInterface):
    """.csv file ingestor."""

    @classmethod
    def parse(cls, path: Path) -> List[QuoteModel]:
        """Return a parsed list of QuoteModel objects.

        :param path: (Path) specifying the data file's path.
        :return: list of QuoteModel's.
        """
        df = pd.read_csv(filepath_or_buffer=path)
        return [QuoteModel(**df.loc[i]) for i in df.index]


class Ingestor:
    """File parsing class."""

    legend = {'.txt': TextIngestor, '.pdf': PdfIngestor,
              '.docx': DocxIngestor, '.csv': CsvIngestor}

    @classmethod
    def get_ingestor(cls, path: Path):
        """Return an ingestor class.

        If any available, return of matching filetype.
        Else, return None.
        :param path: (Path) specifying the data's path.
        :return: a subclass IngestorInterface, or None.
        """
        suffix = path.suffix
        if suffix in cls.legend:
            return cls.legend[suffix]

    @classmethod
    def parse(cls, path) -> List[QuoteModel]:
        """Return a parsed list of QuoteModels.

        From specified file.
        :param path: (str or Path) file to parse
        """
        path = Path(path)
        ingestor = cls.get_ingestor(path)
        if ingestor is None:
            raise TypeError(f"Cannot ingest given file type: '{path.suffix}'.")
        return ingestor.parse(path)
