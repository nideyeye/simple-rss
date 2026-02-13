"""
翻译客户端
提供多种翻译服务的统一接口
"""
import logging
from typing import Optional, Dict
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class TranslationProvider(ABC):
    """翻译服务提供者基类"""

    @abstractmethod
    def translate(self, text: str, from_lang: str = 'auto', to_lang: str = 'zh') -> Optional[str]:
        """
        翻译文本

        Args:
            text: 待翻译文本
            from_lang: 源语言代码（auto 表示自动检测）
            to_lang: 目标语言代码

        Returns:
            翻译后的文本，失败时返回 None
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查服务是否可用"""
        pass


class DummyTranslator(TranslationProvider):
    """模拟翻译器（用于测试）"""

    def translate(self, text: str, from_lang: str = 'auto', to_lang: str = 'zh') -> Optional[str]:
        return f"[翻译 {to_lang}] {text}"

    def is_available(self) -> bool:
        return True


class GoogleTranslateClient(TranslationProvider):
    """Google 翻译客户端（需要 googletrans 库）"""

    def __init__(self):
        try:
            from googletrans import Translator
            self.translator = Translator()
            self._available = True
        except ImportError:
            logger.warning("googletrans 库未安装，Google 翻译不可用")
            self._available = False

    def translate(self, text: str, from_lang: str = 'auto', to_lang: str = 'zh') -> Optional[str]:
        if not self.is_available():
            return None

        try:
            result = self.translator.translate(text, src=from_lang, dest=to_lang)
            return result.text
        except Exception as e:
            logger.exception(f"Google 翻译失败: {e}")
            return None

    def is_available(self) -> bool:
        return self._available


class DeepLClient(TranslationProvider):
    """DeepL 翻译客户端"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._available = bool(api_key)

    def translate(self, text: str, from_lang: str = 'auto', to_lang: str = 'zh') -> Optional[str]:
        if not self.is_available():
            return None

        try:
            import requests

            # DeepL API URL
            url = "https://api-free.deepl.com/v2/translate"
            if not self.api_key.endswith(':fx'):
                url = "https://api.deepl.com/v2/translate"

            data = {
                'auth_key': self.api_key,
                'text': text,
                'source_lang': from_lang.upper() if from_lang != 'auto' else None,
                'target_lang': to_lang.upper(),
            }

            response = requests.post(url, data=data)
            response.raise_for_status()

            result = response.json()
            return result['translations'][0]['text']

        except Exception as e:
            logger.exception(f"DeepL 翻译失败: {e}")
            return None

    def is_available(self) -> bool:
        return self._available


class TranslationService:
    """翻译服务"""

    def __init__(self, provider: Optional[TranslationProvider] = None):
        self.provider = provider or DummyTranslator()

    def translate(self, text: str, from_lang: str = 'auto', to_lang: str = 'zh') -> Optional[str]:
        """翻译文本"""
        if not text or not text.strip():
            return text

        return self.provider.translate(text, from_lang, to_lang)

    def is_available(self) -> bool:
        """检查翻译服务是否可用"""
        return self.provider.is_available()


def create_translation_service(config: Dict) -> TranslationService:
    """
    根据配置创建翻译服务

    Args:
        config: 配置字典，格式如：
            {
                'provider': 'google' | 'deepl' | 'dummy',
                'api_key': '...' (可选)
            }

    Returns:
        翻译服务实例
    """
    provider_name = config.get('provider', 'dummy').lower()
    api_key = config.get('api_key')

    if provider_name == 'google':
        provider = GoogleTranslateClient()
    elif provider_name == 'deepl':
        provider = DeepLClient(api_key)
    else:
        provider = DummyTranslator()

    return TranslationService(provider)
