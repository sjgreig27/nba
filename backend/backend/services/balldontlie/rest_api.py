import os
import requests
from typing import Optional, List, TypeVar, Generic
from loguru import logger
from pydantic import BaseModel
from abc import abstractmethod
from operator import itemgetter


class RestApiServiceException(BaseException):
    pass


Entity = TypeVar("Entity", bound=BaseModel)


class RestApiService(Generic[Entity]):
    """
    Simple class to manage simple, unpaginated Rest API endpoints from balldontlie.io
    """

    BASE_URL = "https://api.balldontlie.io/v1"

    def __init__(self):
        self.api_key = os.environ.get("BALLDONTLIE_API_KEY")
        if not self.api_key:
            raise RestApiServiceException(
                "No API key provided - add environment variable BALLDONTLIE_API_KEY"
            )

    @abstractmethod
    def get_entity_name(self) -> str:
        raise NotImplementedError(
            "Each instance of the service must define the entiy name."
        )

    def get_headers(self) -> dict:
        return {"Authorization": self.api_key}

    def get_url(self, item_id: Optional[int] = None) -> str:
        root_url = f"{self.BASE_URL}/{self.get_entity_name()}"
        if item_id is None:
            return root_url
        return f"{root_url}/{item_id}"

    def fetch_data(
        self, url: str, kwargs: Optional[dict] = None
    ) -> Entity | List[Entity]:
        headers = self.get_headers()
        kwargs = kwargs or {}
        request = requests.get(url, headers=headers, **kwargs)
        logger.debug("Fetching data from balldontlie api.")
        if not request.ok:
            logger.error(f"Failed to fetch data for url '{url}' - {request.content}")
            raise RestApiServiceException("Failed to fetch data from API.")
        data = request.json()
        return data["data"]

    def get_item_list(
        self, pagination_params: dict, kwargs: Optional[dict] = None
    ) -> List[Entity]:
        url = self.get_url()
        limit, offset = itemgetter("limit", "offset")(pagination_params)
        return self.fetch_data(url, kwargs)[offset : offset + limit]

    def get_item(self, instance_id: int, kwargs: Optional[dict] = None) -> Entity:
        url = self.get_url(instance_id)
        return self.fetch_data(url, kwargs)


class PaginatedRestApiService(RestApiService, Generic[Entity]):
    """
    Simple class to manage paginated Rest API endpoints from balldontlie.io
    """

    MAX_PAGINATION_SIZE = 100

    @abstractmethod
    def get_entity_name(self) -> str:
        super().get_entity_name()

    def get_item_list(
        self, pagination_params: dict, kwargs: Optional[dict] = None
    ) -> List[Entity]:
        url = self.get_url()
        limit, offset = itemgetter("limit", "offset")(pagination_params)
        return self.fetch_paginated_data(url, limit=limit, offset=offset, kwargs=kwargs)

    def _get_request_kwargs(self, kwargs) -> dict:
        if not kwargs:
            kwargs = {}
        if "params" not in kwargs:
            kwargs["params"] = {}
        return kwargs

    def _update_request_kwargs(self, kwargs: dict, limit: int, offset: int) -> None:
        params = kwargs["params"]
        server_limit = (
            self.MAX_PAGINATION_SIZE if limit > self.MAX_PAGINATION_SIZE else limit
        )
        params.update({"per_page": server_limit, "cursor": offset})

    def fetch_paginated_data(
        self, url: str, limit: int = None, offset=None, kwargs: Optional[dict] = None
    ) -> List[Entity]:
        headers = self.get_headers()
        request_kwargs = self._get_request_kwargs(kwargs)
        self._update_request_kwargs(request_kwargs, limit, offset)
        accumulated_data = []
        more_data_to_fetch = len(accumulated_data) < limit
        while more_data_to_fetch:
            request = requests.get(url, headers=headers, **request_kwargs)
            logger.debug("Fetching data from balldontlie api.")
            if not request.ok:
                logger.error(
                    f"Failed to fetch data for url '{url}' - {request.content}"
                )
                raise RestApiServiceException("Failed to fetch data from API.")
            data = request.json()
            accumulated_data.extend(data["data"])
            meta = data["meta"]
            next_offset = meta.get("next_cursor")
            if not next_offset or len(accumulated_data) == limit:
                break
            else:
                self._update_request_kwargs(
                    request_kwargs, limit - len(accumulated_data), next_offset
                )
        return accumulated_data
