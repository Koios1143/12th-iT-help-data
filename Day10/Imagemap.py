imagemap_message = ImagemapSendMessage(
    base_url='https://github.com/line/line-bot-sdk-nodejs/raw/master/examples/kitchensink/static/rich',
    alt_text='this is an imagemap',
    base_size=BaseSize(height=1040, width=1040),
    video=Video(
        original_content_url='https://github.com/line/line-bot-sdk-nodejs/raw/master/examples/kitchensink/static/imagemap/video.mp4',
        preview_image_url='https://github.com/line/line-bot-sdk-nodejs/raw/master/examples/kitchensink/static/imagemap/preview.jpg',
        area=ImagemapArea(
            x=0, y=0, width=1040, height=520
        ),
        external_link=ExternalLink(
            link_uri='https://scist.org',
            label='See More',
        ),
    ),
    actions=[
        URIImagemapAction(
            link_uri='https://google.com/',
            area=ImagemapArea(
                x=0, y=520, width=520, height=520
            )
        ),
        MessageImagemapAction(
            text='hello',
            area=ImagemapArea(
                x=520, y=520, width=520, height=520
            )
        )
    ]
)
line_bot_api.reply_message(reply_token, imagemap_message)