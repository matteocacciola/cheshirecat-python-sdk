import json
from pathlib import Path
from typing import Dict, Any, List
import aiohttp

from api.endpoints.base import AbstractEndpoint
from api.models.api.rabbitholes import AllowedMimeTypesOutput


class RabbitHoleEndpoint(AbstractEndpoint):
    def __init__(self, client: "CheshireCatClient"):
        super().__init__(client)
        self.prefix = "/rabbithole"

    async def post_file(
        self,
        file_path,
        file_name: str | None = None,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
        agent_id: str | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> aiohttp.ClientResponse:
        """
        This method posts a file to the RabbitHole API. The file is uploaded to the RabbitHole server and ingested into
        the RAG system. The file is then processed by the RAG system and the results are stored in the RAG database.
        The process is asynchronous and the results are returned in a batch.
        The CheshireCat processes the injection in background and the client will be informed at the end of the process.
        :param file_path: The path to the file to upload.
        :param file_name: The name of the file.
        :param chunk_size: The size of the chunks to split the file into.
        :param chunk_overlap: The overlap of the chunks.
        :param agent_id: The ID of the agent.
        :param metadata: The metadata to include with the file.
        :return: The response from the RabbitHole API.
        """
        file_name = file_name or Path(file_path).name

        data = aiohttp.FormData()
        with open(file_path, "rb") as f:
            data.add_field("file", f, filename=file_name)

        if chunk_size is not None:
            data.add_field("chunk_size", str(chunk_size))

        if chunk_overlap is not None:
            data.add_field("chunk_overlap", str(chunk_overlap))

        if metadata is not None:
            data.add_field("metadata", json.dumps(metadata))

        async with self.get_async_http_client(agent_id) as client:
            result = await client.post(self.prefix, data=data)
            await client.close()
            return result

    async def post_files(
        self,
        file_paths: List[str],
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
        agent_id: str | None = None,
        metadata: Dict[str, Any] | None = None
    ) -> aiohttp.ClientResponse:
        """
        Posts multiple files to the RabbitHole API. The files are uploaded to the RabbitHole server and
        ingested into the RAG system. The files are processed in a batch. The process is asynchronous.
        The CheshireCat processes the injection in background and the client will be informed at the end of the process.
        :param file_paths: The paths to the files to upload.
        :param chunk_size: The size of the chunks to split the files into.
        :param chunk_overlap: The overlap of the chunks.
        :param agent_id: The ID of the agent.
        :param metadata: The metadata to include with the files.
        :return: The response from the RabbitHole API.
        """
        data = aiohttp.FormData()

        for file_path in file_paths:
            with open(file_path, "rb") as f:
                data.add_field("files", f, filename=Path(file_path).name)

        if chunk_size is not None:
            data.add_field("chunk_size", str(chunk_size))

        if chunk_overlap is not None:
            data.add_field("chunk_overlap", str(chunk_overlap))

        if metadata is not None:
            data.add_field("metadata", json.dumps(metadata))

        async with self.get_async_http_client(agent_id) as client:
            result = await client.post(f"{self.prefix}/batch", data=data)
            await client.close()
            return result

    async def post_web(
        self,
        web_url: str,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
        agent_id: str | None = None,
        metadata: Dict[str, Any] | None = None
    ) -> aiohttp.ClientResponse:
        """
        Posts a web URL to the RabbitHole API. The web URL is ingested into the RAG system. The web URL is
        processed by the RAG system by Web scraping and the results are stored in the RAG database.
        The process is asynchronous.
        The CheshireCat processes the injection in background and the client will be informed at the end of the process.
        :param web_url: The URL of the website to ingest.
        :param chunk_size: The size of the chunks to split the files into.
        :param chunk_overlap: The overlap of the chunks.
        :param agent_id: The ID of the agent.
        :param metadata: The metadata to include with the files.
        :return: The response from the RabbitHole API.
        """
        payload = {"url": web_url}

        if chunk_size is not None:
            payload["chunk_size"] = chunk_size

        if chunk_overlap is not None:
            payload["chunk_overlap"] = chunk_overlap

        if metadata is not None:
            payload["metadata"] = metadata

        async with self.get_async_http_client(agent_id) as client:
            result= await client.post(f"{self.prefix}/web", json=payload)
            await client.close()
            return result

    async def post_memory(
        self,
        file_path: str,
        file_name: str | None = None,
        agent_id: str | None = None
    ) -> aiohttp.ClientResponse:
        """
        Posts a memory point, either for the agent identified by the agent_id parameter (for multi-agent
        installations) or for the default agent (for single-agent installations). The memory point is ingested into the
        RAG system. The process is asynchronous. The provided file must be in JSON format.
        The CheshireCat processes the injection in background and the client will be informed at the end of the process.
        :param file_path: The path to the file to upload.
        :param file_name: The name of the file.
        :param agent_id: The ID of the agent.
        :return: The response from the RabbitHole API.
        """
        file_name = file_name or Path(file_path).name

        data = aiohttp.FormData()
        with open(file_path, "rb") as f:
            data.add_field("file", f, filename=file_name)

        async with self.get_async_http_client(agent_id) as client:
            result = await client.post(f"{self.prefix}/memory", data=data)
            await client.close()
            return result

    def get_allowed_mime_types(self, agent_id: str | None = None) -> AllowedMimeTypesOutput:
        """
        Retrieves the allowed MIME types for the RabbitHole API. The allowed MIME types are the MIME types
        that are allowed to be uploaded to the RabbitHole API. The allowed MIME types are returned in a list.
        If the agent_id parameter is provided, the allowed MIME types are retrieved for the agent identified by the
        agent_id parameter (for multi-agent installations). If the agent_id parameter is not provided, the allowed MIME
        types are retrieved for the default agent (for single-agent installations).
        :param agent_id: The ID of the agent.
        :return: AllowedMimeTypesOutput, the details of the allowed MIME types.
        """
        return self.get(f"{self.prefix}/allowed-mimetypes", AllowedMimeTypesOutput, agent_id)
