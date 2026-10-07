"""In-memory clue lookup and filtering."""

from dataclasses import dataclass

from .models import CategoryPage, Clue, CluePage, Round


@dataclass(frozen=True)
class ClueRepository:
    clues: tuple[Clue, ...]
    dataset_version: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "_by_id", {clue.id: clue for clue in self.clues})
        object.__setattr__(self, "_categories", tuple(sorted({c.category for c in self.clues})))

    def get(self, clue_id: int) -> Clue | None:
        return self._by_id.get(clue_id)

    def search(
        self,
        *,
        query: str | None,
        category: str | None,
        round_: Round | None,
        limit: int,
        offset: int,
    ) -> CluePage:
        query_folded = query.casefold() if query else None
        category_folded = category.casefold() if category else None
        matches = [
            clue
            for clue in self.clues
            if (query_folded is None or query_folded in clue.prompt.casefold())
            and (category_folded is None or category_folded == clue.category.casefold())
            and (round_ is None or round_ == clue.round)
        ]
        items = matches[offset : offset + limit]
        return CluePage(
            items=items,
            limit=limit,
            offset=offset,
            has_more=offset + len(items) < len(matches),
            dataset_version=self.dataset_version,
        )

    def categories(self, *, query: str | None, limit: int, offset: int) -> CategoryPage:
        query_folded = query.casefold() if query else None
        matches = [
            category
            for category in self._categories
            if query_folded is None or query_folded in category.casefold()
        ]
        items = matches[offset : offset + limit]
        return CategoryPage(
            items=items,
            limit=limit,
            offset=offset,
            has_more=offset + len(items) < len(matches),
            dataset_version=self.dataset_version,
        )
