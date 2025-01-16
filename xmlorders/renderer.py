from rest_framework.renderers import BaseRenderer
import xml.etree.ElementTree as ET

class XMLRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Рендеринг данных в XML-формате.
        """
        if data is None:
            return ''

        # Если есть ошибка (например, 404 или 500), сериализуем как `<error>`
        if isinstance(data, dict) and 'detail' in data:
            root = ET.Element('error')
            message = ET.SubElement(root, 'message')
            message.text = str(data['detail'])
        else:
            # Основной случай: сериализуем данные как `<response>`
            root = ET.Element('response')
            for key, value in data.items():
                element = ET.SubElement(root, key)
                element.text = str(value)

        return ET.tostring(root, encoding='utf-8', method='xml')
