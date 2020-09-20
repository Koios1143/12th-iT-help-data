buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2014/08/Placekitten480.jpg',
        image_aspect_ratio='rectangle',
        image_size='contain',
        image_background_color='#FFFFFF',
        title='Menu',
        text='Please select',
        default_action=URIAction(
            label='view detail',
            uri='http://example.com/page/123'
        )
        actions=[
            PostbackAction(
                label='postback',
                display_text='postback text',
                data='action=buy&itemid=1'
            ),
            LocationAction(
                label='location'
            ),
            DatetimePickerAction(
                label='Select date',
                data='storeId=12345',
                mode='datetime',
                initial="2018-12-25T00:00",
                min='2017-01-24T23:59',
                max='2018-12-25T00:00'
            )
        ]
    )
)
line_bot_api.reply_message(reply_token, buttons_template_message)