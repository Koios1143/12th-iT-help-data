image_carousel_template_message = TemplateSendMessage(
    alt_text='ImageCarousel template',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png',
                action=PostbackAction(
                    label='postback1',
                    display_text='postback text1',
                    data='action=buy&itemid=1'
                )
            ),
            ImageCarouselColumn(
                image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png',
                action=PostbackAction(
                    label='postback2',
                    display_text='postback text2',
                    data='action=buy&itemid=2'
                )
            )
        ]
    )
)
line_bot_api.reply_message(reply_token, image_carousel_template_message)