from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class HeadingBlock(blocks.CharBlock):

    class Meta:
        form_classname = 'full title'
        icon = 'title'
        template = 'blocks/heading_block.html'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'blocks/image_block.html'


class AccordionItem(blocks.StructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'link'])


class AccordionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    items = blocks.StreamBlock([
        ('item', AccordionItem()),
    ])

    class Meta:
        template = 'blocks/accordion_block.html'


class ContentBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    paragraph = blocks.RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'link'])
    image = ImageBlock()
    accordion = AccordionBlock()
