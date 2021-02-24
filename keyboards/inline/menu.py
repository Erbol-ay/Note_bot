from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

inline_choose_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Я клиент",
                callback_data="customer"
            )
        ],
        [
            InlineKeyboardButton(
                text="Я сотрудник",
                callback_data="employee"
            )
        ],
        [
            InlineKeyboardButton(
                text="Я менеджер",
                callback_data="manager"
            )
        ]
    ]
)

customer_menu = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(
                                                 text="Услуги",
                                                 callback_data="services"
                                             )
                                         ],
                                         [
                                             InlineKeyboardButton(
                                                 text="Где находится",
                                                 callback_data="where_is"
                                             )
                                         ],
                                         [
                                             InlineKeyboardButton(
                                                 text="Контакты",
                                                 callback_data="contacts"
                                             ),
                                             InlineKeyboardButton(
                                                 text="Оставить данные",
                                                 callback_data="leave_contacts"
                                             )
                                         ],
                                         [
                                             InlineKeyboardButton(
                                                 text="Назад",
                                                 callback_data="back_to_choose_menu"
                                             )
                                         ]
                                     ])

employee_keyboard = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                            InlineKeyboardButton(
                                                text="Я пришел",
                                                callback_data="employee_arrived"
                                         ),
                                            InlineKeyboardButton(
                                                text="Информация",
                                                callback_data="employee_info"
                                         )
                                         ],
                                         [
                                             InlineKeyboardButton(
                                                 text="Назад",
                                                 callback_data="back_to_choose_menu"
                                             )
                                         ]
                                     ])

manager_keyboard = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(
                                                    text="Все работники",
                                                    callback_data="all_employees_info"
                                                ),
                                                InlineKeyboardButton(
                                                    text="Данные",
                                                    callback_data="database"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Добавить сотрудника",
                                                    callback_data="add_new_employee"
                                                ),
                                                InlineKeyboardButton(
                                                    text="Удалить сотрудника",
                                                    callback_data="delete_employee"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Уствновить местоположение",
                                                    callback_data="set_main_GPS"
                                                ),
                                                InlineKeyboardButton(
                                                    text="Сменить пароль",
                                                    callback_data="change_password"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Начало работы",
                                                    callback_data="start_time"
                                                ),
                                                InlineKeyboardButton(
                                                    text="Допустимая минута",
                                                    callback_data="allowed_time"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Штраф",
                                                    callback_data="fine"
                                                ),
                                                InlineKeyboardButton(
                                                    text="Увеличенный штраф",
                                                    callback_data="increased_fine"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Дни для увеличенного штрафа",
                                                    callback_data="charge"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Сбросить",
                                                    callback_data="restore"
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Назад",
                                                    callback_data="back_to_choose_menu"
                                                )
                                            ]
                                        ])

back_to_customer_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_customer_menu"
            )
        ]
    ]
)

back_to_employee_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_employee_menu"
            )
        ]
    ]
)

back_to_manager_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_manager_menu"
            )
        ]
    ]
)

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Нажмите для отправки",
                request_location=True
            )
        ]
    ],
    resize_keyboard=True
)