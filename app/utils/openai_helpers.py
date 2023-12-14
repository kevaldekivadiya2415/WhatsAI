from loguru import logger
from dotenv import load_dotenv
import os
from openai import OpenAI
from app.utils.templates.prompt_template import BASIC_TEXT_PROMPT, BASIC_IMAGE_PROMPT


# Load environment variables
load_dotenv()


class OpenAIHelper:
    def __init__(self) -> None:
        self.client = OpenAI(organization=None, api_key=os.getenv("OPENAI_KEY"))

    async def text_response_generation(self, text: str) -> str:
        """
        Generate a text response using OpenAI's chat completion API.

        Args:
            text (str): User input text.

        Returns:
            str: Generated text response.
        """
        try:
            resp = self.client.chat.completions.create(
                model=os.getenv("TEXT_OPENAI_MODEL"),
                messages=[
                    {"role": "system", "content": BASIC_TEXT_PROMPT},
                    {"role": "user", "content": text},
                ],
                stream=False,
                max_tokens=256,
            )
            return resp.choices[0].message.content
        except Exception as exc:
            logger.exception(f"Error in text response generation: {exc}")
            raise

    async def image_response_generation(self, image, caption: str = None) -> str:
        """
        Generate an image response using OpenAI's chat completion API.

        Args:
            image: Input image data.
            caption (str): Caption for the image.

        Returns:
            str: Generated image response.
        """
        try:
            if not caption:
                caption = BASIC_IMAGE_PROMPT
            resp = self.client.chat.completions.create(
                model=os.getenv("IMAGE_OPENAI_MODEL"),
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": caption},
                            {
                                "type": "image_url",
                                "image_url": {"url": image},
                            },
                        ],
                    }
                ],
                max_tokens=256,
            )
            return resp.choices[0].message.content
        except Exception as exc:
            logger.exception(f"Error in image response generation: {exc}")
            raise Exception("Failed to generate image response") from exc
