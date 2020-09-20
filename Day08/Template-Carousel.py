carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png',
                image_background_color='#FFFFFF',
                title='this is menu1',
                text='description1',
                actions=[
                    PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message1',
                        text='message text1'
                    ),
                    URIAction(
                        label='uri1',
                        uri='http://google.com'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png',
                image_background_color='#FFFFFF',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    ),
                    URIAction(
                        label='uri2',
                        uri='http://google.com'
                    )
                ]
            )
        ]
        image_aspect_ratio='rectangle',
        image_size='cover'
    )
)
line_bot_api.reply_message(reply_token, carousel_template_message)