from typing import List
from pydantic import BaseModel
from typing import TYPE_CHECKING

from ponika.models import ApiResponse

if TYPE_CHECKING:
    from ponika import PonikaClient, ApiResponse


class MessagesEndpoint:
    def __init__(self, client: "PonikaClient") -> None:
        self.client: "PonikaClient" = client
        self.actions = self.MessagesActionsEndpoint(client)

    class MessagesResponseDataItem(BaseModel):
        """Data model for messages response."""

        message: str
        sender: str
        id: str
        modem_id: str
        status: str
        date: str

    def get_status(self) -> "ApiResponse[List[MessagesResponseDataItem]]":
        """Fetch messages from the device."""
        return ApiResponse[List[self.MessagesResponseDataItem]].model_validate(
            self.client._get(
                "/messages/status",
            )
        )

    class MessagesActionsEndpoint:
        def __init__(self, client: "PonikaClient") -> None:
            self.client: "PonikaClient" = client

        class SendResponseData(BaseModel):
            """Data model for messages action response."""

            sms_used: int

        def post_send(
            self, number: str, message: str, modem: str
        ) -> "ApiResponse[SendResponseData]":
            """Send a message to a recipient."""
            return self.client._post(
                "/messages/actions/send",
                self.SendResponseData,
                {"data": {"number": number, "message": message, "modem": modem}},
            )
