import uuid
from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    file_path: str
    first_character_index: int
    last_character_index: int

    def __len__(self) -> int:
        return self.last_character_index - self.first_character_index + 1

    def __str__(self) -> str:
        with open(self.file_path) as f:
            f.seek(self.first_character_index)
            return f.read(len(self)).strip()

    def info(self) -> str:
        return f'''{self.file_path:<100} \
{f"{self.first_character_index}-{self.last_character_index} ({len(self)})":>19}
{'-' * 120}
\033[2m"{self}"\033[0m
'''


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: list[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: list[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: list[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: list[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: list[MinimalAnswer]
    k: int
