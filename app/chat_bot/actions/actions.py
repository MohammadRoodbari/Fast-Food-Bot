from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Form, Restarted, SlotSet, ActionExecuted, AllSlotsReset
from rasa_sdk.types import DomainDict


class ActionResetBot(Action):
    def name(self):
        return "action_reset_bot"

    def run(self, dispatcher, tracker, domain):
        # Reset all the slots
        reset_slots = [SlotSet(slot, None) for slot in tracker.slots.keys()]
        return [Restarted()] + reset_slots

class HandleConfirmation(Action):
    def name(self):
        return "handle_confirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        last_intent = tracker.latest_message['intent'].get('name')

        if last_intent == "affirm":
            dispatcher.utter_message(text="سفارش شما با موفقیت ثبت و ارسال شد.")
            return [AllSlotsReset(), Restarted()]
        elif last_intent == "deny":
            dispatcher.utter_message(text="چکار میتونم انجام بدم")
            return [AllSlotsReset(), Restarted()]

        return []
    
class ActionCheckInform(Action):
    def name(self):
        return "action_check_inform"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        entities = tracker.latest_message['entities']
        
        if not entities:
            dispatcher.utter_message(text="لطفا پیام خود را دوباره ارسال کنید")
        # else:
        #     # Proceed with the normal flow if entities are present
        #     dispatcher.utter_message(text="دریافت شد، در حال پردازش درخواست شما هستیم.")

        return []



class ActionDeactivateLoop(Action):

    def name(self) -> Text:
        return "action_deactivate_loop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Set pizza_size and pizza_type to None
        dispatcher.utter_message(text="سفارش شما با موفقیت حذف شد")
        return [
            SlotSet("pizza_size", None),
            SlotSet("pizza_type", None),
            Restarted(),
            # Form(None)  # This deactivates the active form
        ]


available_pizza_TYPES = ["سبزیجات", "گوشت"]
ALLOWED_pizza_TYPES = ["پپرونی", "استیک", "سبزیجات", "گوشت", "مرغ"]
ALLOWED_pizza_SIZES = ["کوچک", "متوسط", "بزرگ"]
pizza_prices = {"پپرونی" : 220,
                "استیک" : 300,
                "سبزیجات" : 250,
                "گوشت" : 310,
                "مرغ" : 290}

# class CheckAvailablePizza(FormValidationAction):
#     def name(self) -> Text:
#         return "check_available_pizza"

#     def check_available_pizza(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `pizza_type` value."""

#         if slot_value not in available_pizza_TYPES:
#             dispatcher.utter_message(text=f"تنها پیتزا های موجود برابر است با : {ALLOWED_pizza_SIZES}")
#             return {"pizza_size": None}
#         # dispatcher.utter_message(text=f" {slot_value} وزن میوه میشه.")
#         # return {"pizza_size": slot_value}
    
class ValidatepizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_form"

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        if slot_value not in ALLOWED_pizza_SIZES:
            dispatcher.utter_message(text=f"تنها وزن های موجود برابر است با : {ALLOWED_pizza_SIZES}")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f" {slot_value} اندازه پیتزا سفارش داده شده")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_pizza_TYPES:
            dispatcher.utter_message(
                text=f"در حال حاضر تنها پیتزا های موجود در منو {'/'.join(ALLOWED_pizza_TYPES)} می باشد."
            )
            return {"pizza_type": None}
        dispatcher.utter_message(text=f" {slot_value} نوع پیتزا سفارش داده شده:")
        return {"pizza_type": slot_value}
    
    def validate_pizza_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_number` value."""

        if int(slot_value) > 10:
            dispatcher.utter_message(
                text=f" بیشترین تعداد سفارش پیتزا ۱۰ عدد می باشد"
            )
            return {"pizza_number": None}
        dispatcher.utter_message(text=f" {slot_value} تعداد سفارش پیتزا")
        return {"pizza_number": slot_value}


        # - [\d]{1,2}[$]