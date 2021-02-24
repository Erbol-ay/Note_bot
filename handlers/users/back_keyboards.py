# from aiogram.types import CallbackQuery
#
# from keyboards.inline.menu import customer_menu, employee_keyboard, manager_keyboard
# from loader import dp
#
# # @dp.callback_query_handler(text="back_to_customer_menu")
# # async def customer_menu_def(call: CallbackQuery):
# #     await call.message.edit_text("Добро пожаловать")
# #     await call.message.edit_reply_markup(customer_menu)
#
# @dp.callback_query_handler(text="back_to_employee_menu")
# async def employee_menu(call: CallbackQuery):
#     await call.message.edit_text("Добро пожаловать")
#     await call.message.edit_reply_markup(employee_keyboard)
#
# @dp.callback_query_handler(text="back_to_manager_menu")
# async def manager_menu(call: CallbackQuery):
#     await call.message.edit_text(f"Добро пожаловать, {call.from_user.full_name}")
#     await call.message.edit_reply_markup(manager_keyboard)
